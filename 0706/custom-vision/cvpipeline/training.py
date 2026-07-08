"""학습: 진행 중 이터레이션 대기 → force_train → 완료 폴링.

재발방지: 폴링에 '무한 대기'를 두지 않는다. Custom Vision 백엔드가 stuck 되면(이터레이션이
2시간 넘게 'Training' 에 머무는 사례가 있었다) 옛 코드는 조용히 영원히 매달렸다. 이제는
- 학습이 TRAIN_TIMEOUT_SEC 를 넘기면 TrainingStuckError 로 명확히 실패시키고,
- 진행 중 이전 학습 대기도 상한을 두며,
- 'Failed' 상태도 무한 루프 대신 즉시 예외로 처리하고,
- 1초마다 'Training' 을 도배하는 대신 경과 시간을 주기적으로만 로깅한다.
"""
import time
from azure.cognitiveservices.vision.customvision.training.models import CustomVisionErrorException

# 학습이 이 시간을 넘기면 백엔드 stuck 으로 보고 무한 대기 대신 실패시킨다(정상 학습은 보통 7~15분).
TRAIN_TIMEOUT_SEC = 1200          # 20분
# 진행 중인 '이전' 학습을 기다리는 상한(그 이터레이션이 stuck 이면 여기서 걸린다).
PENDING_WAIT_TIMEOUT_SEC = 1200   # 20분
POLL_INTERVAL_SEC = 5             # 상태 폴링 간격(옛 1초는 API 낭비 + 로그 도배)
LOG_EVERY_SEC = 15                # 경과 로그 출력 주기

TERMINAL = ("Completed", "Failed")
# 프로젝트당 이터레이션 상한은 F0/S0 공통 20개(공식 limits-and-quotas). 상한에 닿으면
# train_project 자체가 거부되므로, 학습 전에 오래된 미게시 이터레이션을 정리해 여유를 확보한다.
MAX_ITERATIONS_PER_PROJECT = 20
KEEP_RECENT_ITERATIONS = 5


class TrainingStuckError(RuntimeError):
    """학습이 제한 시간 내에 끝나지 않음(Custom Vision 백엔드 stuck 추정)."""


def _fmt(sec):
    m, s = divmod(int(sec), 60)
    return f"{m}분 {s}초"


def wait_for_pending_iterations(trainer, project, timeout_sec=PENDING_WAIT_TIMEOUT_SEC):
    """진행 중인 이전 학습이 남아 있으면 끝날 때까지(상한 내에서) 기다린다.

    이전 실행을 로컬에서 중단해도 클라우드 학습은 계속된다. 진행 중 학습이 남아 있으면 새
    train_project 가 TrainingAlreadyInProgress 로 거부되므로 먼저 대기하되, 상한을 넘기면
    stuck 으로 보고 명확히 실패시킨다(삭제 후 재시도 안내).
    """
    for pending in trainer.get_iterations(project.id):
        if pending.status in TERMINAL:
            continue
        print(f"진행 중인 이전 학습 대기: {pending.name} ({pending.status})")
        start = time.time()
        while pending.status not in TERMINAL:
            if time.time() - start > timeout_sec:
                raise TrainingStuckError(
                    f"이전 이터레이션 '{pending.name}' 이 {_fmt(timeout_sec)} 넘게 "
                    f"'{pending.status}' 입니다. 백엔드 stuck 으로 보입니다 — 해당 이터레이션을 "
                    f"삭제(delete_iteration) 후 다시 시도하세요."
                )
            time.sleep(POLL_INTERVAL_SEC)
            pending = trainer.get_iteration(project.id, pending.id)
        print(f"  → {pending.name} {pending.status}")


def prune_old_iterations(trainer, project, keep_recent=KEEP_RECENT_ITERATIONS):
    """완료됐고 게시되지 않은 오래된 이터레이션을 정리한다(최근 keep_recent 개는 보존).

    이터레이션은 프로젝트당 20개 상한이 있어, 매 실행 새 이터레이션을 만들다 보면 어느 순간
    train_project 가 거부된다. 게시 중(publish_name 있음)·진행 중 이터레이션은 건드리지 않는다.
    """
    iterations = sorted(trainer.get_iterations(project.id), key=lambda it: it.created, reverse=True)
    deletable = [
        it for it in iterations
        if it.status == "Completed" and not it.publish_name
    ]
    for it in deletable[keep_recent:]:
        trainer.delete_iteration(project.id, it.id)
        print(f"  오래된 이터레이션 정리: {it.name} (created={it.created})")
    if len(iterations) >= MAX_ITERATIONS_PER_PROJECT:
        print(f"  [!] 이터레이션 {len(iterations)}개 — 상한 {MAX_ITERATIONS_PER_PROJECT}개에 근접/도달. "
              f"게시 해제 후 수동 정리가 필요할 수 있습니다.")


