"""SSBR-G2 foundation profile.

Covers SSBR grades in the G2 class family (e.g. F3626Y, 2550H).
"""
from profiles._schema import Profile


_CLUSTER_CLASSES = {
    'unknown_under_max_sim':                              {"class_id": 100, "name": "unknown",                      "color": (255, 255, 255), "pass": True},

    # NG CLASSES
    'NG-불량아닌클래스인데훔쳐가--테두리-그냥밝아':         {"class_id": 23,  "name": "ng-steal-edge-light",          "color": (0, 0, 255),     "pass": False},
    'NG-수분-허연고무':                                   {"class_id": 24,  "name": "ng-moist-white-rubber",        "color": (0, 0, 255),     "pass": False},
    'NG-불량아닌클래스인데훔쳐가--테두리-뭐아닌데':         {"class_id": 25,  "name": "ng-steal-edge-nothing",        "color": (0, 0, 255),     "pass": False},
    'NG-불량아닌클래스인데훔쳐가--긴지렁이-파마':          {"class_id": 26,  "name": "ng-steal-longworm-perm",       "color": (0, 0, 255),     "pass": False},
    'NG-수분-크고-선명하고-테두리':                        {"class_id": 27,  "name": "ng-moist-big-clear-edge",      "color": (0, 0, 255),     "pass": False},
    'NG-수분-황토고무':                                   {"class_id": 28,  "name": "ng-moist-yellow-rubber",       "color": (0, 0, 255),     "pass": False},
    'NG-수분-긴지렁이랑있어-왕커':                         {"class_id": 29,  "name": "ng-moist-longworm-big",        "color": (0, 0, 255),     "pass": False},
    'NG-수분-테두리쪽-매우밝아':                           {"class_id": 30,  "name": "ng-moist-edge-verylight",      "color": (0, 0, 255),     "pass": False},
    'NG-Side-2+3-수분-흐릿':                              {"class_id": 31,  "name": "ng-side23-moist-blur",         "color": (0, 0, 255),     "pass": False},
    'NG-불량아닌클래스인데훔쳐가--지진났다':               {"class_id": 32,  "name": "ng-steal-shaky",               "color": (0, 0, 255),     "pass": False},
    'NG-지렁이':                                           {"class_id": 33,  "name": "ng-worm",                      "color": (0, 0, 255),     "pass": False},
    'NG-눌림':                                             {"class_id": 34,  "name": "ng-pressed",                   "color": (0, 0, 255),     "pass": False},
    'NG-수분-노란색-밝아':                                 {"class_id": 35,  "name": "ng-moist-yellow-light",        "color": (0, 0, 255),     "pass": False},
    'NG-부스러기-갈색고무-이상해':                         {"class_id": 36,  "name": "ng-debris-brown-rubber",       "color": (0, 0, 255),     "pass": False},
    'NG-불량아닌클래스인데훔쳐가--긴지렁이-고무전체':      {"class_id": 37,  "name": "ng-steal-longworm-fullrubber", "color": (0, 0, 255),     "pass": False},
    'NG-Side-2+3-수분-선명':                              {"class_id": 38,  "name": "ng-side23-moist-clear",        "color": (0, 0, 255),     "pass": False},
    'NG-수분-크고-선명하고-테두리-매우밝아':                {"class_id": 39,  "name": "ng-moist-big-clear-edge-light","color": (0, 0, 255),     "pass": False},

    # PASS CLASSES
    'Side-2+3_고무-흐리고-수분이조금있고':                {"class_id": 40,  "name": "side23-rubber-moist-blur",     "color": (255, 255, 255), "pass": True},
    '그냥고무+부스러기등등':                              {"class_id": 41,  "name": "rubber-debris-mixed",          "color": (255, 255, 255), "pass": True},
    '크랙':                                               {"class_id": 42,  "name": "crack",                        "color": (255, 255, 255), "pass": True},
    '하얀':                                               {"class_id": 43,  "name": "white-object",                 "color": (255, 255, 255), "pass": True},
    '파란색':                                             {"class_id": 44,  "name": "blue",                         "color": (255, 255, 255), "pass": True},
    '크랙-Side':                                          {"class_id": 45,  "name": "crack-side",                   "color": (255, 255, 255), "pass": True},
    '테두리-파란배경-스트라이프':                         {"class_id": 46,  "name": "edge-blue-stripe",             "color": (255, 255, 255), "pass": True},
    '부스러기-갈색고무-딱한개':                           {"class_id": 47,  "name": "debris-brown-rubber-one",      "color": (255, 255, 255), "pass": True},
    '부스러기-황토고무':                                  {"class_id": 48,  "name": "debris-yellow-rubber",         "color": (255, 255, 255), "pass": True},
    '고무-어두워':                                         {"class_id": 49,  "name": "rubber-dark",                  "color": (255, 255, 255), "pass": True},
    '테두리-삐쭉날개':                                     {"class_id": 50,  "name": "edge-sharp-wing",              "color": (255, 255, 255), "pass": True},
    '후_NBR에서가져온거-검정-쓰레기':                      {"class_id": 51,  "name": "after-nbr-black-trash",        "color": (255, 255, 255), "pass": True},
    '파란색-날개보여-매우삐쭉':                            {"class_id": 52,  "name": "blue-wing-sharp",              "color": (255, 255, 255), "pass": True},
    '부스러기-갈색고무':                                   {"class_id": 53,  "name": "debris-brown-rubber",          "color": (255, 255, 255), "pass": True},
    '파란색-고무조금보여':                                 {"class_id": 54,  "name": "blue-rubber-small",            "color": (255, 255, 255), "pass": True},
    '파란색-날개보여':                                     {"class_id": 55,  "name": "blue-wing",                    "color": (255, 255, 255), "pass": True},
    'Side-2+3_검정배경-날개':                              {"class_id": 56,  "name": "side23-black-wing",            "color": (255, 255, 255), "pass": True},
    '짝대기':                                             {"class_id": 57,  "name": "bar-line",                     "color": (255, 255, 255), "pass": True},
    '수분-부스러기섞인-부스러기':                           {"class_id": 58,  "name": "moist-debris-mixed",           "color": (255, 255, 255), "pass": True},
    'Side-2+3_하얀배경-날개':                              {"class_id": 59,  "name": "side23-white-wing",            "color": (255, 255, 255), "pass": True},
}

_SEGMENT_CLASSES = {
    0: {"description": "wet",          "name": "wet",          "color": None, "pass": False},
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

        cluster_classes=_CLUSTER_CLASSES,
        classify_classes=None,
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
        anomaly_cluster={
            "checkpoints_path": f"{root}/defect/classify/weights/SSBR/G1-F0010+F1038+F1810+M0511/DINOv2_(F0010+F1038+F1810+M0511).pt",
            "threshold": 0.2,
        },
        classifier=None,
        segmenter={
            "checkpoint": f"{root}/defect/segment/weights/SSBR/F1038+M0511/03+04_260325_imgsz640_E100_translate0.8/weights/best.pt",
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
