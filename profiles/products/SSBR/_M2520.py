from dataclasses import replace

from profiles._schema import Profile
from profiles.products.SSBR.base import build_profile as _build_base

_CLASSIFY_CLASSES = {
    0:  {"description": "NG-부스러기-노란고무",              "name": "0_ng_debris_yellow_rubber",                "color": (0, 0, 255),     "pass": False},
    1:  {"description": "NG-부스러기-테두리쪽",              "name": "1_ng_debris_edge",                         "color": (0, 0, 255),     "pass": False},
    2:  {"description": "NG-수분",                         "name": "2_ng_wet",                                 "color": (0, 0, 255),     "pass": False},
    3:  {"description": "NG-수분-M2520-gy",                "name": "3_ng_wet_m2520_gy",                        "color": (0, 0, 255),     "pass": False},
    4:  {"description": "NG-수분-노란고무",                 "name": "4_ng_wet_yellow_rubber",                   "color": (0, 0, 255),     "pass": False},
    5:  {"description": "NG-지렁이-(BR-B+(M2520-gy0505))", "name": "5_ng_worm_br_b_m2520_gy0505",              "color": (0, 0, 255),     "pass": False},
    6:  {"description": "NG-지렁이-테두리쪽",               "name": "6_ng_worm_edge",                           "color": (0, 0, 255),     "pass": False},
    7:  {"description": "NG-촉촉수분",                     "name": "7_ng_moist_wet",                           "color": (0, 0, 255),     "pass": False},

    8:  {"description": "OK-고무",                         "name": "8_ok_rubber",                              "color": (255, 255, 255), "pass": True},
    9:  {"description": "OK-고무-거친",                    "name": "9_ok_rubber_rough",                        "color": (255, 255, 255), "pass": True},
    10: {"description": "OK-날개-파란배경",                "name": "10_ok_wing_blue_bg",                       "color": (255, 255, 255), "pass": True},
    11: {"description": "OK-날개확대샷",                   "name": "11_ok_wing_closeup",                       "color": (255, 255, 255), "pass": True},
    12: {"description": "OK-모서리",                       "name": "12_ok_corner",                             "color": (255, 255, 255), "pass": True},
    13: {"description": "OK-양각",                         "name": "13_ok_embossed",                           "color": (255, 255, 255), "pass": True},
    14: {"description": "OK-얼룩",                         "name": "14_ok_stain",                              "color": (255, 255, 255), "pass": True},
    15: {"description": "OK-은갈치",                       "name": "15_ok_silver",                             "color": (255, 255, 255), "pass": True},
    16: {"description": "OK-테두리",                       "name": "16_ok_edge",                               "color": (255, 255, 255), "pass": True},
    17: {"description": "OK-테두리-검정배경",              "name": "17_ok_edge_black_bg",                      "color": (255, 255, 255), "pass": True},
    18: {"description": "OK-테두리-날개",                  "name": "18_ok_edge_wing",                          "color": (255, 255, 255), "pass": True},
    19: {"description": "OK-테두리-날개웨이브",            "name": "19_ok_edge_wing_wave",                     "color": (255, 255, 255), "pass": True},
    20: {"description": "OK-테두리-노란날개-검정배경",      "name": "20_ok_edge_yellow_wing_black_bg",          "color": (255, 255, 255), "pass": True},
    21: {"description": "OK-테두리-밝은배경",              "name": "21_ok_edge_bright_bg",                     "color": (255, 255, 255), "pass": True},
    22: {"description": "OK-테두리-아래",                  "name": "22_ok_edge_bottom",                        "color": (255, 255, 255), "pass": True},
    23: {"description": "OK-테두리-파란배경",              "name": "23_ok_edge_blue_bg",                       "color": (255, 255, 255), "pass": True},
    24: {"description": "OK-테두리-허연날개-검정배경",      "name": "24_ok_edge_white_wing_black_bg",           "color": (255, 255, 255), "pass": True},
    25: {"description": "OK-허얘",                         "name": "25_ok_white",                              "color": (255, 255, 255), "pass": True},
}

_SEGMENT_CLASSES = {
    0: {"description": "wet",                      "name": "wet",                      "color": None, "pass": False},
    1: {"description": "other-rubber",          "name": "other-rubber",          "color": None, "pass": False},
    2: {"description": "wet-brown",          "name": "wet",                        "color": None, "pass": False},
}

def build_profile(checkpoint_root: str) -> Profile:
    root = checkpoint_root.rstrip("/")
    base = _build_base(checkpoint_root)
    return replace(
        base,
        classify_classes=_CLASSIFY_CLASSES,
        segment_classes=_SEGMENT_CLASSES,
        classifier={
            "checkpoint": f"{root}/defect/classify/weights/SSBR/G3-M1525+M2520/07_05+06_intergrated-other-rubber/weights/best_E027.pt",
            "imgsz": 640,
            "threshold": 0.0,
        },
        segmenter={
            "checkpoint": f"{root}/defect/segment/weights/SSBR/G1+G3/07_05+01-2/weights/best.pt",
            "imgsz": 640,
            "threshold": 0.25,
        },
    )