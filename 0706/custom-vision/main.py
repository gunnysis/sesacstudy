"""Custom Vision 객체탐지 파이프라인 엔트리포인트.

fork·scissors·glasses 를 감지하는 모델을 학습·게시하고 테스트 이미지를 예측한다.
기능별 모듈은 cvpipeline 패키지에 분리돼 있고, 이 파일은 CLI 파싱과 전체 흐름 조립만 담당한다.

사용법:
python main.py [임계값 0~1] [테스트이미지경로]
    - 인자 없음     : Images/test 폴더의 모든 이미지를 예측(임계값 0.5)
    - 임계값만      : 표시 신뢰도 기준만 변경
    - 임계값 + 경로 : 지정한 그 파일 하나만 예측
예측 결과 PNG 는 Images/predictions/ 에 저장된다(입력·출력 분리).
python main.py --help  로 옵션 설명을 볼 수 있다.

참고 문서:
https://learn.microsoft.com/ko-kr/azure/ai-services/custom-vision-service/quickstarts/object-detection?pivots=programming-language-python
"""
import os
import sys
import glob
import argparse

import matplotlib.pyplot as plt

from cvpipeline.config import make_trainer, make_predictor, BASE_IMAGE_LOCATION
from cvpipeline.project_setup import get_or_create_project
from cvpipeline.pipeline import train_and_publish, predict_images
from cvpipeline.training import TrainingStuckError

# Windows 콘솔(cp949)에서 한글 출력이 깨지지 않도록 UTF-8 로 강제
sys.stdout.reconfigure(encoding="utf-8")


def parse_args():
    """CLI 인자 파싱. 기존 위치 인자(임계값, 이미지경로)를 그대로 유지하면서 --help 를 제공한다."""
    parser = argparse.ArgumentParser(
        description="fork·scissors·glasses 객체탐지 학습·게시·예측 파이프라인",
    )
    parser.add_argument(
        "threshold", nargs="?", type=float, default=0.5,
        help="표시할 최소 신뢰도 0~1 (기본 0.5)",
    )
    parser.add_argument(
        "image", nargs="?", default=None,
        help="예측할 특정 이미지 경로 (생략 시 Images/test 폴더의 모든 이미지)",
    )
    parser.add_argument(
        "--refresh-glasses", action="store_true",
        help="glasses 박스 계산 로직이 바뀐 경우: 기존 glasses 이미지를 지우고 새 박스로 재업로드",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="데이터 변경이 없어도 새 이터레이션을 강제로 학습(기본: 변경 없으면 기존 모델 재사용)",
    )
    return parser.parse_args()


def resolve_test_images(test_dir, image_arg):
    """예측할 테스트 이미지 경로 리스트를 결정한다(인자로 특정 파일 지정 가능).

    예측 결과 PNG 는 별도 폴더(Images/predictions/)에 저장되므로, test 폴더의
    모든 이미지 파일을 파일명 제한 없이 예측 대상으로 삼는다.
    """
    if image_arg:
        return [image_arg]
    return sorted(
        p for p in glob.glob(os.path.join(test_dir, "*"))
        if p.lower().endswith((".jpg", ".jpeg", ".png"))
    )


def main():
    args = parse_args()

    trainer = make_trainer()
    predictor = make_predictor()

    # 1) 프로젝트 준비
    print("================================================================")
    project = get_or_create_project(trainer)
    print(project.name, project.id)
    print("================================================================")

    # 2) 이미지 구성 → 업로드 → 학습 → 게시
    try:
        train_and_publish(trainer, project,
                          refresh_glasses=args.refresh_glasses, force=args.force)
    except TrainingStuckError as e:
        # 학습이 타임아웃(백엔드 stuck)으로 끝남 — raw 트레이스백 대신 깔끔히 안내하고 종료.
        print("=" * 60)
        print(f"[학습 중단] {e}")
        print("  데이터·라벨은 그대로 유지됩니다. 백엔드 회복 후 다시 실행하면 이어집니다.")
        print("=" * 60)
        sys.exit(2)

    # 3) 예측 + 시각화 (입력: Images/test/, 출력: Images/predictions/ — 입력·출력 분리)
    test_dir = os.path.join(BASE_IMAGE_LOCATION, "test")
    predictions_dir = os.path.join(BASE_IMAGE_LOCATION, "predictions")
    test_image_paths = resolve_test_images(test_dir, args.image)
    if not test_image_paths:
        print(f"[경고] 예측할 이미지가 없습니다. {test_dir} 에 이미지(jpg/png)를 넣으세요.")
    predict_images(predictor, project, test_image_paths, args.threshold, predictions_dir)

    # 파일 저장과 별개로 모든 결과 창을 띄운다 (창을 닫으면 종료)
    plt.show()


if __name__ == "__main__":
    main()
