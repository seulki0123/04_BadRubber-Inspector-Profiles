from dataclasses import replace

from profiles._schema import Profile
from profiles.products.BRC.base import build_profile as _build_base

_CLASSIFY_CLASSES = {
    0:  {"description": "NG-누적고무",              "name": "accumulated",        "color": (0, 0, 255),     "pass": False},
    1:  {"description": "NG-누적고무-점",           "name": "accumulated",        "color": (0, 0, 255),     "pass": False},
    2:  {"description": "NG-수분",                  "name": "wet",                "color": (0, 0, 255),     "pass": False},
    3:  {"description": "OK-검정배경-별똥별",        "name": "black-5-star",       "color": (255, 255, 255), "pass": False},
    4:  {"description": "OK-검정배경-부스러기",      "name": "black-3-debris",     "color": (255, 255, 255), "pass": False},
    5:  {"description": "OK-검정배경-선무언가",      "name": "black-1",            "color": (255, 255, 255), "pass": False},
    6:  {"description": "OK-검정배경-흰색무언가",    "name": "black-2",            "color": (255, 255, 255), "pass": False},
    7:  {"description": "OK-고무",                  "name": "rubber",             "color": (255, 255, 255), "pass": False},
    8:  {"description": "OK-고무-모서리",           "name": "rubber-edge1",       "color": (255, 255, 255), "pass": False},
    9:  {"description": "OK-고무-모서리-위",         "name": "rubber-edge-up",     "color": (255, 255, 255), "pass": False},
    10: {"description": "OK-고무-빛과다",           "name": "light1",             "color": (255, 255, 255), "pass": False},
    11: {"description": "OK-고무-찢어진",           "name": "rubber-edge-down",   "color": (255, 255, 255), "pass": False},
    12: {"description": "OK-고무-테두리-뒤에조명",    "name": "rubber-edge-light1", "color": (255, 255, 255), "pass": False},
    13: {"description": "OK-고무-테두리-어둡",       "name": "black-4-edge",       "color": (255, 255, 255), "pass": False},
    14: {"description": "OK-고무모서리",            "name": "rubber-edge2",       "color": (255, 255, 255), "pass": False},
    15: {"description": "OK-고무위조명",            "name": "rubber-edge-light2", "color": (255, 255, 255), "pass": False},
    16: {"description": "OK-날씬및쭈끌고무",        "name": "unformed",           "color": (255, 255, 255), "pass": False},
    17: {"description": "OK-대왕부스러기",          "name": "big-debris",         "color": (255, 255, 255), "pass": False},
    18: {"description": "OK-부스러기",              "name": "small-debris",       "color": (255, 255, 255), "pass": False},
    19: {"description": "OK-부스러기-고무가",        "name": "debris-rubber",      "color": (255, 255, 255), "pass": False},
    20: {"description": "OK-부스러기-레일쪽",        "name": "debris-rail",        "color": (255, 255, 255), "pass": False},
    21: {"description": "OK-실지렁이",              "name": "line-worm",          "color": (255, 255, 255), "pass": False},
    22: {"description": "OK-양각1",                 "name": "dash1",              "color": (255, 255, 255), "pass": False},
    23: {"description": "OK-양각A",                 "name": "dashA",              "color": (255, 255, 255), "pass": False},
    24: {"description": "OK-이미지디비",            "name": "inspector",          "color": (255, 255, 255), "pass": False},
    25: {"description": "OK-조명",                  "name": "light2",             "color": (255, 255, 255), "pass": False},
    26: {"description": "OK-홈",                    "name": "hole",               "color": (255, 255, 255), "pass": False},
}

