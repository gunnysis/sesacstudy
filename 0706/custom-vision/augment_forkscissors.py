"""fork·scissors 학습 데이터 오프라인 증강(권장 50장 확보용).

원본 20장에 좌우 반전(mirror)과 밝기 변형을 적용해 태그당 50장을 만든다. glasses 와 달리
fork/scissors 는 regions.py 의 고정 좌표가 정답이므로, 증강 이미지의 박스를 여기서 함께
계산해 YOLO 정규화 사이드카(.txt: `cls cx cy w h`)로 저장한다 — 업로드 시
cvpipeline.images 가 이 사이드카를 읽어 리전을 붙인다.

박스 변환 규칙:
  - 좌우 반전: left' = 1 - left - width (top/width/height 불변)
  - 밝기 변형: 박스 불변

증강 파일은 'aug_' 접두사로 구분하며 재실행 시 이미 만든 것은 건너뛴다(idempotent).
"""
import os
import sys
import cv2

sys.stdout.reconfigure(encoding="utf-8")

from cvpipeline.regions import fork_image_regions, scissors_image_regions

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images")
TARGET = 50


def _write_yolo_sidecar(path_no_ext, left, top, width, height):
    """정규화 [left, top, w, h] 박스를 YOLO(`cls cx cy w h`) 사이드카로 저장한다."""
    cx, cy = left + width / 2, top + height / 2
    with open(path_no_ext + ".txt", "w", encoding="utf-8") as f:
        f.write(f"0 {cx:.6f} {cy:.6f} {width:.6f} {height:.6f}\n")


def augment_tag(folder, region_map):
    """한 태그 폴더를 TARGET 장까지 증강한다(반전 우선, 부족하면 밝기 변형)."""
    dir_path = os.path.join(BASE, folder)
    made = 0
    total = len(region_map)

    # 1) 좌우 반전 — 박스 x 좌표도 함께 반전
    for name, (l, t, w, h) in sorted(region_map.items()):
        if total >= TARGET:
            break
        out_stem = os.path.join(dir_path, f"aug_flip_{name}")
        if os.path.exists(out_stem + ".jpg"):
            total += 1
            continue
        img = cv2.imread(os.path.join(dir_path, name + ".jpg"))
        if img is None:
            continue
        cv2.imwrite(out_stem + ".jpg", cv2.flip(img, 1))
        _write_yolo_sidecar(out_stem, max(0.0, 1.0 - l - w), t, w, h)
        made += 1
        total += 1

    # 2) 밝기 변형 — 박스 불변
    for name, (l, t, w, h) in sorted(region_map.items()):
        if total >= TARGET:
            break
        out_stem = os.path.join(dir_path, f"aug_bright_{name}")
        if os.path.exists(out_stem + ".jpg"):
            total += 1
            continue
        img = cv2.imread(os.path.join(dir_path, name + ".jpg"))
        if img is None:
            continue
        cv2.imwrite(out_stem + ".jpg", cv2.convertScaleAbs(img, alpha=1.12, beta=18))
        _write_yolo_sidecar(out_stem, l, t, w, h)
        made += 1
        total += 1

    print(f"[{folder}] 원본 {len(region_map)}장 + 증강 생성 {made}장 → 총 {total}장")


def main():
    augment_tag("fork", fork_image_regions)
    augment_tag("scissors", scissors_image_regions)


if __name__ == "__main__":
    main()
