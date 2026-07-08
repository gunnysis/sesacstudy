# Custom Vision 학습 장애 디버깅 기록 (2026-07-08)

객체탐지 파이프라인에서 **학습이 기준 시간(수 분~15분)을 훨씬 초과해 몇 시간씩 'Training' 상태에
매달리고, 이후 재학습도 정상 동작하지 않던** 장애의 원인 분석·수정·검증 기록.

## 1. 증상

- `train_project()` 로 시작한 이터레이션이 2시간 넘게 `Training` 상태에서 진행되지 않음 (정상: 이 데이터 규모 ~90장 기준 약 9분).
- 진행 중 이터레이션을 삭제해도 후속 학습이 전부 같은 방식으로 hang (프로젝트 학습 큐 자체가 wedge 된 것으로 추정).
- 우회를 위해 포털에서 새 프로젝트를 만들었지만 여전히 코드가 정상 학습하지 못함.

## 2. 진단 과정 (타임라인)

| 단계 | 확인 내용 | 결과 |
|---|---|---|
| 로컬 코드 정독 | `cvpipeline/` 전 모듈 + `main.py` 흐름 분석 | 순서 버그 발견 (아래 3-1) |
| Azure 상태 조회 | Training API 로 프로젝트/이터레이션/태그 전수 조회 | 옛 프로젝트는 이미 삭제됨. 포털에서 새로 만든 `sesac015-cv-project1` 은 **Classification 도메인**(객체탐지 사용 불가), 태그·이미지·이터레이션 0 |
| .env ↔ 코드 대조 | 코드가 읽는 환경변수 키와 .env 의 키 비교 | 키 이름 불일치 → 코드가 의도한 프로젝트를 전혀 가리키지 못함 (아래 3-3) |
| 리소스 SKU 확인 | `az cognitiveservices account show` | Training/Prediction 모두 **S0(표준)**, japaneast → 무료(F0) 쿼터 문제 아님 |
| 공식 문서 팩트체크 | limits-and-quotas 문서 | **이터레이션 상한: 프로젝트당 20개(F0/S0 공통)**, 태그당 최소 15장(권장 50+), 업로드 배치 64장 등 확인 |

## 3. 근본 원인 (3중)

### 3-1. 순서 버그 — 진행 중 학습이 참조하는 이미지를 도중에 삭제 (핵심)

옛 `pipeline.py` 는 매 실행마다 ① glasses 이미지 전체 삭제 → ② 재업로드 → ③ 학습(그리고 학습
함수 **안에서야** 이전 학습 대기)을 수행했다. 이전 실행의 학습이 클라우드에서 아직 도는 중에
그 학습이 참조하는 이미지 50장을 지우는 구조 → 백엔드 이터레이션이 `Training` 에서 수 시간
멈추는 wedge 를 유발했고, 한 번 wedge 되면 그 프로젝트의 후속 학습도 연쇄적으로 hang 했다.

### 3-2. 매 실행 강제 재학습 — `force_train=True`

데이터가 그대로여도 매 실행 새 이터레이션을 만들었다. 불필요한 전체 학습(수 분)이 반복되고,
**프로젝트당 이터레이션 20개 상한**에 다가가면 `train_project` 자체가 거부된다.

### 3-3. 환경 불일치 — 존재하지 않는/잘못된 프로젝트 참조

- 코드가 읽는 키는 `VISION_PROJECT_NAME` 인데 .env 에는 다른 이름의 키만 있어 기본값으로 폴백 → 존재하지 않는 프로젝트명을 계속 참조(재실행 시 빈 프로젝트를 새로 만들 상황).
- 포털에서 우회용으로 만든 프로젝트는 도메인이 **Classification** — 객체탐지 파이프라인(리전 업로드·`detect_image`)에 사용 불가. **프로젝트 타입(도메인 종류)은 생성 후 변경 불가**라 삭제가 정답이었다.

## 4. 수정 내역

