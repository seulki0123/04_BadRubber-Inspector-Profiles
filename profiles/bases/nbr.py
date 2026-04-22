"""SSBR-G2 foundation profile.

Covers SSBR grades in the G2 class family (e.g. F3626Y, 2550H).
"""
from profiles._schema import Profile


_CLUSTER_CLASSES = {
    # NG - debris
    'NG-파우더':                   {"class_id": 0, "name": "wet2",          "color": (0,0,255), "pass": False},
    'NG-파우더-작은편':            {"class_id": 1, "name": "wet2",          "color": (0,0,255), "pass": False},
    'NG-파우더-수동추가':          {"class_id": 2, "name": "wet2",          "color": (0,0,255), "pass": False},

    # NG - wet
    'NG-수분-수동수분':            {"class_id": 3, "name": "wet2",           "color": (0,0,255), "pass": False},
    'NG-수분-수동수분-콩알':       {"class_id": 4, "name": "wet2",            "color": (0,0,255), "pass": False},
    'NG-수분-수동수분-콩알-비정형': {"class_id": 5, "name": "wet2",            "color": (0,0,255), "pass": False},
    'NG-수분-수동추가1':           {"class_id": 6, "name": "wet2",           "color": (0,0,255), "pass": False},
    'NG-수분-매우선명':            {"class_id": 7, "name": "wet2",           "color": (0,0,255), "pass": False},
    'NG-수분-매우선명-가운데':      {"class_id": 8, "name": "wet2",           "color": (0,0,255), "pass": False},
    'NG-수분-고무옆면':            {"class_id": 9, "name": "wet2",           "color": (0,0,255), "pass": False},

    # NG - worm
    'NG-지렁이':                   {"class_id": 10, "name": "other-rubber",          "color": (0,0,255), "pass": False},
    'NG-지렁이-집나감':            {"class_id": 11, "name": "other-rubber",          "color": (0,0,255), "pass": False},
    'NG-지렁이-하단쪽':            {"class_id": 12, "name": "other-rubber",         "color": (0,0,255), "pass": False},
    'NG-지렁이-하단-매우조금':      {"class_id": 13, "name": "other-rubber",         "color": (0,0,255), "pass": False},

    # NG - foreign
    'NG-이물-컬러':                {"class_id": 14, "name": "foreign",      "color": (0,0,255), "pass": False},
    'NG-이물-거뭇거뭇':            {"class_id": 15, "name": "foreign",       "color": (0,0,255), "pass": False},
    'NG-이물-점':                  {"class_id": 16, "name": "foreign",       "color": (0,0,255), "pass": False},

    # OK - debris
    '부스러기':                    {"class_id": 17, "name": "debris",        "color": (255,255,255), "pass": True},
    '부스러기-왕큰':               {"class_id": 18, "name": "wet2",           "color": (0,0,255), "pass": False},
    '테두리-하단-부스러기':        {"class_id": 19, "name": "edge-debris",   "color": (255,255,255), "pass": True},

    # OK - rubber
    '고무':                        {"class_id": 20, "name": "rubber",        "color": (255,255,255), "pass": True},
    '고무-흐림':                   {"class_id": 21, "name": "rubber-blur",   "color": (255,255,255), "pass": True},
    '고무-흐린':                   {"class_id": 22, "name": "rubber-blur",   "color": (255,255,255), "pass": True},

    # OK - rubber uncertain
    '고무-애매1':                  {"class_id": 23, "name": "rubber-uncertain", "color": (255,255,255), "pass": True},
    '고무-애매2':                  {"class_id": 24, "name": "rubber-uncertain", "color": (255,255,255), "pass": True},
    '고무-애매3':                  {"class_id": 25, "name": "rubber-uncertain", "color": (255,255,255), "pass": True},
    '고무-애매4':                  {"class_id": 26, "name": "rubber-uncertain", "color": (255,255,255), "pass": True},

    # OK - edge
    '테두리-고무약간-남색보여':    {"class_id": 27, "name": "edge-blue",     "color": (255,255,255), "pass": True},
    '테두리-고무-보글보글':        {"class_id": 28, "name": "edge-bubble",   "color": (255,255,255), "pass": True},
    '테두리-고무-여리여리':        {"class_id": 29, "name": "edge-soft",     "color": (255,255,255), "pass": True},
    '테두리-보글보글':             {"class_id": 30, "name": "edge-bubble",   "color": (255,255,255), "pass": True},
    '테두리-남색보여':             {"class_id": 31, "name": "edge-blue",     "color": (255,255,255), "pass": True},
    '테두리-여리여리':             {"class_id": 32, "name": "edge-soft",     "color": (255,255,255), "pass": True},
    '테두리-고무지렁이':           {"class_id": 33, "name": "edge-worm",     "color": (255,255,255), "pass": True},
    '테두리-쓰레기통':             {"class_id": 34, "name": "edge-trash",    "color": (255,255,255), "pass": True},

    # OK - white
    '하얀':                        {"class_id": 35, "name": "white",         "color": (255,255,255), "pass": True},
    '하얀-밝은누리':               {"class_id": 36, "name": "white-bright",  "color": (255,255,255), "pass": True},
    '하얀-누리끼리':               {"class_id": 37, "name": "white-yellow",  "color": (255,255,255), "pass": True},
    '하얀-고무흐릿':               {"class_id": 38, "name": "white-blur",    "color": (255,255,255), "pass": True},
    '하얀-고무테두리':             {"class_id": 39, "name": "white-edge",    "color": (255,255,255), "pass": True},

    # OK - black
    '검정-쓰레기':                 {"class_id": 40, "name": "black-trash",   "color": (255,255,255), "pass": True},
    '검정-날개':                   {"class_id": 41, "name": "black-wing",    "color": (255,255,255), "pass": True},
    '검정-날개조금약간':           {"class_id": 42, "name": "black-wing-s",  "color": (255,255,255), "pass": True},
    '검정-날개아주약간':           {"class_id": 43, "name": "black-wing-xs", "color": (255,255,255), "pass": True},

    # 기타
    '파랑':                        {"class_id": 44, "name": "blue",         "color": (255,255,255), "pass": True},
    '파랑-쓰레기통':               {"class_id": 45, "name": "blue-trash",   "color": (255,255,255), "pass": True},

    '눌림':                        {"class_id": 46, "name": "pressed",      "color": (255,255,255), "pass": True},
    '짝대기':                      {"class_id": 47, "name": "line",         "color": (255,255,255), "pass": True},

    '고무-일부-쓰레기통':          {"class_id": 48, "name": "rubber-trash", "color": (255,255,255), "pass": True},
    '고무와검사장비':              {"class_id": 49, "name": "rubber-device","color": (255,255,255), "pass": True},
    '고무와검사장비레일':          {"class_id": 50, "name": "rubber-rail",  "color": (255,255,255), "pass": True},
    '고무와어두운배경':            {"class_id": 51, "name": "rubber-dark",  "color": (255,255,255), "pass": True},

    '수분-애매1':                  {"class_id": 52, "name": "wet-uncertain","color": (255,255,255), "pass": True},
    '고무-흐린-수분':              {"class_id": 53, "name": "rubber-wet",   "color": (255,255,255), "pass": True},

    '상단까만뭔가':                {"class_id": 54, "name": "unknown-dark", "color": (255,255,255), "pass": True},
    '크랙-지렁이처럼보일만한':     {"class_id": 55, "name": "crack-worm",   "color": (255,255,255), "pass": True},
}

