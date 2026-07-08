"""파이프라인 상위 단계 조립: 학습·게시 / 예측.

main.py(그리고 검증 러너 등)가 흐름을 중복 작성하지 않고 재사용하도록 함수로 묶었다.
클라이언트·프로젝트 생성 같은 진입 관심사는 호출자(main)가 담당하고, 여기서는 순수하게
'무엇을 어떤 순서로' 만 조립한다.
"""
from .project_setup import get_or_create_tags
from .images import build_tagged_images, delete_tagged_images, upload_images
from .audit import audit_labels
from .training import train, wait_for_pending_iterations
from .publish import publish_latest
from .prediction import predict_and_visualize


def train_and_publish(trainer, project, refresh_glasses=False, force=False):
    """태그·이미지 준비 → (옵션) glasses 재업로드 → 학습 → 게시. 학습된 iteration 을 반환한다.

    refresh_glasses: glasses 박스 계산 로직이 바뀌었을 때만 True(기존 glasses 삭제 후 재업로드).
    force: 데이터가 그대로여도 새 이터레이션을 강제 학습(기본 False — 변경 없으면 기존 모델 재사용).
    """
    tags = get_or_create_tags(trainer, project)

    # 재발방지(근본원인): 이미지 삭제·업로드보다 '먼저' 진행 중인 이전 학습을 기다린다.
    # 옛 코드는 삭제→업로드를 먼저 해서, 진행 중 학습이 참조하는 이미지를 도중에 지웠고
    # 이것이 이터레이션이 'Training' 에 수 시간 매달리는 백엔드 wedge 의 유력 원인이었다.
    wait_for_pending_iterations(trainer, project)

    print("Adding images...")
    entries = build_tagged_images(tags)

    if refresh_glasses:
        # 같은 이미지는 OKDuplicate 로 건너뛰어 '옛 박스'가 남으므로, 박스 로직이 바뀐 경우에만 삭제 후 재업로드
        print("기존 glasses 이미지 정리(새 박스 반영을 위해)...")
        deleted = delete_tagged_images(trainer, project, tags["glasses"])
        print(f"  기존 glasses 이미지 {deleted}장 삭제(없으면 0 — 첫 실행이면 정상)")

    failed = upload_images(trainer, project, entries)
    if failed:
        for image in failed:
            print("Image status: ", image.status)
        raise RuntimeError("Image batch upload failed.")
    print("Image upload OK (duplicates skipped).")

    # 학습 전 라벨링 점검(문제를 조기에 드러냄 — 학습을 막지는 않는다)
    audit_labels(trainer, project)

    iteration = train(trainer, project, force=force)
    publish_latest(trainer, project, iteration)
    print("Done!")
    return iteration


def predict_images(predictor, project, test_image_paths, threshold, test_dir):
    """주어진 이미지들을 각각 예측하고 바운딩 박스 시각화 PNG 를 저장한다."""
    for path in test_image_paths:
        predict_and_visualize(predictor, project, path, test_dir, threshold)