| 파일 | 수정 | 근거 |
|---|---|---|
| `cvpipeline/pipeline.py` | **이전 학습 대기를 이미지 삭제/업로드보다 앞으로** 이동. glasses 삭제→재업로드는 `--refresh-glasses` 옵션일 때만 | 3-1 재발 방지 |
| `cvpipeline/training.py` | `force` 기본값 True→**False**. `Nothing changed` 응답이면 학습 생략 후 최신 완료 모델 재사용. 완료·미게시 이터레이션 자동 정리(최근 5개 보존, 20개 상한 보호) | 3-2 재발 방지 |
| `cvpipeline/project_setup.py` | `VISION_PROJECT_ID` 직접 지정 지원 + **ObjectDetection 도메인 검증**(Classification 오지정 시 명확한 에러로 조기 실패) | 3-3 재발 방지 |
| `main.py` | `--refresh-glasses`·`--force` CLI 플래그 추가 | 운영 편의 |
| `.env` / `.env.example` | 코드가 읽는 키로 정리(`VISION_PROJECT_ID/NAME` → 객체탐지 프로젝트 `sesac015-od-project1`), 변수 목록 문서화 | 3-3 재발 방지 |

기존에 이미 있던 안전장치(학습 폴링 20분 타임아웃, `Failed` 즉시 예외, 진행 중 학습 대기 상한)는 유지.

## 5. 데이터 품질 개선 (권장사항 적용)

- **glasses 실제 어노테이션 적용**: 원본 데이터셋(`detection/worn/ex07`)의 픽셀 xyxy 라벨 50건을
  `Images/glasses/_annotations.csv`(Roboflow TF CSV 형식)로 변환·배치. 좌표 형식은
  "xywh 로 해석하면 x+w 최대 284 > 이미지 폭 256" 모순으로 **xyxy 확정** + 샘플에 박스를 그려 시각
  검증. 이제 파이프라인이 cascade 추정 대신 실제 라벨(csv=50)을 사용.
- **fork·scissors 증강 20→50장**: `augment_forkscissors.py` — 좌우 반전(박스 `left' = 1 - left - width`
  변환) + 밝기 변형(박스 불변)으로 태그당 50장 확보. 증강 박스는 YOLO 정규화 `.txt` 사이드카로
  저장하고 `cvpipeline/images.py` 가 읽음. 반전 박스는 수식 검증 + 이미지에 그려 시각 검증.
- 결과: 학습 전 라벨 점검(audit) **경고 0건** (이전: fork/scissors 권장 50장 미달 경고 2건).

## 6. 검증 결과

| 검증 | 결과 |
|---|---|
| 1차 전체 실행 (수정 후, 90장) | 학습 **9분 0초** 정상 완료 → 게시 → 예측: fork 79.3% / scissors 94.6% / glasses 86.6% 모두 정확 검출 |
| 멱등 재실행 (변경 없음) | `Nothing changed` → 학습 생략, 기존 모델 재사용, 수 초 내 예측만 수행 |
| 도메인 검증 | Classification 프로젝트 지정 시 명확한 에러로 조기 실패 확인 |
| 2차 전체 실행 (실제 라벨 + 증강 150장) | 태그당 50장 업로드, 라벨 점검 경고 0건, 학습 **10분 51초** 완료 → Iteration 2 재게시 → 예측 3종 정상 |
| 게시 모델 성능 (임계 0.5) | **precision 1.000 / recall 0.800 / mAP 0.994** — glasses 는 실제 어노테이션 덕에 precision·recall·AP 모두 1.000 |

## 7. 재발 방지 수칙

1. **학습이 돌고 있을 때 그 프로젝트의 이미지를 삭제하지 않는다** — 반드시 이터레이션이 터미널 상태(Completed/Failed)가 된 뒤 변경.
2. `force_train` 은 필요할 때만 — 평소엔 변경 감지에 맡기고, 변경이 없으면 기존 모델을 재사용한다.
3. 포털에서 프로젝트를 만들 땐 **도메인 종류(Object Detection vs Classification)** 를 먼저 확인 — 생성 후 변경 불가.
4. 폴링에는 항상 타임아웃을 둔다(무한 대기 금지). 정상 학습 시간의 기준을 기록해 둔다(이 데이터 규모: ~9분).
5. .env 키 이름은 `.env.example` 과 코드(config.py)를 기준으로 맞춘다.

## 참고

- [객체 탐지 퀵스타트(Python)](https://learn.microsoft.com/ko-kr/azure/ai-services/custom-vision-service/quickstarts/object-detection?pivots=programming-language-python) — 이 파이프라인의 기준 문서 (이미지 분류 퀵스타트와 혼동 주의)
- [한도 및 할당량](https://learn.microsoft.com/ko-kr/azure/ai-services/custom-vision-service/limits-and-quotas) — 이터레이션 20개/태그당 최소 15장/배치 64장 등
- ⚠ Azure Custom Vision 은 **2028-09-25 지원 종료 예정**(공식 공지) — 장기적으로 Azure ML AutoML 등으로 전환 권장
