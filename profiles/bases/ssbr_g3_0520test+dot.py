"""SSBR-G3 foundation profile.

Covers SSBR grades in the G3 class family (e.g. F2150, M0511).
Grade-level differences live in `registry.yaml` as overrides.
"""
from profiles._schema import Profile


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

    11: {"description": "OK-고무",                         "name": "11_ok_rubber",                             "color": (255, 255, 255), "pass": False},
    12: {"description": "OK-고무-거친",                    "name": "12_ok_rubber_rough",                       "color": (255, 255, 255), "pass": False},
    13: {"description": "OK-날개-파란배경",                "name": "13_ok_wing_blue_bg",                       "color": (255, 255, 255), "pass": False},
    14: {"description": "OK-날개확대샷",                   "name": "14_ok_wing_closeup",                       "color": (255, 255, 255), "pass": False},
    15: {"description": "OK-모서리",                       "name": "15_ok_corner",                             "color": (255, 255, 255), "pass": False},
    16: {"description": "OK-양각",                         "name": "16_ok_embossed",                           "color": (255, 255, 255), "pass": False},
    17: {"description": "OK-얼룩",                         "name": "17_ok_stain",                              "color": (255, 255, 255), "pass": False},
    18: {"description": "OK-은갈치",                       "name": "18_ok_silver",                             "color": (255, 255, 255), "pass": False},
    19: {"description": "OK-테두리",                       "name": "19_ok_edge",                               "color": (255, 255, 255), "pass": False},
    20: {"description": "OK-테두리-검정배경",              "name": "20_ok_edge_black_bg",                      "color": (255, 255, 255), "pass": False},
    21: {"description": "OK-테두리-날개",                  "name": "21_ok_edge_wing",                          "color": (255, 255, 255), "pass": False},
    22: {"description": "OK-테두리-날개웨이브",            "name": "22_ok_edge_wing_wave",                     "color": (255, 255, 255), "pass": False},
    23: {"description": "OK-테두리-노란날개-검정배경",      "name": "23_ok_edge_yellow_wing_black_bg",          "color": (255, 255, 255), "pass": False},
    24: {"description": "OK-테두리-밝은배경",              "name": "24_ok_edge_bright_bg",                     "color": (255, 255, 255), "pass": False},
    25: {"description": "OK-테두리-아래",                  "name": "25_ok_edge_bottom",                        "color": (255, 255, 255), "pass": False},
    26: {"description": "OK-테두리-파란배경",              "name": "26_ok_edge_blue_bg",                       "color": (255, 255, 255), "pass": False},
    27: {"description": "OK-테두리-허연날개-검정배경",      "name": "27_ok_edge_white_wing_black_bg",           "color": (255, 255, 255), "pass": False},
    28: {"description": "OK-허얘",                         "name": "28_ok_white",                              "color": (255, 255, 255), "pass": False},
}


_SEG_OTHER_RUBBER_CLASSES = {
    0: {"description": "other-rubber", "name": "other-rubber", "color": None, "pass": False},
    1: {"description": "wet",          "name": "wet",          "color": None, "pass": False},
    2: {"description": "wet-brown",    "name": "wet",          "color": None, "pass": False},
}

# 신규 체크포인트 (G1+G3/260505+260409): 0/1/2 모두 활성화.
_SEG_ALL_CLASSES = {
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
        family="ssbr_g3",

        cluster_classes=None,
        classify_classes=_CLASSIFY_CLASSES,
        segment_classes=None,  # multi-segmenter mode: classes are inline per entry below
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
        anomaly_cluster=None,
        classifier={
            "checkpoint": f"{root}/defect/classify/weights/SSBR/G3-M1525+M2520/04_01+02+03+dash_260505_Add-Rubber-Wet-OtherRubber_re/weights/best_E20.pt",
            "imgsz": 640,
            "threshold": 0.0,
        },
        segmenter=[
            {
                "checkpoint": f"{root}/defect/segment/weights/SSBR/G1+G3/12_10+11/weights/best.pt",
                "imgsz": 640,
                "threshold": 0.4,
                "classes": _SEG_OTHER_RUBBER_CLASSES,
            },
        ],
        tile_detector={
            "checkpoint": f"{root}/defect/segment/weights/SSBR/G1-F1038+M0511/26_24+25/weights/best.pt",
            "imgsz": 1024,
            "threshold": 0.5,
            "iou_threshold": 0.5,
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
        dot_confidence_by_side={
            "side2": 0.5,
            "side3": 0.5,
            "side4": 0.5,
            "side5": 0.5,
            "side6": 0.5,
        },

        baler_classifier={
            "checkpoint": f"{root}/baler/weights/SSBR/ssbr_all_paired/best_model.pth",
            "img_size": 224,
            "num_classes": None,
            "class_names": {0: "0", 1: "1", 2: "2"},
        },

        return_mode="segment",
        show=_SHOW,
    )
