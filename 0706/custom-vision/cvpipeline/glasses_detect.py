"""OpenCV Haar cascade 로 이미지에서 안경(눈) 영역을 자동 검출.

객체탐지는 이미지마다 '안경만' 감싸는 정밀 박스가 필요하다. 예전에는 얼굴 전체(88%×76%)를
덮는 고정 박스를 써서 모델이 '안경'이 아니라 '얼굴'을 학습했고, 그 결과 안경만 있는 사진에서
검출이 안 됐다. 그래서 안경 대응 눈 검출기로 각 이미지의 눈/안경 영역을 찾아 파일마다
타이트한 박스를 계산한다. 검출 실패 시에만 얼굴 비례/고정 눈라인 박스로 폴백한다.
"""
import os
import cv2

_cascade_dir = cv2.data.haarcascades
_face_cascade = cv2.CascadeClassifier(os.path.join(_cascade_dir, "haarcascade_frontalface_default.xml"))
_eye_glasses_cascade = cv2.CascadeClassifier(os.path.join(_cascade_dir, "haarcascade_eye_tree_eyeglasses.xml"))
_eye_cascade = cv2.CascadeClassifier(os.path.join(_cascade_dir, "haarcascade_eye.xml"))

# 얼굴/눈 검출이 모두 실패했을 때만 쓰는 최후 고정 박스(정면 얼굴 크롭 기준 눈라인)
GLASSES_FALLBACK_REGION = [0.18, 0.30, 0.64, 0.24]  # [left, top, width, height] 정규화(0~1)


def detect_glasses_region(image_path):
    """이미지에서 안경(눈) 영역을 검출해 정규화 [left, top, width, height] 를 반환한다.
    우선순위: 얼굴 안 양쪽 눈 합집합 > 얼굴 비례 눈라인 > 이미지 전체 양쪽 눈 > 고정 폴백."""
    img = cv2.imread(image_path)
    if img is None:
        return list(GLASSES_FALLBACK_REGION)
    H, W = img.shape[:2]
    gray = cv2.equalizeHist(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

    def eyes_to_region(eyes, ox=0, oy=0):
        # 여러 눈 박스를 감싸는 합집합 + 안경테 여유 패딩
        x1 = min(ox + e[0] for e in eyes); y1 = min(oy + e[1] for e in eyes)
        x2 = max(ox + e[0] + e[2] for e in eyes); y2 = max(oy + e[1] + e[3] for e in eyes)
        pad_x = (x2 - x1) * 0.18; pad_y = (y2 - y1) * 0.35
        x1 = max(0, x1 - pad_x); y1 = max(0, y1 - pad_y)
        x2 = min(W, x2 + pad_x); y2 = min(H, y2 + pad_y)
        return [x1 / W, y1 / H, (x2 - x1) / W, (y2 - y1) / H]

    def face_eyeline_region(fx, fy, fw, fh):
        # 얼굴 bbox 비례로 안경이 놓이는 눈라인 영역(양안+안경테 포함)
        x1 = fx + 0.06 * fw; y1 = fy + 0.28 * fh
        x2 = fx + 0.94 * fw; y2 = fy + 0.56 * fh
        return [x1 / W, y1 / H, (x2 - x1) / W, (y2 - y1) / H]

    # 1) 얼굴을 먼저 찾고 그 안에서 안경-눈 검출(오검출 감소)
    faces = _face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60))
    for (fx, fy, fw, fh) in sorted(faces, key=lambda f: f[2] * f[3], reverse=True):
        roi = gray[fy:fy + fh, fx:fx + fw]
        for cascade in (_eye_glasses_cascade, _eye_cascade):
            eyes = cascade.detectMultiScale(roi, scaleFactor=1.1, minNeighbors=6, minSize=(15, 15))
            eyes = [e for e in eyes if e[1] + e[3] / 2 < fh * 0.6]  # 얼굴 상단(코/입 오검출 제거)
            # 양쪽 눈이 모두 잡혀야 안경 전체 폭을 신뢰할 수 있다. 1개면 반쪽만 덮으므로 버린다.
            if len(eyes) >= 2:
                return eyes_to_region(eyes, ox=fx, oy=fy)
        # 눈 2개 미만 → 얼굴 비례 눈라인 박스(단일 눈보다 안정적)
        return face_eyeline_region(fx, fy, fw, fh)

    # 2) 얼굴 검출 실패 → 이미지 전체에서 안경-눈 직접 검출(양안일 때만)
    for cascade in (_eye_glasses_cascade, _eye_cascade):
        eyes = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
        eyes = [e for e in eyes if e[1] + e[3] / 2 < H * 0.6]
        if len(eyes) >= 2:
            return eyes_to_region(eyes)

    # 3) 전부 실패 → 고정 폴백
    return list(GLASSES_FALLBACK_REGION)
