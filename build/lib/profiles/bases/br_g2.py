"""BR-B-G2 foundation profile.

Reuses the SSBR-G2 profile as-is and only swaps out the `baler_classifier`
for the BR-B baler weights + binary (1/3) class map. If SSBR-G2 ever changes,
BR-B-G2 follows automatically.
"""
from dataclasses import replace

from profiles._schema import Profile
from profiles.bases.ssbr_g2 import build_profile as _build_ssbr_g2


def build_profile(checkpoint_root: str) -> Profile:
    root = checkpoint_root.rstrip("/")
    base = _build_ssbr_g2(checkpoint_root)
    return replace(
        base,
        family="br_g2",
        baler_classifier={
            "checkpoint": f"{root}/baler/weights/BR-B/br_b_all_paired/best_model.pth",
            "img_size": 224,
            "num_classes": None,
            "class_names": {0: "1", 1: "3"},
            "top_start_ratio": 0.3,
            "bottom_end_ratio": 0.7,
        },
    )
