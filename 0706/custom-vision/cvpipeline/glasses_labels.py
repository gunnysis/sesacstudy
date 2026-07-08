"""glasses 바운딩 박스의 '라벨 소스'를 우선순위대로 결정한다.

설계 배경: fork/scissors 는 좌표를 하드코딩(정확하지만 확장 불가)하고, glasses 는 cascade 로
자동 검출(확장되지만 '정답'이 아니라 '추정')한다. 둘 다 나름의 단점이 있다. 진짜 정답은
'데이터셋의 실제 어노테이션(ground truth)' 이다. 그래서 라벨을 아래 우선순위로 고른다:

  1) 실제 어노테이션 (가장 정확)
       - 같은 이름의 YOLO .txt  (Roboflow 'YOLO' 내보내기: `cls cx cy w h`, 정규화)
       - 폴더의 _annotations.csv (Roboflow 'Tensorflow CSV': filename,width,height,class,xmin,ymin,xmax,ymax)
  2) OpenCV Haar cascade 자동 검출 (어노테이션이 없을 때의 '추정' — 부정확할 수 있음)

핵심: cascade 는 정답이 아니라 추정이다. 실제 라벨이 있으면 반드시 그것을 쓰고, 없을 때만
폴백한다. resolve_glasses_region 은 (region, source) 를 함께 반환해 어떤 소스를 썼는지 드러낸다.
"""
import os
import csv

from .glasses_detect import detect_glasses_region

_csv_cache = {}          # {glasses_dir: {filename: [left, top, w, h]}}
_csv_loaded = set()


def _load_annotations_csv(image_dir):
    """폴더의 _annotations.csv(Roboflow TF CSV)를 한 번만 읽어 파일명→정규화 박스 로 인덱싱."""
    if image_dir in _csv_loaded:
        return _csv_cache.get(image_dir, {})
    _csv_loaded.add(image_dir)
    path = os.path.join(image_dir, "_annotations.csv")
    if not os.path.exists(path):
        return {}
    table = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                w, h = float(row["width"]), float(row["height"])
                xmin, ymin = float(row["xmin"]), float(row["ymin"])
                xmax, ymax = float(row["xmax"]), float(row["ymax"])
            except (KeyError, ValueError):
                continue
            if w > 0 and h > 0:
                table[row["filename"]] = [xmin / w, ymin / h, (xmax - xmin) / w, (ymax - ymin) / h]
    _csv_cache[image_dir] = table
    return table


def _yolo_txt_region(image_path):
    """같은 이름의 YOLO .txt(`cls cx cy w h`, 정규화)가 있으면 첫 박스를 [left, top, w, h] 로 반환."""
    txt = os.path.splitext(image_path)[0] + ".txt"
    if not os.path.exists(txt):
        return None
    with open(txt, encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 5:
                _, cx, cy, w, h = (float(x) for x in parts[:5])
                return [max(0.0, cx - w / 2), max(0.0, cy - h / 2), w, h]
    return None


def resolve_glasses_region(image_path):
    """glasses 이미지 1장의 (region, source) 를 반환. source ∈ {'yolo', 'csv', 'cascade'}."""
    yolo = _yolo_txt_region(image_path)
    if yolo:
        return yolo, "yolo"

    table = _load_annotations_csv(os.path.dirname(image_path))
    box = table.get(os.path.basename(image_path))
    if box:
        return box, "csv"

    return detect_glasses_region(image_path), "cascade"
