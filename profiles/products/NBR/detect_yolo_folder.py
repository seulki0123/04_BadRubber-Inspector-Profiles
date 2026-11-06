# -*- coding: utf-8 -*-
"""폴더 안의 모든 이미지를 YOLO 모델로 검출하여 저장하는 스크립트 (기간별 처리, faulty 이미지 개수 제한)

서버 없이 직접 YOLO 모델을 사용하여 불량을 검출합니다.

사용법:
    python detect_yolo_folder.py --base-path <기본경로> --start-date <시작날짜> --end-date <종료날짜> --model <모델경로> --output <출력폴더> --max-faulty <최대장수>
    
예시:
    python detect_yolo_folder.py --base-path "\\gnict_nas\LG_Chemistry_Site\BR-C" --start-date "2026-01-03" --end-date "2026-01-07" --model "model/yolo/nbr/6240/best_model.pt" --output "output" --max-faulty 1000
"""
import argparse
import os
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json
from datetime import datetime, timedelta
import re

try:
    from ultralytics import YOLO
    import torch
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("오류: ultralytics가 설치되지 않았습니다.")
    print("다음 명령으로 설치하세요: pip install ultralytics")
    exit(1)


def parse_date_range(start_date_str: str, end_date_str: str) -> List[str]:
    """시작일과 종료일 사이의 모든 날짜 리스트 반환
    
    Args:
        start_date_str: 시작일 (YYYY-MM-DD 형식)
        end_date_str: 종료일 (YYYY-MM-DD 형식)
    
    Returns:
        날짜 문자열 리스트 (예: ['2026-01-03', '2026-01-04', ...])
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    return dates


def get_all_images(folder_path: str) -> List[str]:
    """폴더 안의 모든 이미지 파일 경로 반환 (labels 폴더 제외)"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
    images = []
    
    for root, dirs, files in os.walk(folder_path):
        # labels 폴더는 탐색에서 제외
        if 'labels' in dirs:
            dirs.remove('labels')
        
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                images.append(os.path.join(root, file))
    
    return sorted(images)


def detect_faulty_spots(
    yolo_model,
    image_path: str,
    conf_threshold: float = 0.1,
    iou_threshold: float = 0.45,
    device = None
) -> Tuple[Optional[np.ndarray], List[Dict], bool]:
    """
    이미지에서 불량 검출
    
    Args:
        yolo_model: YOLO 모델 인스턴스
        image_path: 이미지 경로
        conf_threshold: 신뢰도 임계값
        iou_threshold: IoU 임계값
        
    Returns:
        (annotated_image, detections, has_faulty): 검출된 이미지, 검출 정보 리스트, 불량 여부
    """
    try:
        # 이미지 읽기
        image = cv2.imread(image_path)
        if image is None:
            return None, [], False
        
        # YOLO 추론 수행
        if device is None:
            device = 0 if torch.cuda.is_available() else 'cpu'
        
        results = yolo_model.predict(
            source=image,
            conf=conf_threshold,
            iou=iou_threshold,
            verbose=False,
            device=device,
            task='segment'
        )
        
        if not results or len(results) == 0:
            return image.copy(), [], False
        
        result = results[0]
        detections = []
        has_faulty = False
        
        # 검출 결과 처리
        if result.boxes is not None and len(result.boxes) > 0:
            has_faulty = True
            annotated_image = result.plot()
            
            # 검출 정보 추출
            boxes = result.boxes
            class_names = yolo_model.names if hasattr(yolo_model, 'names') else {}
            
            for i in range(len(boxes)):
                box = boxes[i]
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].cpu().numpy()
                
                detection = {
                    "class": cls,
                    "class_name": class_names.get(cls, f"class_{cls}"),
                    "confidence": conf,
                    "bbox": {
                        "x1": float(xyxy[0]),
                        "y1": float(xyxy[1]),
                        "x2": float(xyxy[2]),
                        "y2": float(xyxy[3])
                    }
                }
                
                # Segmentation 마스크가 있으면 추가
                if result.masks is not None and i < len(result.masks.data):
                    mask = result.masks.data[i].cpu().numpy()
                    detection["has_mask"] = True
                else:
                    detection["has_mask"] = False
                
                detections.append(detection)
        else:
            annotated_image = image.copy()
        
        return annotated_image, detections, has_faulty
        
    except Exception as e:
        print(f"  [오류] 검출 중 예외 발생: {e}")
        return None, [], False


