"""학습 전 라벨링 점검(진단). 구조적으로 잘못된 라벨을 조기에 드러낸다.

Custom Vision 객체탐지 요구사항(공식 limits-and-quotas 문서 기준):
  - 태그당 최소 15장(권장 50+)
  - 이미지 최소 256px(작으면 업스케일), 종횡비 25:1 이하, 형식 jpg/png/bmp/gif, 6MB 이하
  - 이미지당 리전 최대 300
  - 모든 학습 이미지는 최소 1개의 유효한 리전을 가져야 학습에 기여한다.
"""

MIN_IMAGES_PER_TAG = 15
RECOMMENDED_PER_TAG = 50
MIN_PIXELS = 256
MAX_ASPECT_RATIO = 25.0
TINY_AREA = 0.02  # 정규화 면적이 이보다 작으면 '너무 작은 박스'로 경고


def audit_labels(trainer, project):
    """프로젝트의 라벨 상태를 점검해 경고 리스트를 반환하고 요약을 출력한다(학습을 막지는 않음)."""
    warnings = []
    tags = {t.id: t.name for t in trainer.get_tags(project.id)}

    all_images = trainer.get_images(project.id, take=256)

    # 1) 리전 없는 이미지(학습에 기여 못 함)
    orphans = [im for im in all_images if not im.regions]
    if orphans:
        warnings.append(f"리전 없는 이미지 {len(orphans)}장 — 라벨을 달거나 제거하세요.")

    # 2) 이미지 규격(픽셀/종횡비)
    for im in all_images:
        w, h = getattr(im, "width", 0) or 0, getattr(im, "height", 0) or 0
        if w and h:
            if min(w, h) < MIN_PIXELS:
                warnings.append(f"이미지 {im.id[:8]} {w}x{h}: 최소 {MIN_PIXELS}px 미만(업스케일됨).")
            if max(w, h) / max(min(w, h), 1) > MAX_ASPECT_RATIO:
                warnings.append(f"이미지 {im.id[:8]} {w}x{h}: 종횡비 {MAX_ASPECT_RATIO:.0f}:1 초과.")

    # 3) 태그별 이미지 수 + 박스 유효성
    print("라벨 점검(태그별):")
    for tid, name in tags.items():
        imgs = trainer.get_tagged_images(project.id, tag_ids=[tid], take=256)
        n = len(imgs)
        if n < MIN_IMAGES_PER_TAG:
            warnings.append(f"[{name}] {n}장 < 최소 {MIN_IMAGES_PER_TAG}장 — 학습이 거부됩니다.")
        elif n < RECOMMENDED_PER_TAG:
            warnings.append(f"[{name}] {n}장(권장 {RECOMMENDED_PER_TAG}+): 정확도 향상엔 이미지 추가 권장.")
        for im in imgs:
            for r in (im.regions or []):
                if r.width * r.height < TINY_AREA:
                    warnings.append(f"[{name}] 너무 작은 박스(면적<{int(TINY_AREA * 100)}%): {im.id[:8]}")
                if r.left < 0 or r.top < 0 or r.left + r.width > 1.001 or r.top + r.height > 1.001:
                    warnings.append(f"[{name}] 이미지 밖으로 나간 박스: {im.id[:8]}")
        print(f"  [{name}] {n}장")

    # 이모지는 Windows cp949 콘솔에서 UnicodeEncodeError 를 내므로 ASCII 마커를 쓴다.
    if warnings:
        print(f"라벨 점검 결과: 경고 {len(warnings)}건")
        for w in warnings:
            print("  [!]", w)
    else:
        print("라벨 점검 결과: 문제 없음 [OK]")
    return warnings
