from dataclasses import replace

from profiles._schema import Profile
from profiles.products.BRB.base import build_profile as _build_base

_CLUSTER_CLASSES = {
    'unknown_under_max_sim': {"class_id": 100, "name": "unknown", "color": (255, 255, 255), "pass": True},

    # =========================
    # NG CLASSES
    # =========================
    'NG-Side-2+3-수분-선명':                          {"class_id": 0,  "name": "ng-side23-moist-clear",             "color": (0, 0, 255), "pass": False},
    'NG-Side-2+3-수분-흐릿':                          {"class_id": 1,  "name": "ng-side23-moist-blur",              "color": (0, 0, 255), "pass": False},
    'NG-눌림':                                        {"class_id": 2,  "name": "ng-pressed",                        "color": (0, 0, 255), "pass": False},
    'NG-부스러기-갈색고무-이상해':                    {"class_id": 3,  "name": "ng-debris-brown-rubber-weird",      "color": (0, 0, 255), "pass": False},

    'NG-불량아닌클래스인데훔쳐가--긴지렁이-고무전체': {"class_id": 4,  "name": "ng-steal-longworm-fullrubber",      "color": (0, 0, 255), "pass": False},
    'NG-불량아닌클래스인데훔쳐가--긴지렁이-파마':     {"class_id": 5,  "name": "ng-steal-longworm-perm",            "color": (0, 0, 255), "pass": False},
    'NG-불량아닌클래스인데훔쳐가--지진났다':          {"class_id": 6,  "name": "ng-steal-shaky",                    "color": (0, 0, 255), "pass": False},
    'NG-불량아닌클래스인데훔쳐가--테두리-그냥밝아':   {"class_id": 7,  "name": "ng-steal-edge-light",               "color": (0, 0, 255), "pass": False},
    'NG-불량아닌클래스인데훔쳐가--테두리-뭐아닌데':   {"class_id": 8,  "name": "ng-steal-edge-nothing",             "color": (0, 0, 255), "pass": False},

    'NG-수분-긴지렁이랑있어-왕커':                    {"class_id": 9,  "name": "ng-moist-longworm-big",             "color": (0, 0, 255), "pass": False},
    'NG-수분-노란색-밝아':                            {"class_id": 10, "name": "ng-moist-yellow-light",             "color": (0, 0, 255), "pass": False},
    'NG-수분-크고-선명하고-테두리':                   {"class_id": 11, "name": "ng-moist-big-clear-edge",           "color": (0, 0, 255), "pass": False},
    'NG-수분-크고-선명하고-테두리-매우밝아':          {"class_id": 12, "name": "ng-moist-big-clear-edge-verylight", "color": (0, 0, 255), "pass": False},
    'NG-수분-테두리쪽-매우밝아':                      {"class_id": 13, "name": "ng-moist-edge-verylight",           "color": (0, 0, 255), "pass": False},
    'NG-수분-허연고무':                               {"class_id": 14, "name": "ng-moist-white-rubber",             "color": (0, 0, 255), "pass": False},
    'NG-수분-황토고무':                               {"class_id": 15, "name": "ng-moist-yellow-rubber",            "color": (0, 0, 255), "pass": False},

    # 기존 worm 클래스들이 현재는 하나로 합쳐짐
    'NG-지렁이':                                      {"class_id": 16, "name": "ng-worm",                           "color": (0, 0, 255), "pass": False},

    # =========================
    # PASS CLASSES
    # =========================
    'Side-2+3_검정배경-날개':                         {"class_id": 17, "name": "side23-black-wing",                 "color": (255, 255, 255), "pass": True},
    'Side-2+3_고무-흐리고-수분이조금있고':            {"class_id": 18, "name": "side23-rubber-moist-blur",          "color": (255, 255, 255), "pass": True},
    'Side-2+3_하얀배경-날개':                         {"class_id": 19, "name": "side23-white-wing",                 "color": (255, 255, 255), "pass": True},

    '고무-어두워':                                    {"class_id": 20, "name": "rubber-dark",                       "color": (255, 255, 255), "pass": True},
    '그냥고무+부스러기등등':                          {"class_id": 21, "name": "rubber-debris-mixed",               "color": (255, 255, 255), "pass": True},

    '부스러기-갈색고무':                              {"class_id": 22, "name": "debris-brown-rubber",               "color": (255, 255, 255), "pass": True},
    '부스러기-갈색고무-딱한개':                       {"class_id": 23, "name": "debris-brown-rubber-one",           "color": (255, 255, 255), "pass": True},
    '부스러기-황토고무':                              {"class_id": 24, "name": "debris-yellow-rubber",              "color": (255, 255, 255), "pass": True},

    '수분-부스러기섞인-부스러기':                     {"class_id": 25, "name": "moist-debris-mixed",                "color": (255, 255, 255), "pass": True},

    '짝대기':                                         {"class_id": 26, "name": "bar-line",                          "color": (255, 255, 255), "pass": True},

    '크랙':                                           {"class_id": 27, "name": "crack",                             "color": (255, 255, 255), "pass": True},
    '크랙-Side':                                      {"class_id": 28, "name": "crack-side",                        "color": (255, 255, 255), "pass": True},

    '테두리-삐쭉날개':                                {"class_id": 29, "name": "edge-sharp-wing",                   "color": (255, 255, 255), "pass": True},
    '테두리-파란배경-스트라이프':                     {"class_id": 30, "name": "edge-blue-stripe",                  "color": (255, 255, 255), "pass": True},

    '파란색':                                         {"class_id": 31, "name": "blue",                              "color": (255, 255, 255), "pass": True},
    '파란색-고무조금보여':                            {"class_id": 32, "name": "blue-rubber-small",                 "color": (255, 255, 255), "pass": True},
    '파란색-날개보여':                                {"class_id": 33, "name": "blue-wing",                         "color": (255, 255, 255), "pass": True},
    '파란색-날개보여-매우삐쭉':                       {"class_id": 34, "name": "blue-wing-sharp",                   "color": (255, 255, 255), "pass": True},

    '하얀':                                           {"class_id": 35, "name": "white-object",                      "color": (255, 255, 255), "pass": True},

    '후_NBR에서가져온거-검정-쓰레기':                 {"class_id": 36, "name": "after-nbr-black-trash",             "color": (255, 255, 255), "pass": True},
}

_SEGMENT_CLASSES = {
    0: {"description": "other-rubber", "name": "other-rubber", "color": None, "pass": False},
    1: {"description": "wet",          "name": "wet",          "color": None, "pass": False},
    2: {"description": "wet-brown",    "name": "wet",          "color": None, "pass": True},
}

def build_profile(checkpoint_root: str) -> Profile:
    root = checkpoint_root.rstrip("/")
    base = _build_base(checkpoint_root)
    return replace(
        base,
        cluster_classes=_CLUSTER_CLASSES,
        segment_classes=_SEGMENT_CLASSES,
        anomaly_cluster={
            "checkpoints_path": f"{root}/defect/classify/weights/SSBR/G1-F0010+F1038+F1810+M0511/DINOv2_(F0010+F1038+F1810+M0511).pt",
            "threshold": 0.2,
        },
        segmenter={
            "checkpoint": f"{root}/defect/segment/weights/SSBR/G1+G3/260409_erasing0.0_E50/weights/best.pt",
            "imgsz": 640,
            "threshold": 0.25,
        },
    )