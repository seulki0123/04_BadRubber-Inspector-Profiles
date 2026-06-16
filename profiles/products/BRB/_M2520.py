from dataclasses import replace

from profiles._schema import Profile
from profiles.products.BRB.base import build_profile as _build_base

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
    2: {"description": "wet-brown",    "name": "wet",          "color": None, "pass": False},
}

def build_profile(checkpoint_root: str) -> Profile:
    root = checkpoint_root.rstrip("/")
    base = _build_base(checkpoint_root)
    return replace(
        base,
        classify_classes=_CLASSIFY_CLASSES,
        segment_classes=_SEGMENT_CLASSES,
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
    )