def _latest_completed(trainer, project):
    """가장 최근에 학습 완료된 이터레이션을 반환한다(없으면 None)."""
    completed = [it for it in trainer.get_iterations(project.id) if it.status == "Completed"]
    if not completed:
        return None
    return sorted(completed, key=lambda it: it.trained_at)[-1]


def _poll_until_done(trainer, project, iteration, timeout_sec):
    """이터레이션이 Completed 될 때까지 폴링. 타임아웃/Failed 는 예외로 드러낸다."""
    start = time.time()
    last_log = -LOG_EVERY_SEC
    while iteration.status != "Completed":
        if iteration.status == "Failed":
            raise TrainingStuckError(f"학습이 'Failed' 상태로 끝났습니다: {iteration.name}")
        elapsed = time.time() - start
        if elapsed > timeout_sec:
            raise TrainingStuckError(
                f"학습이 {_fmt(timeout_sec)} 을 초과했는데 아직 '{iteration.status}' 입니다. "
                f"Custom Vision 백엔드가 stuck 된 것으로 보입니다(대개 서버측 일시 장애). "
                f"이터레이션 '{iteration.name}' 을 삭제하고 잠시 후 재시도하세요."
            )
        if elapsed - last_log >= LOG_EVERY_SEC:
            print(f"Training status: {iteration.status} (경과 {_fmt(elapsed)})")
            last_log = elapsed
        time.sleep(POLL_INTERVAL_SEC)
        iteration = trainer.get_iteration(project.id, iteration.id)
    return iteration


def train(trainer, project, timeout_sec=TRAIN_TIMEOUT_SEC, force=False):
    """새 이터레이션을 학습하고 완료될 때까지(상한 내에서) 폴링해 반환한다.

    force 기본 False(재발방지): 옛 코드는 매 실행 force_train=True 로 무조건 새 학습을 만들어
    - 데이터가 그대로여도 매번 수 분짜리 전체 학습이 돌고,
    - 이터레이션이 쌓여 프로젝트당 20개 상한에 다가갔다.
    이제 변경이 없으면 서비스가 'Nothing changed' 로 거부하고, 그 경우 최신 완료 모델을
    재사용한다. glasses 박스 로직을 바꿨다면 --refresh-glasses(삭제→재업로드)로 진짜 변경을
    만들거나 --force 로 강제 학습한다.
    """
    wait_for_pending_iterations(trainer, project)
    prune_old_iterations(trainer, project)

    print(f"Training... (force_train={force})")
    training_start = time.time()
    try:
        iteration = trainer.train_project(project.id, force_train=force)
    except CustomVisionErrorException as e:
        msg = e.message or ""
        if "Nothing changed" in msg:
            # 데이터 변경 없음 → 학습 불필요. 최신 완료 모델을 그대로 쓴다(정상 경로).
            latest = _latest_completed(trainer, project)
            if latest:
                print(f"변경 없음 → 학습 생략, 기존 모델 재사용: {latest.name} (trained_at={latest.trained_at})")
                return latest
            raise
        if "Not enough images" in msg:
            # "이미지 부족"은 알려진 정상 실패로 처리(옛 모델로 예측만 이어감). 그 외 에러는
            # 조용히 옛 모델을 쓰면 원인을 가리므로 그대로 올려서 실패를 드러낸다.
            print("=" * 60)
            print(f"[경고] 학습 실패: {msg}")
            print("  어떤 태그가 최소 15장 미만이라 학습이 거부됐습니다.")
            print("  아래 예측은 새로 학습하지 못한 '이전 모델' 결과입니다.")
            print("=" * 60)
            latest = _latest_completed(trainer, project)
            if not latest:
                raise
            print(f"재사용 이터레이션: {latest.name} (trained_at={latest.trained_at})")
            return latest
        raise

    iteration = _poll_until_done(trainer, project, iteration, timeout_sec)

    elapsed = time.time() - training_start
    print(f"Training completed in {_fmt(elapsed)} (total {elapsed:.1f}s)")
    return iteration
