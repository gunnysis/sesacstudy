import requests
import json
from dataclasses import dataclass
from typing import List, Optional
import dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import image as mpimg


# .env 를 스크립트 위치 기준으로 로드 (cwd 가 어디든 동작)
_ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
loaded_env = dotenv.load_dotenv(dotenv_path=_ENV_PATH)

# Image Analysis 4.0 REST API 버전 (공식 문서 기준 GA)
API_VERSION = os.getenv("API_VERSION")

@dataclass
class Metadata:
    width: int
    height: int

@dataclass
class BoundingBox:
    x: int
    y: int
    w: int
    h: int

@dataclass
class Tag:
    name: str
    confidence: float

@dataclass
class Value:
    boundingBox: BoundingBox
    tags: List[Tag]

@dataclass
class ObjectsResult:
    values: List[Value]

@dataclass
class AnalyzeResult:
    modelVersion: str
    metadata: Metadata
    objectsResult: ObjectsResult

class ObjectDetection:
    def detect_object(self, image_path: Optional[str] = None, features: str = "objects"):
        """로컬 이미지 파일을 Azure Image Analysis 4.0 으로 분석한다.

        공식 문서: call-analyze-image-40 (REST API)
        - 로컬 이미지: 바이너리 본문 + Content-Type: application/octet-stream
        - 원격 이미지(URL): JSON 본문 {"url": ...} + Content-Type: application/json
        """
        # Azure 포털의 Computer Vision 리소스에서 엔드포인트/키 확인
        endpoint = os.getenv("END_POINT")  # Retrieve the endpoint from environment variables
        key = os.getenv("API_KEY")  # Retrieve the API key from environment variables

        if not endpoint or not key:
            raise RuntimeError(
                f".env 로드 실패 또는 값 누락 (loaded={loaded_env}, path={_ENV_PATH}). "
                "END_POINT / API_KEY 를 확인하세요."
            )
        # endpoint 끝에 슬래시가 없으면 붙여준다
        if not endpoint.endswith("/"):
            endpoint += "/"

        # <endpoint>/computervision/imageanalysis:analyze?api-version=...&features=...
        url = (
            f"{endpoint}computervision/imageanalysis:analyze"
            f"?api-version={API_VERSION}&features={features}"
        )

        # 분석할 로컬 이미지
        image_name="image.jpg"
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), image_name)
        # 시각화에서 다시 열 수 있도록 경로를 보관해 둔다
        self._image_path = image_path

        # (공식 문서: 로컬 이미지의 Content-Type 은 application/octet-stream)
        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Content-Type': 'application/octet-stream'
        }

        with open(image_path, "rb") as f:
            image_bytes = f.read()

        response = requests.post(url, headers=headers, data=image_bytes)

        # 오류 응답이면 상태코드와 함께 내용을 그대로 보여준다
        if not response.ok:
            print(f"요청 실패 (HTTP {response.status_code}): {response.text}")
            response.raise_for_status()

        response_content = response.text

        # Print the JSON response for debugging
        print(f"Response Content: {response_content}")
        # json_response = json.loads(response_content)
        #print(f"JSON Response: {json_response}")




        # Deserialize and print the result
        data = json.loads(response_content)
        try:
            deserialized_object = self.from_dict(AnalyzeResult, data)

            print(f"Model Version: {deserialized_object.modelVersion}")
            print(f"Metadata - Width: {deserialized_object.metadata.width}, Height: {deserialized_object.metadata.height}")
            for value in deserialized_object.objectsResult.values:
                print(f"BoundingBox - X: {value.boundingBox.x}, Y: {value.boundingBox.y}, Width: {value.boundingBox.w}, Height: {value.boundingBox.h}")
                for tag in value.tags:
                    print(f"Tag - Name: {tag.name}, Confidence: {tag.confidence}")

            # 텍스트 출력 대신(또는 함께) 탐지 결과를 이미지 위에 그려서 보여준다
            self.visualize(deserialized_object)

        except KeyError as e:
            print(f"KeyError: {e}. Please check the JSON response structure.")

    def visualize(self, result):
        """탐지된 객체의 바운딩 박스와 태그를 원본 이미지 위에 그린다."""
        img = mpimg.imread(self._image_path)

        _, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(img)
        ax.set_title(f"Object Detection ({len(result.objectsResult.values)} objects)")
        ax.axis("off")

        for value in result.objectsResult.values:
            box = value.boundingBox
            # 사각형 박스 그리기
            rect = patches.Rectangle(
                (box.x, box.y), box.w, box.h,
                linewidth=2, edgecolor="lime", facecolor="none",
            )
            ax.add_patch(rect)

            # 가장 신뢰도 높은 태그를 라벨로 표시
            if value.tags:
                top = max(value.tags, key=lambda t: t.confidence)
                label = f"{top.name} {top.confidence:.0%}"
                ax.text(
                    box.x, box.y - 5, label,
                    color="black", fontsize=10, fontweight="bold",
                    bbox=dict(facecolor="lime", edgecolor="none", pad=2),
                )

        plt.tight_layout()
        # 결과를 PNG 로 저장하고 창으로도 띄운다
        out_path = os.path.join(os.path.dirname(self._image_path), "object_detection.png")
        plt.savefig(out_path, dpi=150, bbox_inches="tight")
        print(f"시각화 저장: {out_path}")
        plt.show()

    def from_dict(self, data_class, data):
        if isinstance(data, list):
            return [self.from_dict(data_class.__args__[0], item) for item in data]
        if isinstance(data, dict):
            fieldtypes = {f.name: f.type for f in data_class.__dataclass_fields__.values()}
            return data_class(**{k: self.from_dict(fieldtypes[k], v) for k, v in data.items()})
        return data

# Usage example
if __name__ == "__main__":
    objectDetection = ObjectDetection()
    objectDetection.detect_object()
