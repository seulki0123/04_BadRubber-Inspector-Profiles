"""Grade Selection loader.

Given `(line, grade)` from `production_information`, the foundation profile is
resolved purely by convention:

    products/<LINE>/_<grade>.py        where <LINE> = line.replace("-", "")

e.g. (line="BR-B", grade="F2150")  ->  profiles.products.BRB._F2150

Each base module exports `build_profile(checkpoint_root) -> Profile`. The
resolved Profile is then reshaped into what `Detector`, `BalerClassification`
and friends already consume: `classifier.classes`, `segmenter.classes`, etc.

There is no registry and no override layer: everything a (line, grade) needs
(classes, checkpoints, thresholds, `return_mode`, `show`) lives in its base
profile module.
"""
from __future__ import annotations

import importlib
import os
from typing import Tuple

import yaml

from ._schema import Profile


# ---------------------------------
# Foundation profile resolution (convention-based)
# ---------------------------------

def _base_module(line: str, grade: str) -> str:
    """Module path of the foundation profile for a (line, grade) pair.

    Convention: `products/<LINE>/_<grade>.py` with `<LINE> = line` minus dashes.
    """
    folder = line.replace("-", "")
    return f"profiles.products.{folder}._{grade}"


def _load_base_profile(line: str, grade: str, checkpoint_root: str) -> Profile:
    mod_name = _base_module(line, grade)
    try:
        module = importlib.import_module(mod_name)
    except ModuleNotFoundError as e:
        # Only treat this as "no such profile" when the *target* module (or its
        # package) is what's missing. A bad import *inside* an existing profile
        # file must surface as-is, not be masked as an unknown grade.
        if e.name and mod_name.startswith(e.name):
            folder = line.replace("-", "")
            raise ValueError(
                f"No profile for (line={line!r}, grade={grade!r}): expected "
                f"module {mod_name} (file products/{folder}/_{grade}.py)."
            ) from e
        raise
    if not hasattr(module, "build_profile"):
        raise ValueError(
            f"{mod_name} must export `build_profile(checkpoint_root) -> Profile`"
        )
    return module.build_profile(checkpoint_root)


def load_profile(line: str, grade: str, checkpoint_root: str) -> dict:
    """Resolve the (line, grade) foundation profile into a plain dict.

    `checkpoint_root` is injected into the base profile factory so every
    checkpoint path is anchored at a single user-controlled root.

    Returns the Profile as a plain dict (see `Profile.to_dict`).
    """
    if not checkpoint_root:
        raise ValueError("load_profile: `checkpoint_root` must be a non-empty path.")
    return _load_base_profile(line, grade, checkpoint_root).to_dict()


# ---------------------------------
# Shaping helpers for downstream consumers
# ---------------------------------

def _inject_classes(resolved: dict) -> dict:
    """Attach the appropriate classes dict to each model section so that
    downstream constructors can read `config["classifier"]["classes"]` etc.
    """
    out = dict(resolved)

    if out.get("classifier") is not None and out.get("classify_classes") is not None:
        out["classifier"] = {**out["classifier"], "classes": out["classify_classes"]}

    if out.get("dot_classifier") is not None:
        if out.get("dot_classify_classes") is None:
            raise ValueError(
                "dot_classifier is enabled but `dot_classify_classes` is not set. "
                "Define dot-specific classes in the base profile."
            )
        out["dot_classifier"] = {
            **out["dot_classifier"],
            "classes": out["dot_classify_classes"],
        }

    if out.get("segmenter") is not None:
        seg = out["segmenter"]
        if isinstance(seg, dict):
            # legacy single-model: inject shared `segment_classes` if present
            if out.get("segment_classes") is not None:
                out["segmenter"] = {**seg, "classes": out["segment_classes"]}
        elif isinstance(seg, list):
            # multi-checkpoint: each entry must carry its own `classes` inline
            normalized = []
            for i, entry in enumerate(seg):
                if not isinstance(entry, dict):
                    raise TypeError(
                        f"segmenter[{i}] must be a dict, got {type(entry).__name__}"
                    )
                if "checkpoint" not in entry:
                    raise ValueError(f"segmenter[{i}] missing 'checkpoint' field")
                if entry.get("classes") is None:
                    raise ValueError(
                        f"segmenter[{i}] missing 'classes'. In multi-checkpoint mode "
                        "each entry must define its own `classes` dict (use "
                        "`pass: True` to opt this model out of a class)."
                    )
                normalized.append(entry)
            out["segmenter"] = normalized
        else:
            raise TypeError(
                f"segmenter must be a dict or list of dicts, got {type(seg).__name__}"
            )

    if out.get("anomaly_cluster") is not None and out.get("cluster_classes") is not None:
        out["anomaly_cluster"] = {**out["anomaly_cluster"], "classes": out["cluster_classes"]}

    if out.get("dot_cluster") is not None and out.get("cluster_classes") is not None:
        out["dot_cluster"] = {**out["dot_cluster"], "classes": out["cluster_classes"]}

    return out


