"""SSBR-G2 foundation profile.

Covers SSBR grades in the G2 class family (e.g. F3626Y, 2550H).
"""
from profiles._schema import Profile


_CLUSTER_CLASSES = {
    # NG - debris
    'NG-파우더':                    {"class_id": 0,  "name":"wet2",             "color": (0,0,255),       "pass": False},
    'NG-파우더-작은편':             {"class_id": 1,  "name": "wet2",             "color": (0,0,255),       "pass": False},
    'NG-파우더-수동추가':           {"class_id": 2,  "name": "wet2",             "color": (0,0,255),       "pass": False},

    # NG - wet
    'NG-수분-수동수분':             {"class_id": 3,  "name": "wet2",             "color": (0,0,255),       "pass": False},
    'NG-수분-수동수분-콩알':        {"class_id": 4,  "name": "wet2",             "color": (0,0,255),       "pass": False},
    'NG-수분-수동수분-콩알-비정형': {"class_id": 5,  "name": "wet2",             "color": (0,0,255),       "pass": False},
    'NG-수분-수동추가1':            {"class_id": 6,  "name": "wet2",             "color": (0,0,255),       "pass": False},
    'NG-수분-매우선명':             {"class_id": 7,  "name": "wet2",             "color": (0,0,255),       "pass": False},
    'NG-수분-매우선명-가운데':       {"class_id": 8,  "name": "wet2",             "color": (0,0,255),       "pass": False},
    'NG-수분-고무옆면':             {"class_id": 9,  "name": "wet2",             "color": (0,0,255),       "pass": False},
    'NG-수분-MayDatas':             {"class_id": 10, "name": "wet2",             "color": (0,0,255),       "pass": False},

    # NG - worm
    'NG-지렁이-MayDatas':           {"class_id": 11, "name": "other-rubber",     "color": (0,0,255),       "pass": False},

    # NG - foreign
    'NG-이물-컬러':                 {"class_id": 12, "name": "foreign_X",          "color": (0,0,255),       "pass": False},
    'NG-이물-거뭇거뭇':             {"class_id": 13, "name": "foreign_X",          "color": (0,0,255),       "pass": False},
    'NG-이물-점':                   {"class_id": 14, "name": "foreign_X",          "color": (0,0,255),       "pass": False},

    # OK - rubber
    '고무':                         {"class_id": 15, "name": "rubber",           "color": (255,255,255),   "pass": False},
    '고무-흐림':                    {"class_id": 16, "name": "rubber-blur",      "color": (255,255,255),   "pass": False},
    '고무-흐린':                    {"class_id": 17, "name": "rubber-blur",      "color": (255,255,255),   "pass": False},

    # OK - rubber uncertain
    '고무-애매1':                   {"class_id": 18, "name": "rubber-uncertain", "color": (255,255,255),   "pass": False},
    '고무-애매2':                   {"class_id": 19, "name": "rubber-uncertain", "color": (255,255,255),   "pass": False},
    '고무-애매3':                   {"class_id": 20, "name": "rubber-uncertain", "color": (255,255,255),   "pass": False},

    # OK - edge
    '테두리-보글보글':              {"class_id": 21, "name": "edge-bubble",      "color": (255,255,255),   "pass": False},
    '테두리-고무지렁이':            {"class_id": 22, "name": "edge-worm",        "color": (255,255,255),   "pass": False},
    '테두리-고무약간-남색보여':     {"class_id": 23, "name": "edge-blue",        "color": (255,255,255),   "pass": False},
    '테두리-쓰레기통':              {"class_id": 24, "name": "edge-trash",       "color": (255,255,255),   "pass": False},
    '테두리-여리여리':              {"class_id": 25, "name": "edge-soft",        "color": (255,255,255),   "pass": False},
    '테두리-남색보여':              {"class_id": 26, "name": "edge-blue",        "color": (255,255,255),   "pass": False},

    # OK - white
    '하얀':                         {"class_id": 27, "name": "white",            "color": (255,255,255),   "pass": False},
    '하얀-밝은누리':                {"class_id": 28, "name": "white-bright",     "color": (255,255,255),   "pass": False},
    '하얀-누리끼리':                {"class_id": 29, "name": "white-yellow",     "color": (255,255,255),   "pass": False},
    '하얀-고무테두리':              {"class_id": 30, "name": "white-edge",       "color": (255,255,255),   "pass": False},

    # OK - black
    '검정-쓰레기':                  {"class_id": 31, "name": "black-trash",      "color": (255,255,255),   "pass": False},
    '검정-날개':                    {"class_id": 32, "name": "black-wing",       "color": (255,255,255),   "pass": False},
    '검정-날개조금약간':            {"class_id": 33, "name": "black-wing-s",     "color": (255,255,255),   "pass": False},
    '검정-날개아주약간':            {"class_id": 34, "name": "black-wing-xs",    "color": (255,255,255),   "pass": False},

    # OK - blue
    '파랑':                         {"class_id": 35, "name": "blue",             "color": (255,255,255),   "pass": False},
    '파랑-쓰레기통':                {"class_id": 36, "name": "blue-trash",       "color": (255,255,255),   "pass": False},

    # 기타
    '짝대기':                       {"class_id": 37, "name": "line",             "color": (255,255,255),   "pass": False},
    '고무-일부-쓰레기통':           {"class_id": 38, "name": "rubber-trash",     "color": (255,255,255),   "pass": False},
    '수분-애매1':                   {"class_id": 39, "name": "wet-uncertain",    "color": (255,255,255),   "pass": False},
    '고무-흐린-수분':               {"class_id": 40, "name": "rubber-wet",       "color": (255,255,255),   "pass": False},
}

