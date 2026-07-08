"""예측 + 바운딩 박스 시각화(matplotlib)."""
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from .config import PUBLISH_ITERATION_NAME

# 한글 제목이 깨지지 않도록 Windows 기본 한글 폰트 지정
matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

TAG_COLORS = {"fork": "lime", "scissors": "cyan", "glasses": "yellow"}  # 태그별 바운딩 박스 색상


def predict_and_visualize(predictor, project, test_image_path, output_dir, prob_threshold):
    """이미지 1장을 예측하고 바운딩 박스를 그려 output_dir/prediction_<원본이름>.png 로 저장한다.

    출력은 입력(test)과 섞이지 않도록 별도 폴더(Images/predictions/)에 저장한다.
    """
    name = os.path.basename(test_image_path)
    print(f"\n=== 예측: {name} ===")

    with open(test_image_path, mode="rb") as test_data:
        results = predictor.detect_image(project.id, PUBLISH_ITERATION_NAME, test_data)

    for prediction in results.predictions:
        print("\t" + prediction.tag_name + ": {0:.2f}% bbox.left = {1:.2f}, bbox.top = {2:.2f}, bbox.width = {3:.2f}, bbox.height = {4:.2f}".format(
            prediction.probability * 100, prediction.bounding_box.left, prediction.bounding_box.top,
            prediction.bounding_box.width, prediction.bounding_box.height))

    img = Image.open(test_image_path)
    img_w, img_h = img.size

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(img)
    ax.axis("off")

    drawn = 0
    for prediction in results.predictions:
        if prediction.probability < prob_threshold:
            continue
        bb = prediction.bounding_box
        # 정규화 좌표(0~1) -> 픽셀 좌표
        left, top = bb.left * img_w, bb.top * img_h
        width, height = bb.width * img_w, bb.height * img_h
        color = TAG_COLORS.get(prediction.tag_name, "red")

        rect = patches.Rectangle((left, top), width, height, linewidth=3, edgecolor=color, facecolor="none")
        ax.add_patch(rect)
        ax.text(left, max(top - 8, 0),
                f"{prediction.tag_name} {prediction.probability * 100:.1f}%",
                color="black", fontsize=12, fontweight="bold",
                bbox=dict(facecolor=color, alpha=0.8, edgecolor="none", pad=2))
        drawn += 1

    ax.set_title(f"{name}  (>= {int(prob_threshold * 100)}%, {drawn}건)", fontsize=13)
    plt.tight_layout()

    stem = os.path.splitext(name)[0]
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"prediction_{stem}.png")
    fig.savefig(output_path, dpi=120, bbox_inches="tight")
    print(f"시각화 저장: {output_path} (표시 {drawn}건 / 전체 {len(results.predictions)}건)")
