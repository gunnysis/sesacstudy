"""백엔드/force_train 격리 검증용 임시 러너.

전략: glasses 를 실제로 삭제→재업로드해 '진짜 변경'을 만든 뒤, 정상 완료 이력이 있는
일반 학습(force=False)으로 학습한다(Iteration 1~3 과 동일 경로). force_train=True 경로만
hang 하는지 격리한다. 학습은 20분 타임아웃 내장.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

from cvpipeline.config import make_trainer, make_predictor, BASE_IMAGE_LOCATION
from cvpipeline.project_setup import get_or_create_project, get_or_create_tags
from cvpipeline.images import build_tagged_images, delete_tagged_images, upload_images
from cvpipeline.training import train, wait_for_pending_iterations, TrainingStuckError
from cvpipeline.publish import publish_latest
from cvpipeline.prediction import predict_and_visualize

trainer = make_trainer()
predictor = make_predictor()
project = get_or_create_project(trainer)

# 0) 진행 중인 이전 학습이 있으면 먼저 대기 — 학습이 참조 중인 이미지를 지우면 wedge 위험
wait_for_pending_iterations(trainer, project)

# 1) 진짜 변경 만들기: glasses 삭제 → 새 박스로 재업로드
tags = get_or_create_tags(trainer, project)
print("Adding images...")
entries = build_tagged_images(tags)
deleted = delete_tagged_images(trainer, project, tags["glasses"])
print(f"  기존 glasses {deleted}장 삭제")
failed = upload_images(trainer, project, entries)
print(f"  업로드 완료(실패 {len(failed)}건)")

# 2) 일반 학습(force=False) — 검증된 경로
try:
    iteration = train(trainer, project, force=False)   # 20분 타임아웃 내장
except TrainingStuckError as e:
    print(f"[STUCK 확인] {e}")
    sys.exit(2)

publish_latest(trainer, project, iteration)
print("Done!")

test_dir = os.path.join(BASE_IMAGE_LOCATION, "test")
predictions_dir = os.path.join(BASE_IMAGE_LOCATION, "predictions")
predict_and_visualize(predictor, project, os.path.join(test_dir, "test_image3.jpg"), predictions_dir, 0.3)
