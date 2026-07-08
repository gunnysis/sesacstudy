"""glasses 학습 데이터 오프라인 증강(권장 50장 확보용).

원본 face-*.jpg 에 좌우 반전(mirror)과 밝기 변형을 적용해 폴더에 저장한다. 바운딩 박스는
학습 시 cvpipeline.glasses_detect.detect_glasses_region 이 파일별로 자동 재검출하므로 여기서
좌표를 따로 저장하지 않는다. 증강 파일은 'aug_' 접두사로 구분하며, 재실행 시 원본만 소스로
쓰고 이미 만든 증강본은 건너뛴다(idempotent).

주의: 증강은 소량 데이터의 임시 보강일 뿐, 다양한 '실제' 사진이 가장 좋다.
"""
import os
import sys
import cv2

sys.stdout.reconfigure(encoding="utf-8")

GLASSES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images", "glasses")
TARGET = 50


def _count(files):
    return len([f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))])


def main():
    originals = sorted(
        f for f in os.listdir(GLASSES_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png")) and not f.startswith("aug_")
    )
    print(f"원본 glasses {len(originals)}장")
    made = 0

    # 1) 좌우 반전(mirror) — 얼굴엔 자연스럽고 포즈 다양성을 준다
    for f in originals:
        out = os.path.join(GLASSES_DIR, f"aug_flip_{os.path.splitext(f)[0]}.jpg")
        if os.path.exists(out):
            continue
        img = cv2.imread(os.path.join(GLASSES_DIR, f))
        if img is None:
            continue
        cv2.imwrite(out, cv2.flip(img, 1))
        made += 1

    # 2) 목표(TARGET)까지 밝기 변형으로 채운다
    total = len(originals) + sum(1 for f in os.listdir(GLASSES_DIR) if f.startswith("aug_flip_"))
    for f in originals:
        if total >= TARGET:
            break
        out = os.path.join(GLASSES_DIR, f"aug_bright_{os.path.splitext(f)[0]}.jpg")
        if os.path.exists(out):
            continue
        img = cv2.imread(os.path.join(GLASSES_DIR, f))
        if img is None:
            continue
        cv2.imwrite(out, cv2.convertScaleAbs(img, alpha=1.12, beta=18))  # 살짝 밝게/대비
        made += 1
        total += 1

    final = _count(os.listdir(GLASSES_DIR))
    print(f"증강 {made}장 생성 → 총 glasses {final}장")


if __name__ == "__main__":
    main()
