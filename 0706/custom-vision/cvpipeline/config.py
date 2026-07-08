"""환경변수 로드와 Custom Vision 클라이언트/상수 정의.

키·엔드포인트는 코드에 하드코딩하지 않고 같은 폴더의 .env 에서 읽는다(python-dotenv).
"""
import os
from dotenv import load_dotenv
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

load_dotenv()

# --- .env 에서 읽는 자격증명/엔드포인트 ---
TRAINING_ENDPOINT = os.getenv("VISION_TRAINING_ENDPOINT")
PREDICTION_ENDPOINT = os.getenv("VISION_PREDICTION_ENDPOINT")
TRAINING_KEY = os.getenv("VISION_TRAINING_KEY")
PREDICTION_KEY = os.getenv("VISION_PREDICTION_KEY")
PREDICTION_RESOURCE_ID = os.getenv("VISION_PREDICTION_RESOURCE_ID")

# --- 프로젝트 상수 ---
# 프로젝트 학습 큐가 백엔드에서 wedge 되는 사례가 있어(진행중 이터레이션 삭제 후에도 후속
# 학습이 전부 hang), 환경변수로 프로젝트명을 바꿔 '새 프로젝트'로 우회할 수 있게 한다.
# 주의: 포털에서 만든 프로젝트를 지정할 땐 도메인이 'ObjectDetection' 이어야 한다
# (Classification 프로젝트는 생성 후 타입 변경 불가 — project_setup 에서 검증해 조기 실패).
PROJECT_ID = os.getenv("VISION_PROJECT_ID")  # 지정 시 이름 검색 대신 이 ID 를 그대로 사용
PROJECT_NAME = os.getenv("VISION_PROJECT_NAME", "sesac015-customvision")
PUBLISH_ITERATION_NAME = os.getenv("VISION_PUBLISH_NAME", "sesac015-object-detection-v1")

# 이미지 루트: 이 패키지의 부모 폴더(custom-vision/) 아래 Images/
BASE_IMAGE_LOCATION = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Images"
)


def make_trainer():
    """학습(Training) 클라이언트를 생성한다."""
    credentials = ApiKeyCredentials(in_headers={"Training-key": TRAINING_KEY})
    return CustomVisionTrainingClient(TRAINING_ENDPOINT, credentials)


def make_predictor():
    """예측(Prediction) 클라이언트를 생성한다."""
    credentials = ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY})
    return CustomVisionPredictionClient(PREDICTION_ENDPOINT, credentials)
