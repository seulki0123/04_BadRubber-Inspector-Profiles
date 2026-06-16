from profiles._schema import Profile

_SHOW = {
    "anomaly_map": False,
    "anomaly_score": False,
    "foreground": False,
    "anomaly_regions_polygon": False,
    "anomaly_regions_bbox": False,
    "segmentation_regions_polygon": False,
    "segmentation_regions_bbox": True,
    "patchcore": True,
    "show_pass_classes": False,
}

def build_profile(checkpoint_root: str) -> Profile:
    root = checkpoint_root.rstrip("/")
    return Profile(
        family="base",
        bgremover={
            "checkpoint": f"{root}/defect/rmbg/weights/_intergrated/full-line/20260309/weights/best.pt",
            "imgsz": 672,
        },
        anomalyclip={
            "checkpoint": f"{root}/defect/anomaly/weights/9_12_4_mvtec+(BR-A_1208)+(BR-B_F3626E)+(BR-C_1280+GNDn5)+(NBR-6230)+(SSBR-F1038+F1810+F0010+M0511+M1525+M2520+F3626Y+2550(H)+F2150+F2743)/epoch_15.pth",
            "imgsz": 512,
            "threshold": 0.0,
            "min_area": 3000,
        },
        return_mode="segment",
        show=_SHOW,
    )