_CLASSIFY_CLASSES = {
    0: {"description": "NG-1-지렁이",        "name": "other-rubber",               "color": (0, 0, 255),     "pass": False},
    1: {"description": "NG-2-이물-블랙",     "name": "foreign",                    "color": (0, 0, 255),     "pass": False},
    2: {"description": "NG-2-이물-컬러",     "name": "foreign",                     "color": (0, 0, 255),     "pass": False},
    3: {"description": "NG-3-수분",          "name": "wet2",                       "color": (0, 0, 255),     "pass": False},
    4: {"description": "고무",               "name": "rubber",                     "color": (255, 255, 255), "pass": True},
    5: {"description": "지렁이-집",          "name": "other-rubber-empty",          "color": (255, 255, 255), "pass": True},
    6: {"description": "짝대기",             "name": "dash",                       "color": (255, 255, 255), "pass": True},
    7: {"description": "하단부스러기",       "name": "debris",                       "color": (255, 255, 255), "pass": True},
}

_SEGMENT_CLASSES = {
    0: {"description": "foreign_black", "name": "foreign",        "color": None, "pass": False},
    1: {"description": "foreign_color", "name": "foreign",        "color": None, "pass": False},
    2: {"description": "other_rubber",  "name": "other_rubber",  "color": None, "pass": False},
    3: {"description": "wet2",           "name": "wet2",           "color": None, "pass": False},
}

_DOT_CLASSIFY_CLASSES = _CLASSIFY_CLASSES

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
        family="nbr",

        cluster_classes=_CLUSTER_CLASSES,
        classify_classes=_CLASSIFY_CLASSES,
        segment_classes=_SEGMENT_CLASSES,
        dot_classify_classes=_DOT_CLASSIFY_CLASSES,

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
        anomaly_cluster={
            "checkpoints_path": f"{root}/defect/classify/weights/NBR/6240+7150/DINOv2_(6240-260124+260214+260215)+(7150-260227+260302)_add-ok.pt",
            "threshold": 0.2,
        },
        classifier={
            "checkpoint": f"{root}/defect/classify/weights/NBR/G1+G2+G3/260320_imgsz640_E100_erasing0.0/weights/best.pt",
            "imgsz": 640,
            "threshold": 0.0,
        },
        segmenter={
            "checkpoint": f"{root}/defect/segment/weights/NBR/G1+G2+G3/260320_imgsz640_E100/weights/best.pt",
            "imgsz": 640,
            "threshold": 0.25,
        },
        dot_detector1={
            "checkpoint": f"{root}/defect/detect/weights/BR/dot/04-18/best.pt",
            "imgsz": 2048,
            "threshold": 0.3,
        },
        dot_detector2=None,
        dot_cluster=None,
        dot_classifier={
            "checkpoint": f"{root}/defect/classify/weights/NBR/G1+G2+G3/260320_imgsz640_E100_erasing0.0/weights/best.pt",
            "imgsz": 640,
            "threshold": 0.0,
        },
        dot_confidence_by_side={
            "side2": 0.6,
            "side3": 0.6,
            "side4": 0.6,
            "side5": 0.6,
            "side6": 0.6,
        },

        baler_classifier={
            "checkpoint": f"{root}/baler/weights/NBR/nbr_all_paired/best_model.pth",
            "img_size": 224,
            "num_classes": None,
            "class_names": {0: "0", 1: "1", 2: "2"},
        },

        return_mode="segment",
        show=_SHOW,
    )
