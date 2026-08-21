"""Profile schema for Grade Selection.

A Profile is the single source of truth for a production (line, grade) combination.
It bundles together:
    - classify/segment/cluster class dictionaries
    - checkpoint paths, image sizes, thresholds for every model stage
    - baler classifier configuration
    - runtime output options (return_mode, show)

A profile is resolved from a single foundation module, `products/<LINE>/_<grade>.py`
(see `profiles.load_profile`). There is no registry or override layer.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Union


# `segmenter` may be either a single-model dict (legacy: classes injected from
# `segment_classes`) or a list of model dicts (multi-checkpoint, each carries
# its own `classes` inline).
SegmenterConfig = Union[Dict[str, Any], List[Dict[str, Any]]]


@dataclass
class Profile:
    """Resolved profile data. Every field is optional so a base can stay minimal."""

    family: str

    # classes (int-keyed: class_id -> entry)
    classify_classes: Optional[Dict[int, Dict[str, Any]]] = None
    dot_classify_classes: Optional[Dict[int, Dict[str, Any]]] = None
    # Only used when `segmenter` is the legacy single-model dict form.
    # For multi-model `segmenter` (List[Dict]), put `classes` inline per entry.
    segment_classes: Optional[Dict[int, Dict[str, Any]]] = None

    # cluster classes (str-keyed: cluster label -> entry with class_id inside)
    cluster_classes: Optional[Dict[str, Dict[str, Any]]] = None

    # defect_detection stages
    bgremover: Optional[Dict[str, Any]] = None
    anomaly_extractor: Optional[Dict[str, Any]] = None
    anomalyclip: Optional[Dict[str, Any]] = None
    classifier: Optional[Dict[str, Any]] = None
    segmenter: Optional[SegmenterConfig] = None
    anomaly_cluster: Optional[Dict[str, Any]] = None
    dot_detector1: Optional[Dict[str, Any]] = None
    dot_detector2: Optional[Dict[str, Any]] = None
    tile_detector: Optional[Dict[str, Any]] = None
    dot_classifier: Optional[Dict[str, Any]] = None
    dot_cluster: Optional[Dict[str, Any]] = None
    dot_confidence_by_side: Optional[Dict[str, float]] = None

    # PatchCore 메모리뱅크 기반 전역 이상점수 검출 ('etc')
    patchcore: Optional[Dict[str, Any]] = None
    # PatchCore 를 side 별로 활성화/비활성화 (미지정 시 활성)
    patchcore_active_by_side: Optional[Dict[str, bool]] = None

    # baler_classification
    baler_classifier: Optional[Dict[str, Any]] = None

    # runtime/output
    return_mode: Optional[str] = None
    show: Optional[Dict[str, Any]] = None

    def to_dict(self) -> dict:
        return asdict(self)