def to_defect_detection_config(resolved: dict) -> dict:
    """Shape the resolved profile into the dict structure historically returned
    by `utils.config.load_config()` for DefectDetection.

    Keys: bgremover, anomalyclip, classifier, dot_classifier, segmenter, anomaly_cluster,
    dot_detector1, dot_detector2, tile_detector, dot_cluster, dot_confidence_by_side,
    show, return_mode.
    """
    shaped = _inject_classes(resolved)
    return {
        "bgremover": shaped.get("bgremover"),
        "anomalyclip": shaped.get("anomalyclip"),
        "classifier": shaped.get("classifier"),
        "dot_classifier": shaped.get("dot_classifier"),
        "segmenter": shaped.get("segmenter"),
        "anomaly_cluster": shaped.get("anomaly_cluster"),
        "dot_detector1": shaped.get("dot_detector1"),
        "dot_detector2": shaped.get("dot_detector2"),
        "tile_detector": shaped.get("tile_detector"),
        "dot_cluster": shaped.get("dot_cluster"),
        "dot_confidence_by_side": shaped.get("dot_confidence_by_side"),
        "patchcore": shaped.get("patchcore"),
        "patchcore_active_by_side": shaped.get("patchcore_active_by_side"),
        "show": shaped.get("show") or {},
        "return_mode": shaped.get("return_mode"),
    }


def to_baler_classification_config(resolved: dict) -> dict:
    """Shape the baler side of the resolved profile for BalerClassification."""
    return {"classifier": resolved.get("baler_classifier")}


# ---------------------------------
# Full config.yaml -> resolved dict
# ---------------------------------

def _read_config_yaml(config_path: str | os.PathLike = "config.yaml") -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _production_info(raw: dict) -> Tuple[str, str]:
    prod = raw.get("production_information") or {}
    line = prod.get("line")
    grade = prod.get("grade")
    if not line or not grade:
        raise ValueError(
            "config.yaml: `production_information.line` and `.grade` are required."
        )
    return line, str(grade)


def _checkpoint_root(raw: dict, config_path: str | os.PathLike) -> str:
    root = raw.get("checkpoint_root")
    if not isinstance(root, str) or not root.strip():
        raise ValueError(
            f"{config_path}: top-level `checkpoint_root:` is required "
            "and must be the absolute path all checkpoint paths are anchored to."
        )
    return root.strip()


def resolve_from_file(
    config_path: str | os.PathLike = "config.yaml",
    section: str = "defect_detection",
) -> dict:
    """Load a config.yaml and resolve the profile for its (line, grade).

    `section` selects what shape is returned:

      - "defect_detection" -> dict for Detector
      - "baler_classification" -> dict for BalerClassification Classifier
      - "profile" -> raw resolved profile dict (all fields, no shaping)
    """
    raw = _read_config_yaml(config_path)
    line, grade = _production_info(raw)
    checkpoint_root = _checkpoint_root(raw, config_path)

    resolved = load_profile(line, grade, checkpoint_root)

    if section == "profile":
        return resolved
    if section == "defect_detection":
        return to_defect_detection_config(resolved)
    if section == "baler_classification":
        return to_baler_classification_config(resolved)

    raise ValueError(
        f"Unknown section {section!r}; expected 'defect_detection', "
        "'baler_classification' or 'profile'."
    )
