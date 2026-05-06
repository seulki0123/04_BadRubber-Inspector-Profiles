# Profiles

`DefectDetection`, `BalerClassification`, `Inspector-AIServer` 세 모듈이 공용으로 쓰는 **Grade Selection** 프로필 패키지. 제품 라인 / 그레이드 조합 하나를 고르면, 거기에 필요한 클래스 정의 · 모델 체크포인트 · 임계값 · 출력 옵션이 한 덩어리로 해석된다.

---

## 왜 필요한가

- 이전에는 `classes_*.py`, `cluster_name_*.py`, `config_*.yaml` 같은 파일이 모듈별로 흩뿌려져 있었고, 라인/그레이드를 바꿀 때마다 사람이 직접 파일을 복사·편집해야 했다.
- Profiles 는 **(line, grade) → 프로필 한 덩어리** 매핑을 단일 소유하는 패키지로, 세 모듈이 모두 여기서 import 해서 쓴다.

---

## 디렉토리 구조

```
src/Profiles/
├── pyproject.toml                ← pip install -e . 로 설치 가능
├── README.md
└── profiles/                     ← 파이썬 패키지 (import profiles)
    ├── __init__.py               ← loader (load_profile, resolve_from_file, ...)
    ├── _schema.py                ← Profile dataclass, override 검증
    ├── registry.yaml             ← (line, grade) → base family + overrides
    └── bases/                    ← 파운데이션 프로필들 (build_profile 팩토리)
        ├── ssbr_g2.py
        ├── ssbr_g3.py
        ├── br.py
        └── nbr.py
```

---

## 설치 · import

소비자(consumer) 세 모듈 중 어느 쪽에서든 두 가지 방식으로 연결 가능.

### 1) pip 설치 (권장)

```bash
pip install -e /path/to/src/Profiles
```

이후 어디서나:

```python
from profiles import load_profile, resolve_from_file
```

### 2) sys.path 부트스트랩

설치 없이 같은 레포 안에서 바로 쓰고 싶을 때. 각 모듈의 config 로더 상단에서:

```python
import sys
from pathlib import Path
_PROFILES_ROOT = Path(__file__).resolve().parents[3] / "Profiles"
if str(_PROFILES_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROFILES_ROOT))

from profiles import resolve_from_file
```

> `parents[N]` 의 N 은 consumer 파일 위치 기준으로 맞춘다.

---

## 3-레이어 해석 순서

프로필 하나는 아래 순서로 깊은-병합되어 최종 dict 로 만들어진다 (뒤가 이김).

1. **`bases/<family>.py` 의 `build_profile(checkpoint_root)`** — 파운데이션. SSBR-G3 / SSBR-G2 / BR / NBR 등. 모든 체크포인트 경로는 주입받은 `checkpoint_root` 에 앵커링된다.
2. **`registry.yaml` 의 해당 엔트리 `overrides:`** — 그레이드 단위 미세조정 (예: `M2520` 만 `wet-brown`의 `pass` 를 `false` 로).
3. **프로젝트 `config.yaml` 의 `overrides:`** — 실험/디버그용 일회성 덮어쓰기.

---

## consumer 쪽 `config.yaml` 스키마

`DefectDetection/config.yaml` · `Inspector-AIServer/config.yaml` 공통:

```yaml
# 모든 체크포인트 경로가 앵커링되는 단일 절대경로.
checkpoint_root: /path/to/LG_Chemistry/inspection

production_information:
  line: SSBR             # registry 의 line 키와 매치
  grade: M2520           # registry 의 grade 키와 매치
  # return_mode: segment # (선택) 프로필 기본값을 덮어쓸 때만 지정

defect_detection:
  show: {}               # (선택) 프로필 show 와 deep-merge
  overrides: {}          # (선택) 체크포인트/threshold/classes 미세조정

# Inspector-AIServer 전용
baler_classification:
  overrides: {}
```

### 금지 규칙

- `overrides:` 블록 안에는 **`return_mode` 와 `show` 를 넣을 수 없다.** 각각 `production_information.return_mode`, `defect_detection.show` 전용 경로로만 지정. 로더가 위반 시 `ValueError` 를 던진다.
- classes / cluster_classes 덮어쓸 때 **`class_id` 키(또는 entry 안의 `class_id`)는 불변**. 수정 가능한 필드는 `name / color / pass / description` 뿐.

---

## registry.yaml 쓰는 법

```yaml
profiles:
  - line: SSBR
    grade: F2150
    extends: ssbr_g3           # bases/ssbr_g3.py 를 foundation 으로

  - line: SSBR
    grade: M2520
    extends: ssbr_g3
    overrides:                 # 이 그레이드만 덮어쓰기
      segment_classes:
        2:                     # class_id 2 (= wet-brown)
          pass: false           # pass 만 뒤집음
```

