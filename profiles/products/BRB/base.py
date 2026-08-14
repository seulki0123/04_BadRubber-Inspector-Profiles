from dataclasses import replace

from profiles._schema import Profile
from profiles.products.base import build_profile as _build_base

def build_profile(checkpoint_root: str) -> Profile:
    root = checkpoint_root.rstrip("/")
    base = _build_base(checkpoint_root)
    return replace(
        base,
        family="BR-B",
        baler_classifier={
            "checkpoint": f"{root}/baler/weights/BR-B/br_b_all_paired/best_model.pth",
            "img_size": 224,
            "num_classes": None,
            "class_names": {0: "1", 1: "3"},
            "top_start_ratio": 0.3,
            "bottom_end_ratio": 0.7,
        },
        # patchcore={
        #     "checkpoint": f"{root}/defect/patchcore/weights/BR-B/_intergrated/260615/bank_res256.pt",
        #     "holdout": f"{root}/defect/patchcore/weights/BR-B/_intergrated/260615/holdout_scores_res256.json",
        #     "backbone": f"{root}/defect/patchcore/weights/backbone/res256/wide_resnet50_racm-8234f177.pth",
        #     "threshold": None,
        #     "imgsz": 256,
        # },
        # patchcore_active_by_side={
        #     "side1": True,
        #     "side2": False,
        #     "side3": False,
        #     "side4": False,
        #     "side5": False,
        #     "side6": False,
        # },
    )
