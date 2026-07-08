"""도메인 조회, 프로젝트/태그 get-or-create.

이름이 같은 리소스가 이미 있으면 재사용하고, 없을 때만 새로 만든다(재실행 안전).

재발방지: 이 파이프라인은 '객체탐지(ObjectDetection)' 전용이다. 포털에서 손으로 만든
프로젝트는 도메인이 Classification 인 경우가 있는데(프로젝트 타입은 생성 후 변경 불가),
그 프로젝트에 리전(바운딩 박스) 업로드·detect_image 를 시도하면 이해하기 어려운 에러로
실패한다. 그래서 프로젝트를 잡을 때 도메인 타입을 검증해 조기에 명확히 실패시킨다.
"""
from .config import PROJECT_ID, PROJECT_NAME


def find_object_detection_domain(trainer):
    """객체탐지용 General 도메인을 찾는다(프로젝트 생성 시에만 필요)."""
    return next(
        d for d in trainer.get_domains()
        if d.type == "ObjectDetection" and d.name == "General"
    )


def _ensure_object_detection(trainer, project):
    """프로젝트 도메인이 객체탐지인지 검증한다. 아니면 명확한 안내와 함께 실패."""
    domain = next((d for d in trainer.get_domains() if d.id == project.settings.domain_id), None)
    if domain is None or domain.type != "ObjectDetection":
        kind = domain.type if domain else "알 수 없음"
        raise RuntimeError(
            f"프로젝트 '{project.name}'(id={project.id}) 의 도메인 타입이 '{kind}' 입니다. "
            f"이 파이프라인은 객체탐지(ObjectDetection) 전용이며, 프로젝트 타입은 생성 후 "
            f"변경할 수 없습니다. VISION_PROJECT_ID/VISION_PROJECT_NAME 을 객체탐지 "
            f"프로젝트로 바꾸거나, 해당 환경변수를 비워 코드가 새 객체탐지 프로젝트를 "
            f"만들게 하세요."
        )


def get_or_create_project(trainer):
    """VISION_PROJECT_ID 가 있으면 그 프로젝트를, 없으면 이름으로 찾고, 없으면 새로 만든다."""
    if PROJECT_ID:
        project = trainer.get_project(PROJECT_ID)
        print(f"Using project by id: {project.name} ({project.id})")
        _ensure_object_detection(trainer, project)
        return project

    project = next((p for p in trainer.get_projects() if p.name == PROJECT_NAME), None)
    if project:
        print(f"Project '{PROJECT_NAME}' already exists with ID: {project.id}")
        _ensure_object_detection(trainer, project)
        return project

    print(f"create project '{PROJECT_NAME}'")
    domain = find_object_detection_domain(trainer)
    return trainer.create_project(PROJECT_NAME, domain_id=domain.id)


def get_or_create_tags(trainer, project, names=("fork", "scissors", "glasses")):
    """태그도 있으면 재사용, 없으면 생성한다. {이름: 태그} 딕셔너리를 반환."""
    existing = {t.name: t for t in trainer.get_tags(project.id)}
    return {name: (existing.get(name) or trainer.create_tag(project.id, name)) for name in names}