`extends` 는 `bases/<name>.py` 의 파일명(.py 제외)이어야 한다.

---

## Segmenter — 단일 vs 멀티 체크포인트

`segmenter` 필드는 두 가지 형식을 모두 받는다.

### 1) 단일 체크포인트 (레거시, 자동 주입)

`segmenter` 가 dict 면 별도의 `segment_classes` 가 `segmenter["classes"]` 로 자동 주입된다 (기존 동작).

```python
# bases/ssbr_g3.py
_SEGMENT_CLASSES = {
    0: {"description": "other-rubber", "name": "other-rubber", "color": None, "pass": False},
    1: {"description": "wet",          "name": "wet",          "color": None, "pass": False},
}

Profile(
    ...
    segment_classes=_SEGMENT_CLASSES,
    segmenter={
        "checkpoint": f"{root}/.../seg/best.pt",
        "imgsz": 640,
        "threshold": 0.25,
    },
)
```

### 2) 멀티 체크포인트 (list-form)

`segmenter` 가 list 면 각 엔트리가 자기 `classes` 를 인라인으로 들고 있어야 한다. `Segmenter` 는 모델을 순서대로 돌려가며 polygon 을 **공용 `class_polys` 에 클래스 이름 단위로** 쌓는다 (같은 `name` 끼리는 mask union 으로 병합).

각 모델이 **그 클래스를 쓸지 말지** 는:
- `classes` 에서 빼버리거나
- 그 entry 에 `pass: True`

```python
# 모델별 클래스 테이블 — 모델마다 학습된 class_id 가 다를 수 있고,
# `name` 이 같으면 최종 출력에서 동일 클래스로 머지된다.
_SEG_OTHER_RUBBER_CLASSES = {
    0: {"name": "other-rubber", "color": None, "pass": False},
}

_SEG_WET_CLASSES = {
    0: {"name": "other-rubber", "color": None, "pass": False},
    1: {"name": "wet",          "color": None, "pass": False},
}

Profile(
    ...
    segment_classes=None,   # 멀티 모드에서는 사용하지 않음
    segmenter=[
        {
            "checkpoint": f"{root}/.../seg_other_rubber/best.pt",
            "imgsz": 640,
            "threshold": 0.25,
            "classes": _SEG_OTHER_RUBBER_CLASSES,   # other-rubber 만 사용
        },
        {
            "checkpoint": f"{root}/.../seg_wet/best.pt",
            "imgsz": 640,
            "threshold": 0.25,
            "classes": _SEG_WET_CLASSES,            # wet, other-rubber 둘 다 사용
        },
    ],
)
```

### 멀티 모드에서의 override 규칙

- 멀티 모드일 때 `segment_classes` 키로는 override 할 수 없다 (loader 가 `ValueError` 를 던진다).
- 한 entry 의 threshold 같은 걸 손보고 싶으면 `segmenter:` 자체를 list 로 통째로 다시 써서 deep-merge 가 아니라 **replacement** 가 일어나게 한다.

---

## 새 항목 추가

### 새 (line, grade) 추가 — 기존 family 사용

`registry.yaml` 에 한 블록만 추가:

```yaml
  - line: SSBR
    grade: <NEW_GRADE>
    extends: ssbr_g3
```

필요하면 `overrides:` 로 미세조정.

### 새 family 추가 — 완전히 다른 클래스 세트

1. `bases/<family>.py` 생성. `build_profile(checkpoint_root) -> Profile` 를 반드시 export.
2. `registry.yaml` 에 해당 family 를 쓰는 (line, grade) 엔트리 추가.

`bases/ssbr_g3.py` 를 복사해 시작하면 제일 빠르다.

---

## 공용 API

```python
from profiles import (
    load_profile,                     # (line, grade, checkpoint_root, extra_overrides=None) -> dict
    resolve_from_file,                # (config_path, section) -> shaped dict
    to_defect_detection_config,       # Profile dict -> Detector 용 dict
    to_baler_classification_config,   # Profile dict -> BalerClassification 용 dict
    build_runtime_overrides,          # config.yaml raw -> extra_overrides dict
)
```

- **DefectDetection**: `resolve_from_file(path, section="defect_detection")` 하나로 끝.
- **Inspector-AIServer**: `load_profile(...)` 로 resolve 후 `to_defect_detection_config` / `to_baler_classification_config` 로 각각 쪼개서 `Detector` / `BalerClassification.Classifier` 에 주입.

---

## 검증 체크리스트

- `checkpoint_root` 누락 → `ValueError`
- `line, grade` 누락 → `ValueError`
- `overrides:` 안에 `return_mode` / `show` → `ValueError`
- classes 덮어쓰기에 `class_id` 등장 → `ValueError`
- classes 덮어쓰기에 허용 외 필드(`name/color/pass/description` 이외) → `ValueError`
