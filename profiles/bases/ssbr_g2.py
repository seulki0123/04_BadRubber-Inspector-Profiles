"""SSBR-G2 foundation profile.

Covers SSBR grades in the G2 class family (e.g. F3626Y, 2550H).
"""
from profiles._schema import Profile


_CLASSIFY_CLASSES = {
    0:  {"description": "NG-수분",                  "name": "wet",                  "color": (0, 0, 255),     "pass": False},
    1:  {"description": "NG-수분-테두리쪽",          "name": "wet",                  "color": (0, 0, 255),     "pass": False},
    2:  {"description": "NG-지렁이",                 "name": "other-rubber",         "color": (0, 0, 255),     "pass": False},
    3:  {"description": "NG-지렁이-테두리쪽",        "name": "other-rubber",         "color": (0, 0, 255),     "pass": False},
    4:  {"description": "OK-갈라짐",                 "name": "drain",                "color": (255, 255, 255), "pass": True},
    5:  {"description": "OK-갈라짐-테두리쪽",        "name": "drain-edge",           "color": (255, 255, 255), "pass": True},
    6:  {"description": "OK-검정배경-날개삐쭉",       "name": "black-wings",          "color": (255, 255, 255), "pass": True},
    7:  {"description": "OK-그냥고무",               "name": "rubber",               "color": (255, 255, 255), "pass": True},
    8:  {"description": "OK-양각-밝은",              "name": "dash-light",           "color": (255, 255, 255), "pass": True},
    9:  {"description": "OK-양각-어두운",            "name": "dash-dark",            "color": (255, 255, 255), "pass": True},
    10: {"description": "OK-조명배경-날개삐쭉",      "name": "light-wings",          "color": (255, 255, 255), "pass": True},
    11: {"description": "OK-조명배경-모서리",         "name": "light-edge",           "color": (255, 255, 255), "pass": True},
    12: {"description": "OK-테두리-아래-거의배경",    "name": "edge-bottom-light",    "color": (255, 255, 255), "pass": True},
    13: {"description": "OK-테두리-아래-날개많이",    "name": "edge-bottom-wings",    "color": (255, 255, 255), "pass": True},
    14: {"description": "OK-테두리-아래-날개중간",    "name": "edge-bottom-wings-middle", "color": (255, 255, 255), "pass": True},
    15: {"description": "OK-테두리-옆",              "name": "edge-side",            "color": (255, 255, 255), "pass": True},
    16: {"description": "OK-테두리-튀어나온",        "name": "edge-up",              "color": (255, 255, 255), "pass": True},
}


_SEGMENT_CLASSES = {
    0: {"description": "other-rubber", "name": "other-rubber", "color": None, "pass": False},
    1: {"description": "wet",          "name": "wet",          "color": None, "pass": False},
    2: {"description": "wet-brown",    "name": "wet",          "color": None, "pass": False},
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
        family="ssbr_g2",

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
            "checkpoint": f"{root}/defect/classify/weights/SSBR/G2-F3626Y+2550H/03_01+02/260403_(03_01+02)_erasing0.0_E30/weights/best.pt",
            "imgsz": 640,
            "threshold": 0.0,
        },
        segmenter={
            "checkpoint": f"{root}/defect/segment/weights/SSBR/G2-F3626Y+2550H/260404_erasing0.0_E100/weights/best.pt",
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
