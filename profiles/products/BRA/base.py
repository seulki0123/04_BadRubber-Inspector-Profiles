from dataclasses import replace

from profiles._schema import Profile
from profiles.products.base import build_profile as _build_base

def build_profile(checkpoint_root: str) -> Profile:
    root = checkpoint_root.rstrip("/")
    base = _build_base(checkpoint_root)
    return replace(
        base,
        family="BR-A_SSBR", # BR-A 는 하얀 고무 1208만 생산하므로, base.py 는 SSBR Grade 생산 기준으로 함
        baler_classifier={
            "checkpoint": f"{root}/baler/weights/SSBR/ssbr_all_paired/best_model.pth",
            "img_size": 224,
            "num_classes": None,
            "class_names": {0: "0", 1: "1", 2: "2"},
        },
        patchcore=None,
        patchcore_active_by_side=None,
    )