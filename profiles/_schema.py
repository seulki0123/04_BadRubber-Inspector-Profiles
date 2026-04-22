"""Profile schema and merge utilities for Grade Selection.

A Profile is the single source of truth for a production (line, grade) combination.
It bundles together:
    - classify/segment/cluster class dictionaries
    - checkpoint paths, image sizes, thresholds for every model stage
    - baler classifier configuration
    - runtime output options (return_mode, show)

Profiles are resolved in three layers (lowest to highest precedence):
    1. `bases/<family>.py`                (foundation, e.g. SSBR-G3)
    2. `registry.yaml` entry `overrides`  (per-grade tweaks)
    3. Project `config.yaml` `overrides`  (per-run experiment/debug tweaks)
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional


CLASSES_OVERRIDABLE_FIELDS = frozenset({"name", "color", "pass", "description"})
CLUSTER_OVERRIDABLE_FIELDS = frozenset({"name", "color", "pass"})


@dataclass
class Profile:
    """Resolved profile data. Every field is optional so a base can stay minimal."""

    family: str

    # classes (int-keyed: class_id -> entry)
    classify_classes: Optional[Dict[int, Dict[str, Any]]] = None
    dot_classify_classes: Optional[Dict[int, Dict[str, Any]]] = None
    segment_classes: Optional[Dict[int, Dict[str, Any]]] = None

    # cluster classes (str-keyed: cluster label -> entry with class_id inside)
    cluster_classes: Optional[Dict[str, Dict[str, Any]]] = None

    # defect_detection stages
    bgremover: Optional[Dict[str, Any]] = None
    anomalyclip: Optional[Dict[str, Any]] = None
    classifier: Optional[Dict[str, Any]] = None
    segmenter: Optional[Dict[str, Any]] = None
    anomaly_cluster: Optional[Dict[str, Any]] = None
    dot_detector1: Optional[Dict[str, Any]] = None
    dot_detector2: Optional[Dict[str, Any]] = None
    dot_classifier: Optional[Dict[str, Any]] = None
    dot_cluster: Optional[Dict[str, Any]] = None
    dot_confidence_by_side: Optional[Dict[str, float]] = None

    # baler_classification
    baler_classifier: Optional[Dict[str, Any]] = None

    # runtime/output
    return_mode: Optional[str] = None
    show: Optional[Dict[str, Any]] = None

    def to_dict(self) -> dict:
        return asdict(self)


def deep_merge(base: Any, overrides: Any) -> Any:
    """Deep-merge two values. Keys present in `overrides` always win.

    Rules:
      - If both are dicts -> recurse per key (keys absent in overrides keep base).
      - Otherwise -> `overrides` replaces `base` (including explicit None to disable).
    """
    if isinstance(base, dict) and isinstance(overrides, dict):
        result = dict(base)
        for k, v in overrides.items():
            if k in result:
                result[k] = deep_merge(result[k], v)
            else:
                result[k] = v
        return result
    return overrides


def validate_classes_override(
    base_classes: Optional[Dict[int, Dict[str, Any]]],
    override_classes: Optional[Dict[int, Dict[str, Any]]],
    section: str,
) -> None:
    """Ensure that an override to an int-keyed classes dict only touches
    `name / color / pass / description` fields of EXISTING class_ids.

    Adding a new class_id, removing one, or touching any other field is rejected.
    """
    if override_classes is None:
        return
    if not isinstance(override_classes, dict):
        raise TypeError(f"{section} override must be a dict, got {type(override_classes).__name__}")
    if base_classes is None:
        raise ValueError(
            f"{section}: cannot override classes because base has none. "
            "Define the classes in the base profile first."
        )

    extra_ids = set(override_classes.keys()) - set(base_classes.keys())
    if extra_ids:
        raise ValueError(
            f"{section}: cannot add new class_ids via override (immutable keys). "
            f"Unknown: {sorted(extra_ids)}"
        )

    for cls_id, entry in override_classes.items():
        if not isinstance(entry, dict):
            raise TypeError(
                f"{section}[{cls_id}] override must be a dict of fields, got {type(entry).__name__}"
            )
        illegal = set(entry.keys()) - CLASSES_OVERRIDABLE_FIELDS
        if illegal:
            raise ValueError(
                f"{section}[{cls_id}]: only {sorted(CLASSES_OVERRIDABLE_FIELDS)} can be overridden, "
                f"got {sorted(illegal)}"
            )


def validate_cluster_override(
    base_classes: Optional[Dict[str, Dict[str, Any]]],
    override_classes: Optional[Dict[str, Dict[str, Any]]],
) -> None:
    """Like `validate_classes_override` but for the str-keyed cluster dict.
    `class_id` lives inside the entry and is therefore immutable.
    """
    if override_classes is None:
        return
    if not isinstance(override_classes, dict):
        raise TypeError(f"cluster_classes override must be a dict, got {type(override_classes).__name__}")
    if base_classes is None:
        raise ValueError(
            "cluster_classes: cannot override because base has none. "
            "Define the classes in the base profile first."
        )

    extra = set(override_classes.keys()) - set(base_classes.keys())
    if extra:
        raise ValueError(
            f"cluster_classes: cannot add new cluster labels via override. "
            f"Unknown: {sorted(extra)}"
        )

    for label, entry in override_classes.items():
        if not isinstance(entry, dict):
            raise TypeError(
                f"cluster_classes[{label}] override must be a dict, got {type(entry).__name__}"
            )
        illegal = set(entry.keys()) - CLUSTER_OVERRIDABLE_FIELDS
        if illegal:
            raise ValueError(
                f"cluster_classes[{label}]: only {sorted(CLUSTER_OVERRIDABLE_FIELDS)} can be "
                f"overridden (class_id is immutable), got {sorted(illegal)}"
            )


def apply_profile_overrides(base: dict, overrides: Optional[dict]) -> dict:
    """Validate overrides against the shape constraints, then deep-merge into base.

    `base` is the dict form of a Profile (as produced by `Profile.to_dict()`).
    `overrides` is a plain dict loaded from YAML (or None/empty).
    """
    if not overrides:
        return dict(base)

    if not isinstance(overrides, dict):
        raise TypeError(f"overrides must be a dict, got {type(overrides).__name__}")

    # Field-shape validation for immutable-key sections
    for section in ("classify_classes", "dot_classify_classes", "segment_classes"):
        if section in overrides:
            validate_classes_override(base.get(section), overrides[section], section)
    if "cluster_classes" in overrides:
        validate_cluster_override(base.get("cluster_classes"), overrides["cluster_classes"])

    # Reject unknown top-level keys (typo-safety)
    known = set(Profile.__dataclass_fields__.keys())
    unknown = set(overrides.keys()) - known
    if unknown:
        raise ValueError(
            f"Unknown override keys: {sorted(unknown)}. Known: {sorted(known)}"
        )

    return deep_merge(base, overrides)
