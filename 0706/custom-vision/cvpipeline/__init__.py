"""Custom Vision 객체탐지 파이프라인 패키지.

책임별로 모듈을 분리했다:
  config          — 환경변수·클라이언트·상수
  project_setup   — 도메인 조회, 프로젝트/태그 get-or-create
  regions         — fork/scissors 고정 바운딩 박스 좌표 데이터
  glasses_labels  — glasses 라벨 소스 결정(실제 어노테이션 우선, 없으면 cascade 폴백)
  glasses_detect  — OpenCV Haar cascade 로 안경 박스 자동 검출(어노테이션 없을 때의 추정)
  images          — 업로드 엔트리 구성·기존 이미지 삭제·배치 업로드
  training        — 진행 중 학습 대기 → force_train → 완료 폴링
  publish         — 학습된 이터레이션을 예측 엔드포인트에 게시
  prediction      — 예측 + 바운딩 박스 시각화
  pipeline        — 위 단계를 재사용 가능한 흐름으로 조립(train_and_publish / predict_images)
"""