def save_detected_image(
    annotated_image: np.ndarray,
    output_path: str,
    width: int = 512,
    height: int = 620,
    quality: int = 60,
    maintain_aspect_ratio: bool = True
) -> bool:
    """검출된 이미지를 지정된 크기와 압축률로 저장
    
    Args:
        annotated_image: 검출 결과가 그려진 이미지
        output_path: 저장 경로
        width: 저장할 이미지 너비 (기본: 512)
        height: 저장할 이미지 높이 (기본: 620)
        quality: JPEG 압축률 (0-100)
        maintain_aspect_ratio: 원본 비율 유지 여부 (기본: True)
        
    Returns:
        저장 성공 여부
    """
    try:
        # 원본 이미지 크기
        orig_h, orig_w = annotated_image.shape[:2]
        orig_aspect = orig_w / orig_h
        
        if maintain_aspect_ratio:
            # 원본 비율 유지하면서 리사이즈
            target_aspect = width / height
            
            if orig_aspect > target_aspect:
                # 원본이 더 넓음: 너비 기준으로 리사이즈
                new_width = width
                new_height = int(width / orig_aspect)
            else:
                # 원본이 더 높음: 높이 기준으로 리사이즈
                new_height = height
                new_width = int(height * orig_aspect)
            
            resized_image = cv2.resize(annotated_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        else:
            # 고정 크기로 리사이즈 (비율 무시)
            resized_image = cv2.resize(annotated_image, (width, height), interpolation=cv2.INTER_AREA)
        
        # 디렉토리 생성
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 압축률로 저장
        success = cv2.imwrite(output_path, resized_image, [cv2.IMWRITE_JPEG_QUALITY, quality])
        
        return success and os.path.exists(output_path)
    except Exception as e:
        print(f"  [오류] 이미지 저장 실패: {e}")
        return False


def save_metadata(
    result: Dict,
    output_dir: str,
    filename: str,
    date_folder: str = None
) -> Optional[str]:
    """각 이미지의 메타데이터를 개별 JSON 파일로 저장
    
    Args:
        result: 처리 결과 딕셔너리
        output_dir: 출력 기본 디렉토리
        filename: 이미지 파일명
        date_folder: 날짜 폴더명 (예: "2026-01-03")
    
    Returns:
        메타데이터 파일 경로 또는 None
    """
    try:
        # 메타데이터 폴더 생성 (날짜별 폴더 구조 유지)
        if date_folder:
            meta_dir = os.path.join(output_dir, date_folder, "meta")
        else:
            meta_dir = os.path.join(output_dir, "meta")
        os.makedirs(meta_dir, exist_ok=True)
        
        # 파일명 생성 (원본 파일명 기반, 타임스탬프 없이)
        name_without_ext = os.path.splitext(filename)[0]
        meta_filename = f"{name_without_ext}.json"
        meta_path = os.path.join(meta_dir, meta_filename)
        
        # 메타데이터 저장
        metadata = {
            "image_path": result["image_path"],
            "filename": result["filename"],
            "faulty_detected": result["faulty_detected"],
            "detection_count": result["detection_count"],
            "detections": result["detections"],
            "saved_path": result.get("saved_path"),
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "skipped": result.get("skipped", False)
        }
        
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return os.path.abspath(meta_path)
    except Exception as e:
        print(f"  [오류] 메타데이터 저장 실패: {e}")
        return None


def process_image(
    yolo_model,
    image_path: str,
    output_dir: str,
    conf_threshold: float,
    iou_threshold: float,
    width: int,
    height: int,
    quality: int,
    device = None,
    maintain_aspect_ratio: bool = True,
    date_folder: str = None,
    faulty_count: int = 0,
    max_faulty: int = 1000,
    save_faulty_image: bool = True
) -> Dict:
    """이미지 하나를 처리
    
    Args:
        date_folder: 날짜 폴더명 (예: "2026-01-03")
        faulty_count: 현재까지 저장된 faulty 이미지 개수
        max_faulty: 최대 faulty 이미지 개수
        save_faulty_image: faulty 이미지 저장 여부 (False면 메타데이터만)
    
    Returns:
        처리 결과 딕셔너리
    """
    filename = os.path.basename(image_path)
    result = {
        "image_path": image_path,
        "filename": filename,
        "faulty_detected": False,
        "detection_count": 0,
        "detections": [],
        "saved_path": None,
        "error": None,
        "skipped": False,
        "meta_path": None
    }
    
    # YOLO 검출 수행
    annotated_image, detections, has_faulty = detect_faulty_spots(
        yolo_model,
        image_path,
        conf_threshold,
        iou_threshold,
        device
    )
    
    if annotated_image is None:
        result["error"] = "이미지 읽기 또는 검출 실패"
        # 메타데이터는 저장
        save_metadata(result, output_dir, filename, date_folder)
        return result
    
    result["faulty_detected"] = has_faulty
    result["detection_count"] = len(detections)
    result["detections"] = detections
    
    # faulty 이미지 저장 여부 결정
    should_save_faulty = False
    if has_faulty and save_faulty_image:
        if faulty_count < max_faulty:
            should_save_faulty = True
    
    # faulty 이미지 저장
    if should_save_faulty:
        # 날짜별 폴더 구조 유지
        if date_folder:
            faulty_dir = os.path.join(output_dir, date_folder, "faulty_img")
        else:
            faulty_dir = os.path.join(output_dir, "faulty_img")
        
        os.makedirs(faulty_dir, exist_ok=True)
        
        # 파일명 생성
        name_without_ext = os.path.splitext(filename)[0]
        output_filename = f"{name_without_ext}_detected.jpg"
        output_path = os.path.join(faulty_dir, output_filename)
        
        # 검출된 이미지 저장
        success = save_detected_image(annotated_image, output_path, width, height, quality, maintain_aspect_ratio)
        
        if success:
            result["saved_path"] = os.path.abspath(output_path)
        else:
            result["error"] = "이미지 저장 실패"
    
    # 메타데이터는 항상 저장
    meta_path = save_metadata(result, output_dir, filename, date_folder)
    if meta_path:
        result["meta_path"] = meta_path
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="폴더 안의 모든 이미지를 YOLO 모델로 검출하여 저장 (기간별 처리)"
    )
    parser.add_argument(
        "--base-path",
        type=str,
        required=True,
        help="기본 경로 (예: \\\\gnict_nas\\LG_Chemistry_Site\\BR-C)"
    )
    parser.add_argument(
        "--start-date",
        type=str,
        required=True,
        help="시작 날짜 (YYYY-MM-DD 형식, 예: 2026-01-03)"
    )
    parser.add_argument(
        "--end-date",
        type=str,
        required=True,
        help="종료 날짜 (YYYY-MM-DD 형식, 예: 2026-01-07)"
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="YOLO 모델 파일 경로 (.pt 파일)"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="출력 기본 폴더 경로"
    )
    parser.add_argument(
        "--max-faulty",
        type=int,
        default=1000,
        help="최대 faulty 이미지 저장 개수 (기본: 1000)"
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.1,
        help="신뢰도 임계값 (기본: 0.1)"
    )
    parser.add_argument(
        "--iou",
        type=float,
        default=0.45,
        help="IoU 임계값 (기본: 0.45)"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=512,
        help="저장할 이미지 너비 (기본: 512)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=620,
        help="저장할 이미지 높이 (기본: 620)"
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=60,
        help="JPEG 압축률 0-100 (기본: 60)"
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="사용할 디바이스 (0: GPU, 'cpu': CPU, None: 자동 선택)"
    )
    
    args = parser.parse_args()
    
    # 날짜 범위 파싱
    try:
        date_list = parse_date_range(args.start_date, args.end_date)
    except ValueError as e:
        print(f"[오류] 날짜 형식 오류: {e}")
        print("날짜는 YYYY-MM-DD 형식이어야 합니다.")
        return
    
    # YOLO 모델 로드
    if not os.path.exists(args.model):
        print(f"[오류] 모델 파일을 찾을 수 없습니다: {args.model}")
        return
    
    print("="*60)
    print("YOLO 폴더 검출 스크립트 (기간별 처리)")
    print("="*60)
    print(f"기본 경로: {args.base_path}")
    print(f"기간: {args.start_date} ~ {args.end_date} ({len(date_list)}일)")
    print(f"모델: {args.model}")
    print(f"출력 폴더: {args.output}")
    print(f"최대 faulty 이미지: {args.max_faulty}장")
    print(f"이미지 크기: {args.width}x{args.height}")
    print()
    
    print("[정보] YOLO 모델 로드 중...")
    try:
        yolo_model = YOLO(args.model)
        
        # 디바이스 설정
        if args.device is None:
            device = 0 if torch.cuda.is_available() else 'cpu'
        else:
            device = args.device if args.device == 'cpu' else int(args.device)
        
        if device != 'cpu' and torch.cuda.is_available():
            print(f"[정보] GPU 사용: {torch.cuda.get_device_name(device)}")
        else:
            print(f"[정보] CPU 사용")
        
        print(f"[정보] 모델 로드 완료: {args.model}")
    except Exception as e:
        print(f"[오류] 모델 로드 실패: {e}")
        return
    
    # 출력 기본 폴더 생성
    os.makedirs(args.output, exist_ok=True)
    
    # 전역 카운터
    total_faulty_count = 0
    total_processed = 0
    total_faulty_detected = 0
    
    # 날짜별 처리
    for date_str in date_list:
        date_folder_path = os.path.join(args.base_path, date_str)
        
        # 빈 날짜 건너뛰기
        if not os.path.exists(date_folder_path):
            print(f"\n[정보] 폴더가 없습니다 (건너뜀): {date_folder_path}")
            continue
        
        # 폴더가 비어있는지 확인
        try:
            if not os.listdir(date_folder_path):
                print(f"\n[정보] 폴더가 비어있습니다 (건너뜀): {date_folder_path}")
                continue
        except Exception:
            print(f"\n[정보] 폴더 접근 실패 (건너뜀): {date_folder_path}")
            continue
        
        print(f"\n{'='*60}")
        print(f"[{date_str}] 처리 시작")
        print(f"{'='*60}")
        
        # 날짜별 출력 폴더 생성 (원본 구조 유지)
        date_output_path = os.path.join(args.output, date_str)
        os.makedirs(date_output_path, exist_ok=True)
        
        # 이미지 파일 찾기
        all_images = get_all_images(date_folder_path)
        print(f"[{date_str}] {len(all_images)}개 이미지 발견")
        
        if len(all_images) == 0:
            print(f"[{date_str}] 이미지가 없습니다. 건너뜁니다.")
            continue
        
        # 이미지 처리
        date_faulty_count = 0
        date_processed = 0
        date_faulty_detected = 0
        
        # faulty 이미지 저장 여부 결정
        save_faulty = (total_faulty_count < args.max_faulty)
        
        if not save_faulty:
            print(f"[{date_str}] 최대 faulty 이미지 개수 도달 ({args.max_faulty}장). 메타데이터만 생성합니다.")
        
        for i, image_path in enumerate(all_images, 1):
            if i % 100 == 0 or i == len(all_images):
                print(f"[{date_str}] [{i}/{len(all_images)}] 처리 중... (faulty 저장: {date_faulty_count}/{args.max_faulty}, 누적: {total_faulty_count}/{args.max_faulty})")
            
            result = process_image(
                yolo_model,
                image_path,
                args.output,
                args.conf,
                args.iou,
                args.width,
                args.height,
                args.quality,
                device=device,
                maintain_aspect_ratio=True,
                date_folder=date_str,
                faulty_count=total_faulty_count,
                max_faulty=args.max_faulty,
                save_faulty_image=save_faulty
            )
            
            date_processed += 1
            total_processed += 1
            
            if result.get("faulty_detected"):
                date_faulty_detected += 1
                total_faulty_detected += 1
                
                if result.get("saved_path"):
                    date_faulty_count += 1
                    total_faulty_count += 1
        
        print(f"\n[{date_str}] 완료:")
        print(f"  처리된 이미지: {date_processed}개")
        print(f"  불량 검출: {date_faulty_detected}개")
        print(f"  저장된 faulty 이미지: {date_faulty_count}개")
        print(f"  누적 faulty 이미지: {total_faulty_count}/{args.max_faulty}장")
        print(f"  저장 위치: {date_output_path}")
    
    # 전체 결과 요약
    print("\n" + "="*60)
    print("전체 처리 완료")
    print("="*60)
    print(f"처리 기간: {args.start_date} ~ {args.end_date}")
    print(f"총 처리된 이미지: {total_processed}개")
    print(f"총 불량 검출: {total_faulty_detected}개")
    print(f"총 저장된 faulty 이미지: {total_faulty_count}/{args.max_faulty}장")
    print(f"\n출력 폴더: {args.output}")
    print("\n날짜별 폴더 구조:")
    for date_str in date_list:
        date_output = os.path.join(args.output, date_str)
        if os.path.exists(date_output):
            print(f"  {date_str}/")
            print(f"    - faulty_img/")
            print(f"    - meta/")


if __name__ == "__main__":
    main()
