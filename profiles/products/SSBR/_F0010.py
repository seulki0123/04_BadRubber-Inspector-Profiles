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
    6:  {"description": "NG-지렁이-구분못하겠어",            "name": "6_ng_worm_unclear",                        "color": (0, 0, 255),     "pass": False},
    7:  {"description": "NG-지렁이-작아",                  "name": "7_ng_worm_small",                          "color": (0, 0, 255),     "pass": False},
    8:  {"description": "NG-지렁이-큰날개가붙어서",          "name": "8_ng_worm_big_wing_attached",              "color": (0, 0, 255),     "pass": False},
    9:  {"description": "NG-지렁이-테두리쪽",               "name": "9_ng_worm_edge",                           "color": (0, 0, 255),     "pass": False},
    10: {"description": "NG-촉촉수분",                     "name": "10_ng_moist_wet",                          "color": (0, 0, 255),     "pass": False},

    11: {"description": "OK-고무",                         "name": "11_ok_rubber",                             "color": (255, 255, 255), "pass": True},
    12: {"description": "OK-고무-거친",                    "name": "12_ok_rubber_rough",                       "color": (255, 255, 255), "pass": True},
    13: {"description": "OK-날개-파란배경",                "name": "13_ok_wing_blue_bg",                       "color": (255, 255, 255), "pass": True},
    14: {"description": "OK-날개확대샷",                   "name": "14_ok_wing_closeup",                       "color": (255, 255, 255), "pass": True},
    15: {"description": "OK-모서리",                       "name": "15_ok_corner",                             "color": (255, 255, 255), "pass": True},
    16: {"description": "OK-양각",                         "name": "16_ok_embossed",                           "color": (255, 255, 255), "pass": True},
    17: {"description": "OK-얼룩",                         "name": "17_ok_stain",                              "color": (255, 255, 255), "pass": True},
    18: {"description": "OK-은갈치",                       "name": "18_ok_silver",                             "color": (255, 255, 255), "pass": True},
    19: {"description": "OK-테두리",                       "name": "19_ok_edge",                               "color": (255, 255, 255), "pass": True},
    20: {"description": "OK-테두리-검정배경",              "name": "20_ok_edge_black_bg",                      "color": (255, 255, 255), "pass": True},
    21: {"description": "OK-테두리-날개",                  "name": "21_ok_edge_wing",                          "color": (255, 255, 255), "pass": True},
    22: {"description": "OK-테두리-날개웨이브",            "name": "22_ok_edge_wing_wave",                     "color": (255, 255, 255), "pass": True},
    23: {"description": "OK-테두리-노란날개-검정배경",      "name": "23_ok_edge_yellow_wing_black_bg",          "color": (255, 255, 255), "pass": True},
    24: {"description": "OK-테두리-밝은배경",              "name": "24_ok_edge_bright_bg",                     "color": (255, 255, 255), "pass": True},
    25: {"description": "OK-테두리-아래",                  "name": "25_ok_edge_bottom",                        "color": (255, 255, 255), "pass": True},
    26: {"description": "OK-테두리-파란배경",              "name": "26_ok_edge_blue_bg",                       "color": (255, 255, 255), "pass": True},
    27: {"description": "OK-테두리-허연날개-검정배경",      "name": "27_ok_edge_white_wing_black_bg",           "color": (255, 255, 255), "pass": True},
    28: {"description": "OK-허얘",                         "name": "28_ok_white",                              "color": (255, 255, 255), "pass": True},
}

_SEG_OTHER_RUBBER_CLASSES = {
    0: {"description": "other-rubber", "name": "other-rubber", "color": None, "pass": False},
    1: {"description": "wet",          "name": "wet",          "color": None, "pass": True},
    2: {"description": "wet-brown",    "name": "wet",          "color": None, "pass": True},
}

# 신규 체크포인트 (G1+G3/260505+260409): 0/1/2 모두 활성화.
_SEG_ALL_CLASSES = {
    0: {"description": "other-rubber", "name": "other-rubber", "color": None, "pass": False},
    1: {"description": "wet",          "name": "wet",          "color": None, "pass": False},
    2: {"description": "wet-brown",    "name": "wet",          "color": None, "pass": False},
}

def build_profile(checkpoint_root: str) -> Profile:
    root = checkpoint_root.rstrip("/")
    base = _build_base(checkpoint_root)
    return replace(
        base,
        classify_classes=_CLASSIFY_CLASSES,
        classifier={
            "checkpoint": f"{root}/defect/classify/weights/SSBR/G3-M1525+M2520/04_01+02+03+dash_260505_Add-Rubber-Wet-OtherRubber_re/weights/best_E20.pt",
            "imgsz": 640,
            "threshold": 0.0,
        },
        segmenter=[
            {
                "checkpoint": f"{root}/defect/segment/weights/SSBR/G1+G3/260409_erasing0.0_E50/weights/best.pt",
                "imgsz": 640,
                "threshold": 0.25,
                "classes": _SEG_OTHER_RUBBER_CLASSES,
            },
            {
                "checkpoint": f"{root}/defect/segment/weights/SSBR/G1+G3/260505+260409/weights/best.pt",
                "imgsz": 640,
                "threshold": 0.25,
                "classes": _SEG_ALL_CLASSES,
            },
        ],
    )
