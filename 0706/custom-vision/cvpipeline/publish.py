"""학습된 이터레이션을 예측 엔드포인트에 게시."""
from azure.cognitiveservices.vision.customvision.training.models import CustomVisionErrorException
from .config import PUBLISH_ITERATION_NAME, PREDICTION_RESOURCE_ID


def publish_latest(trainer, project, iteration):
    """최신 이터레이션을 엔드포인트에 게시한다. 이름을 옛 이터레이션이 점유 중이면 해제 후 재게시."""
    try:
        trainer.publish_iteration(project.id, iteration.id, PUBLISH_ITERATION_NAME, PREDICTION_RESOURCE_ID)
        print(f"Published: {PUBLISH_ITERATION_NAME} -> {iteration.name}")
    except CustomVisionErrorException as e:
        msg = e.message or ""
        if "already published as" in msg:
            # 이 이터레이션이 이미 같은 이름으로 게시됨 → 그대로 사용
            print(f"이미 게시됨: {iteration.name} ({PUBLISH_ITERATION_NAME})")
        elif "name is in use" in msg:
            # 다른(옛) 이터레이션이 이름을 점유 → 해제 후 최신 이터레이션으로 재게시
            print("옛 이터레이션이 이름 점유 중 → unpublish 후 최신 이터레이션으로 재게시")
            for it in trainer.get_iterations(project.id):
                if it.publish_name == PUBLISH_ITERATION_NAME:
                    trainer.unpublish_iteration(project.id, it.id)
                    print(f"  unpublish: {it.name}")
            trainer.publish_iteration(project.id, iteration.id, PUBLISH_ITERATION_NAME, PREDICTION_RESOURCE_ID)
            print(f"Published: {PUBLISH_ITERATION_NAME} -> {iteration.name}")
        else:
            raise
