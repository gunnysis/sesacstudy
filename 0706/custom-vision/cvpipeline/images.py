"""학습 이미지 구성·삭제·업로드.

fork/scissors 는 고정 좌표(regions), glasses 는 자동 검출(glasses_detect)로 박스를 붙인다.
"""
import os
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageFileCreateBatch, ImageFileCreateEntry, Region,
)
from .config import BASE_IMAGE_LOCATION
from .regions import fork_image_regions, scissors_image_regions
from .glasses_labels import resolve_glasses_region, _yolo_txt_region

# OKDuplicate = 이미 업로드된 이미지(재실행 시 정상). 진짜 실패만 걸러낸다.
OK_STATUSES = {"OK", "OKDuplicate"}
# Custom Vision 은 한 번에 최대 64장까지만 업로드 가능하므로 64장씩 나눠 올린다.
BATCH_SIZE = 64


def _entries_from_fixed_regions(folder, region_map, tag):
    """고정 좌표 딕셔너리로 업로드 엔트리 리스트를 만든다(fork/scissors 공통)."""
    entries = []
    for file_name, (x, y, w, h) in region_map.items():
        regions = [Region(tag_id=tag.id, left=x, top=y, width=w, height=h)]
        path = os.path.join(BASE_IMAGE_LOCATION, folder, file_name + ".jpg")
        with open(path, mode="rb") as image_contents:
            entries.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), regions=regions))
    return entries


def _entries_from_aug_sidecars(folder, tag):
    """aug_* 증강 이미지(augment_forkscissors.py 가 만든 YOLO .txt 사이드카)의 엔트리를 만든다."""
    dir_path = os.path.join(BASE_IMAGE_LOCATION, folder)
    entries = []
    for file_name in sorted(os.listdir(dir_path)):
        if not (file_name.startswith("aug_") and file_name.lower().endswith((".jpg", ".jpeg", ".png"))):
            continue
        path = os.path.join(dir_path, file_name)
        box = _yolo_txt_region(path)
        if not box:
            continue  # 사이드카 없는 증강본은 박스를 알 수 없으므로 제외
        x, y, w, h = box
        regions = [Region(tag_id=tag.id, left=x, top=y, width=w, height=h)]
        with open(path, mode="rb") as image_contents:
            entries.append(ImageFileCreateEntry(
                name=os.path.splitext(file_name)[0], contents=image_contents.read(), regions=regions))
    return entries


def build_tagged_images(tags):
    """fork/scissors/glasses 전체에 대해 태그+박스가 붙은 업로드 엔트리를 만든다."""
    entries = []
    fork_n = scissors_n = 0
    for folder, region_map, tag_name in (("fork", fork_image_regions, "fork"),
                                         ("scissors", scissors_image_regions, "scissors")):
        fixed = _entries_from_fixed_regions(folder, region_map, tags[tag_name])
        aug = _entries_from_aug_sidecars(folder, tags[tag_name])
        entries += fixed + aug
        if folder == "fork":
            fork_n = len(fixed) + len(aug)
        else:
            scissors_n = len(fixed) + len(aug)

    # glasses 폴더의 모든 이미지 파일을 자동으로 학습에 사용한다(파일명 하드코딩 불필요).
    glasses_dir = os.path.join(BASE_IMAGE_LOCATION, "glasses")
    glasses_files = sorted(
        f for f in os.listdir(glasses_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    )
    label_sources = {}  # 라벨 소스별 집계(yolo/csv=실제 어노테이션, cascade=추정)
    for file_name in glasses_files:
        image_path = os.path.join(glasses_dir, file_name)
        (x, y, w, h), source = resolve_glasses_region(image_path)  # 실제 라벨 우선, 없으면 cascade
        label_sources[source] = label_sources.get(source, 0) + 1
        regions = [Region(tag_id=tags["glasses"].id, left=x, top=y, width=w, height=h)]
        with open(image_path, mode="rb") as image_contents:
            entries.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), regions=regions))

    print(f"  fork {fork_n}장 / scissors {scissors_n}장 / glasses {len(glasses_files)}장 준비 (증강 포함)")
    src_desc = ", ".join(f"{k}={v}" for k, v in sorted(label_sources.items()))
    print(f"  glasses 라벨 소스: {src_desc}")
    if label_sources.get("cascade") and not (label_sources.get("yolo") or label_sources.get("csv")):
        print("  [!] glasses 박스가 전부 cascade '추정'입니다 — 정확도를 위해 Roboflow 등에서 "
              "실제 어노테이션(YOLO .txt 또는 _annotations.csv)을 함께 넣으면 자동으로 그것을 씁니다.")
    return entries


def delete_tagged_images(trainer, project, tag):
    """특정 태그가 달린 기존 이미지를 모두 지운다.

    glasses 박스를 새로 계산했어도 같은 이미지가 이미 프로젝트에 있으면 업로드가 OKDuplicate 로
    건너뛰어져 '옛 박스'가 그대로 남는다. 그래서 재업로드 전에 이 함수로 먼저 지워 새 박스를 반영한다.
    반환값: 삭제한 이미지 수.
    """
    deleted_total = 0
    while True:
        existing = trainer.get_tagged_images(project.id, tag_ids=[tag.id], take=256)
        if not existing:
            break
        trainer.delete_images(project.id, image_ids=[img.id for img in existing])
        deleted_total += len(existing)
        if len(existing) < 256:
            break
    return deleted_total


def upload_images(trainer, project, entries):
    """엔트리를 64장씩 나눠 업로드하고, OK/OKDuplicate 가 아닌 실패 엔트리 리스트를 반환한다."""
    failed = []
    for i in range(0, len(entries), BATCH_SIZE):
        chunk = entries[i:i + BATCH_SIZE]
        result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=chunk))
        failed.extend(img for img in result.images if img.status not in OK_STATUSES)
    return failed