_SEGMENT_CLASSES = {
    0: {"description": "wet", "name": "wet",        "color": None, "pass": False},
    1: {"description": "accumulated", "name": "other-rubber",  "color": None, "pass": False},
}

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
        family="nbr-0525",

        cluster_classes=_CLUSTER_CLASSES,
        classify_classes=None,
        segment_classes=_SEGMENT_CLASSES,
        dot_classify_classes=None,

        bgremover={
            "checkpoint": f"{root}/defect/rmbg/weights/_intergrated/full-line/rmbg_0625/weights/best.pt",
            "imgsz": 672,
            "use_blur_mask": True,
            "blur_kernel": 501,
            "blur_threshold": 0.60,
            "blur_resize_scale": 0.25,
        },
        anomalyclip={
            "checkpoint": f"{root}/defect/anomaly/weights/9_12_4_mvtec+(BR-A_1208)+(BR-B_F3626E)+(BR-C_1280+GNDn5)+(NBR-6230)+(SSBR-F1038+F1810+F0010+M0511+M1525+M2520+F3626Y+2550(H)+F2150+F2743)/epoch_15.pth",
            "imgsz": 512,
            "threshold": 0.0,
            "min_area": 3000,
        },
        anomaly_cluster={
            "checkpoints_path": f"{root}/defect/classify/weights/NBR/6240/DINOv2_(03_01+02).pt",
            "threshold": 0.2,
        },
        classifier=None,
        segmenter={
            "checkpoint": f"{root}/defect/segment/weights/NBR/G1+G2+G3/1_2875/weights/best.pt",
            "imgsz": 640,
            "threshold": 0.4,
        },
        dot_detector1=None,
        dot_detector2=None,
        tile_detector={
            "checkpoint": f"{root}/defect/segment/weights/NBR/G1+G2+G3/2875_dot/weights/best.pt",
            "imgsz": 1024,
            "threshold": 0.7,
            "iou_threshold": 0.7,
            "device": None,

            # GUI: overlap 좌우 5%, 상하 0%
            "tile_overlap_x": 0.05,
            "tile_overlap_y": 0.0,

            # GUI: ROI 좌우 10%, 상하 0%
            "roi_left": 0.01,
            "roi_right": 0.01,
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
        dot_cluster=None,
        dot_classifier=None,
        dot_confidence_by_side={
            "side2": 0.75,
            "side3": 0.75,
            "side4": 0.75,
            "side5": 0.75,
            "side6": 0.75,
        },

        # patchcore={
        #     "checkpoint": f"{root}/defect/patchcore/weights/NBR/_intergrated/bank_res256.pt",
        #     "holdout": f"{root}/defect/patchcore/weights/NBR/_intergrated/holdout_scores_res256.json",
        #     "backbone": f"{root}/defect/patchcore/weights/backbone/wide_resnet50_racm-8234f177.pth",
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

        baler_classifier={
            "checkpoint": f"{root}/baler/weights/NBR/nbr_all_paired/best_model.pth",
            "img_size": 224,
            "num_classes": None,
            "class_names": {0: "0", 1: "1", 2: "2"},
        },

        return_mode="segment",
        show=_SHOW,
    )
