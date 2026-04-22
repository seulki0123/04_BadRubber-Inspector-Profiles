"""SSBR-G3 foundation profile.

Covers SSBR grades in the G3 class family (e.g. F2150, M0511).
Grade-level differences live in `registry.yaml` as overrides.
"""
from profiles._schema import Profile


_CLASSIFY_CLASSES = {
    0:  {"description": "NG-부스러기-노란고무",   "name": "debris",        "color": (0, 0, 255),     "pass": False},
    1:  {"description": "NG-부스러기-테두리쪽",   "name": "debris",        "color": (0, 0, 255),     "pass": False},
    2:  {"description": "NG-수분",              "name": "wet",           "color": (0, 0, 255),     "pass": False},
    3:  {"description": "NG-수분-노란고무",       "name": "wet",           "color": (0, 0, 255),     "pass": False},
    4:  {"description": "NG-지렁이",            "name": "other-rubber",   "color": (0, 0, 255),     "pass": False},
    5:  {"description": "NG-촉촉수분",          "name": "wet",           "color": (0, 0, 255),     "pass": False},
    6:  {"description": "OK-고무",              "name": "rubber",         "color": (255, 255, 255), "pass": True},
    7:  {"description": "OK-고무-거친",         "name": "rubber-rough",   "color": (255, 255, 255), "pass": True},
    8:  {"description": "OK-날개-파란배경",      "name": "wings-blue-bg",  "color": (255, 255, 255), "pass": True},
    9:  {"description": "OK-날개확대샷",        "name": "wings-close",    "color": (255, 255, 255), "pass": True},
    10: {"description": "OK-모서리",            "name": "edge",           "color": (255, 255, 255), "pass": True},
    11: {"description": "OK-양각",              "name": "dash",           "color": (255, 255, 255), "pass": True},
    12: {"description": "OK-얼룩",              "name": "stain",          "color": (255, 255, 255), "pass": True},
    13: {"description": "OK-은갈치",            "name": "silver",         "color": (255, 255, 255), "pass": True},
    14: {"description": "OK-테두리",            "name": "edge",           "color": (255, 255, 255), "pass": True},
    15: {"description": "OK-테두리-검정배경",    "name": "edge-black-bg",  "color": (255, 255, 255), "pass": True},
    16: {"description": "OK-테두리-날개",       "name": "edge-wings",     "color": (255, 255, 255), "pass": True},
    17: {"description": "OK-테두리-날개웨이브",  "name": "edge-wings-wave","color": (255, 255, 255), "pass": True},
    18: {"description": "OK-테두리-노란날개-검정배경", "name": "edge-yellow-wings-black-bg", "color": (255, 255, 255), "pass": True},
    19: {"description": "OK-테두리-밝은배경",    "name": "edge-light-bg",  "color": (255, 255, 255), "pass": True},
    20: {"description": "OK-테두리-아래",       "name": "edge-bottom",    "color": (255, 255, 255), "pass": True},
    21: {"description": "OK-테두리-파란배경",    "name": "edge-blue-bg",   "color": (255, 255, 255), "pass": True},
    22: {"description": "OK-테두리-허연날개-검정배경", "name": "edge-white-wings-black-bg", "color": (255, 255, 255), "pass": True},
    23: {"description": "OK-허얘",              "name": "white",          "color": (255, 255, 255), "pass": True},
}


_SEGMENT_CLASSES = {
    0: {"description": "other-rubber", "name": "other-rubber", "color": None, "pass": False},
    1: {"description": "wet",          "name": "wet",          "color": None, "pass": False},
    2: {"description": "wet-brown",    "name": "wet",          "color": None, "pass": True},
}


_SHOW = {
    "anomaly_map": False,
    "anomaly_score": False,
    "foreground": False,
    "anomaly_regions_polygon": False,
    "anomaly_regions_bbox": False,
    "segmentation_regions_polygon": False,
    "segmentation_regions_bbox": True,
    "show_pass_classes": False,
}


def build_profile(checkpoint_root: str) -> Profile:
    root = checkpoint_root.rstrip("/")
    return Profile(
        family="ssbr_g3",

        cluster_classes=None,
        classify_classes=_CLASSIFY_CLASSES,
        segment_classes=_SEGMENT_CLASSES,
        dot_classify_classes=None,

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
        anomaly_cluster=None,
        classifier={
            "checkpoint": f"{root}/defect/classify/weights/SSBR/G3-M1525+M2520/04_01+02+03+dash_erasing0.0_E30_re/weights/best.pt",
            "imgsz": 640,
            "threshold": 0.0,
        },
        segmenter={
            "checkpoint": f"{root}/defect/segment/weights/SSBR/G1+G3/260409_erasing0.0_E50/weights/best.pt",
            "imgsz": 640,
            "threshold": 0.25,
        },
        dot_detector1=None,
        dot_detector2=None,
        dot_cluster=None,
        dot_classifier=None,

        baler_classifier={
            "checkpoint": f"{root}/baler/weights/SSBR/ssbr_all_paired/best_model.pth",
            "img_size": 224,
            "num_classes": None,
            "class_names": {0: "0", 1: "1", 2: "2"},
        },

        return_mode="segment",
        show=_SHOW,
    )