_CLUSTER_CLASSES = {
    'unknown_under_max_sim':                {"class_id": 100, "name": "unknown",           "color": (255, 255, 255), "pass": True},
    '고무-빛과다':                          {"class_id": 0,   "name": "light",             "color": (255, 255, 255), "pass": True},
    '실지렁이':                             {"class_id": 1,   "name": "line-worm",         "color": (255, 255, 255), "pass": True},
    '검정배경-선무언가':                     {"class_id": 2,   "name": "black-1",           "color": (255, 255, 255), "pass": True},
    '검정배경-흰색무언가':                   {"class_id": 3,   "name": "black-2",           "color": (255, 255, 255), "pass": True},
    '부스러기-고무가':                       {"class_id": 4,   "name": "debris-rubber",     "color": (255, 255, 255), "pass": True},
    'NG-후보-고무':                          {"class_id": 5,   "name": "rubber",            "color": (0, 0, 255),     "pass": False},
    '부스러기-레일쪽':                       {"class_id": 6,   "name": "debris-rail",       "color": (255, 255, 255), "pass": True},
    'NG-후보-고무-모서리-삐쭉':              {"class_id": 7,   "name": "rubber-edge",       "color": (0, 0, 255),     "pass": False},
    'NG-후보-고무-테두리-밝은':              {"class_id": 8,   "name": "rubber-edge-light", "color": (0, 0, 255),     "pass": False},
    '검정배경-부스러기':                     {"class_id": 9,   "name": "black-3-debris",    "color": (255, 255, 255), "pass": True},
    '고무-테두리-어둡':                      {"class_id": 10,  "name": "black-4-edge",      "color": (255, 255, 255), "pass": True},
    '검정배경-별똥별':                       {"class_id": 11,  "name": "black-5-star",      "color": (255, 255, 255), "pass": True},
    '고무-모서리-위':                        {"class_id": 12,  "name": "rubber-edge-up",    "color": (255, 255, 255), "pass": True},
    'NG-후보-고무-모서리-아래':              {"class_id": 13,  "name": "rubber-edge-down",  "color": (0, 0, 255),     "pass": False},
    '점이물쓰레기통-테두리쪽-옆-지렁이같은거': {"class_id": 16, "name": "dot-trash-1",       "color": (255, 255, 255), "pass": True},
    '홈':                                    {"class_id": 17,  "name": "hole",              "color": (255, 255, 255), "pass": True},
    '점이물쓰레기통-테두리쪽-옆모서리':      {"class_id": 18,  "name": "dot-trash-2",       "color": (255, 255, 255), "pass": True},
    '점이물쓰레기통-눈알두개':               {"class_id": 19,  "name": "dot-trash-3",       "color": (255, 255, 255), "pass": True},
    '점이물쓰레기통-허옇다':                 {"class_id": 20,  "name": "dot-trash-4",       "color": (255, 255, 255), "pass": True},
    '점이물쓰레기통-테두리쪽-아래':          {"class_id": 21,  "name": "dot-trash-5",       "color": (255, 255, 255), "pass": True},
    'NG-점이물':                             {"class_id": 22,  "name": "foreign",           "color": (0, 0, 255),     "pass": False},
}

_SEGMENT_CLASSES = {
    0: {"description": "wet", "name": "wet",        "color": None, "pass": False},
    1: {"description": "accumulated", "name": "accumulated",        "color": None, "pass": False},
}

def build_profile(checkpoint_root: str) -> Profile:
    root = checkpoint_root.rstrip("/")
    base = _build_base(checkpoint_root)
    return replace(
        base,
        cluster_classes=_CLUSTER_CLASSES,
        classify_classes=_CLASSIFY_CLASSES,
        segment_classes=_SEGMENT_CLASSES,

        classifier={
            "checkpoint": f"{root}/defect/classify/weights/BR/05_BR-C-1280_hdb-sz1000-sp1-pca32_erasing0.0_E30/weights/best.pt",
            "imgsz": 640,
            "threshold": 0.65,
        },
        segmenter={
            "checkpoint": f"{root}/defect/segment/weights/BR-C/G1/09_07+08/weights/best.pt",
            "imgsz": 640,
            "threshold": 0.25,
        },
        dot_detector1={
            "checkpoint": f"{root}/defect/detect/weights/BR/dot/04-18/best.pt",
            "imgsz": 2048,
            "threshold": 0.3,
        },
        dot_cluster={
            "checkpoints_path": f"{root}/defect/classify/weights/BR/03_BR-dot-add1-2604009.pt",
            "threshold": 0.7,
        },
        tile_detector={
            "checkpoint": f"{root}/defect/segment/weights/BR-C/G1/26_24+25/weights/best.pt",
            "imgsz": 1024,
            "threshold": 0.5,
            "iou_threshold": 0.5,
            "device": None,

            # GUI: overlap 좌우 5%, 상하 0%
            "tile_overlap_x": 0.05,
            "tile_overlap_y": 0.0,

            # GUI: ROI 좌우 10%, 상하 0%
            "roi_left": 0.0,
            "roi_right": 0.0,
            "roi_top": 0.05,
            "roi_bottom": 0.05,

            # GUI: 배경 제거 후 외부 black 채움, margin 0, min_pixel 8
            "bg_color": "black",
            "bg_margin_top": 0,
            "bg_margin_bottom": 0,
            "bg_margin_left": 0,
            "bg_margin_right": 0,
            "bg_min_pixel": 8,
        },
    )
