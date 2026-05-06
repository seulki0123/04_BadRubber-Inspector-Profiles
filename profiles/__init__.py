"""Grade Selection loader.

Given `(line, grade)` from `production_information`, this module resolves the
final configuration in three layers:

    1. bases/<family>.py                  foundation profile (Python dataclass)
    2. registry.yaml entry `overrides`    per-grade tweaks (YAML)
    3. caller-supplied overrides          per-run experiment/debug (YAML)

The resolved dict is then reshaped into what `Detector`, `BalerClassification`
and friends already consume: `classifier.classes`, `segmenter.classes`, etc.
"""
from __future__ import annotations

import importlib
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import yaml

from ._schema import Profile, apply_profile_overrides


_REGISTRY_PATH = Path(__file__).with_name("registry.yaml")


def _load_registry() -> list:
    with open(_REGISTRY_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    entries = data.get("profiles", [])
    if not isinstance(entries, list):
        raise ValueError(f"registry.yaml: 'profiles' must be a list, got {type(entries).__name__}")
    return entries


def _find_registry_entry(line: str, grade: str) -> dict:
    for entry in _load_registry():
        if entry.get("line") == line and str(entry.get("grade")) == str(grade):
            return entry
    raise ValueError(
        f"No profile registered for (line={line!r}, grade={grade!r}). "
        f"Add an entry to {_REGISTRY_PATH}."
    )


def _load_base_profile(family: str, checkpoint_root: str) -> Profile:
    mod_name = f"profiles.bases.{family}"
    try:
        module = importlib.import_module(mod_name)
    except ModuleNotFoundError as e:
        raise ValueError(f"Base profile module not found: {mod_name}") from e
    if not hasattr(module, "build_profile"):
        raise ValueError(
            f"{mod_name} must export `build_profile(checkpoint_root) -> Profile`"
        )
    return module.build_profile(checkpoint_root)


def load_profile(
    line: str,
    grade: str,
    checkpoint_root: str,
    extra_overrides: Optional[dict] = None,
) -> dict:
    """Resolve base + registry overrides + (optional) extra overrides into a dict.

    `checkpoint_root` is injected into the base profile factory so every
    checkpoint path is anchored at a single user-controlled root.

    Returns the Profile as a plain dict (see `Profile.to_dict`).
    """
    if not checkpoint_root:
        raise ValueError("load_profile: `checkpoint_root` must be a non-empty path.")

    entry = _find_registry_entry(line, grade)
    base = _load_base_profile(entry["extends"], checkpoint_root).to_dict()

    resolved = apply_profile_overrides(base, entry.get("overrides"))
    if extra_overrides:
        resolved = apply_profile_overrides(resolved, extra_overrides)

    return resolved


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
                "Define dot-specific classes in the base profile or overrides."
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
    dot_detector1, dot_detector2, dot_cluster, dot_confidence_by_side,
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
        "dot_cluster": shaped.get("dot_cluster"),
        "dot_confidence_by_side": shaped.get("dot_confidence_by_side"),
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


_LEGACY_FIELDS_MSG = (
    "Put `return_mode` under `production_information:` (top-level of config.yaml) "
    "and `show` as a flat `defect_detection.show:` block. The `overrides:` block "
    "is reserved for model/checkpoint/threshold/classes tweaks only."
)


def _reject_legacy_in_overrides(overrides: Optional[dict], source: str) -> None:
    """`return_mode` and `show` have dedicated top-level paths in config.yaml
    (see `_LEGACY_FIELDS_MSG`) and must not appear inside a project's
    `overrides:` block. Registry-level overrides are not subject to this rule.
    """
    if not overrides:
        return
    offenders = [k for k in ("return_mode", "show") if k in overrides]
    if offenders:
        raise ValueError(
            f"{source}: `overrides:` may not contain {offenders}. {_LEGACY_FIELDS_MSG}"
        )


def build_runtime_overrides(raw: dict, section: str = "defect_detection") -> Optional[dict]:
    """Translate a project's raw config.yaml into a flat override dict suitable
    for `load_profile(..., extra_overrides=...)`.

    Rules:
      - `<section>.overrides` is used as-is, except it must NOT contain
        `return_mode` or `show` (those have dedicated paths).
      - `production_information.return_mode` is promoted to `return_mode`.
      - `defect_detection.show` (deep dict) is promoted to `show`.
    """
    sub = raw.get(section) or {}
    overrides = dict(sub.get("overrides") or {})
    _reject_legacy_in_overrides(overrides, f"{section}.overrides")

    prod = raw.get("production_information") or {}
    if prod.get("return_mode") is not None:
        overrides["return_mode"] = prod["return_mode"]

    show = (raw.get("defect_detection") or {}).get("show")
    if isinstance(show, dict) and show:
        overrides["show"] = show

    return overrides or None


def resolve_from_file(
    config_path: str | os.PathLike = "config.yaml",
    section: str = "defect_detection",
) -> dict:
    """Load a config.yaml, resolve the profile for its (line, grade), and apply
    the project-level overrides from that file.

    `section` selects which subtree's overrides apply (and what shape is
    returned):

      - "defect_detection" -> dict for Detector
      - "baler_classification" -> dict for BalerClassification Classifier
      - "profile" -> raw resolved profile dict (all fields, no shaping)
    """
    raw = _read_config_yaml(config_path)
    line, grade = _production_info(raw)
    checkpoint_root = _checkpoint_root(raw, config_path)

    extra = build_runtime_overrides(raw, section=section)
    resolved = load_profile(
        line, grade, checkpoint_root, extra_overrides=extra
    )

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
