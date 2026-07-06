import requests
import gradio as gr
import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import random

load_dotenv()

endpoint = os.environ.get("END_POINT")
api_key = os.environ.get("API_KEY")

def request_vision_model(type, img_path):
    url = f"{endpoint}computervision/imageanalysis:analyze?features=denseCaptions&gender-neutral-caption=false&api-version=2023-10-01"

    if type == "Object Detection":
        print("called: Object Detection")
        url = f"{endpoint}computervision/imageanalysis:analyze?features=objects&api-version=2023-10-01"

    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Content-Type': 'application/octet-stream'
    }

    with open(img_path, "rb") as f:
        img_data = f.read()
        response = requests.post(url, headers=headers, data=img_data)

        print(response.status_code)

        if response.status_code != 200:
            print("에러 발생함")
            return None
        
        return response

def draw_image(img_path, polygons):
    image = Image.open(img_path)
    draw = ImageDraw.Draw(image)
    font_path = "arial.ttf" 
    font_size = 16
    font = ImageFont.truetype(font_path, font_size)

    for polygon in polygons:
        color = random_color()
        bounding_box = polygon['boundingBox']
        poligon_point_list = [(bounding_box['x'], bounding_box['y']), (bounding_box['x'] + bounding_box['w'], bounding_box['y']), (bounding_box['x'] + bounding_box['w'], bounding_box['y'] + bounding_box['h']), (bounding_box['x'], bounding_box['y'] + bounding_box['h'])]
        print(f"poligon_point_list: {poligon_point_list}")
        content = polygon['content']
        print(f"content: {content}")
        draw.polygon(poligon_point_list, outline=color, width=2)
        draw.text((bounding_box['x'], bounding_box['y']- 20), content, fill=color, font=font)

    return image

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def detect_object(img_path):
    response = request_vision_model("Object Detection", img_path)

    json_data = response.json()
    print(f"{json_data}")

    objects_result_first_value = json_data['objectsResult']['values'][0]
    print(f"{objects_result_first_value}")

    tags = objects_result_first_value['tags'][0]
    
    polygons = [{
        "boundingBox": objects_result_first_value['boundingBox'],
        "content": f"{tags['name']} ({tags['confidence']})"
    }]

    image = draw_image(img_path, polygons)

    return image

def dense_caption(img_path):
    response = request_vision_model("Dense Caption", img_path)

    json_data = response.json()
    print(f"{json_data}")

    dense_captions_result_values = json_data['denseCaptionsResult']['values']
    print(f"denseCaptionsResult Values: {dense_captions_result_values}")

    polygons = [{
        "boundingBox": item["boundingBox"],
        "content": f"{item['text']}{item['confidence']}"  # 문자열 결합
    }
    for item in dense_captions_result_values
    ]

    print(f"polygons: {polygons}")

    image = draw_image(img_path, polygons)

    return image

def main():
    if endpoint is None:
        print("endpoint is not set!")
        return

    if api_key is None:
        print("api is not set!")
        return

    # print(f"endpoint: {endpoint}")
    # print(f"api key: {api_key}")

    with gr.Blocks() as demo:
        with gr.Tab("Object Detection"):
            with gr.Row():
                object_img = gr.Image(label="이미지", type="filepath", width=500)
                detect_result = gr.Image(label="분석 결과", type="pil", width=500)

                object_img.change(fn=detect_object, inputs=object_img, outputs=detect_result)
        with gr.Tab("Dense Caption"):
            with gr.Row():
                caption_img = gr.Image(label="이미지", type="filepath", width=500)
                caption_result = gr.Image(label="분석 결과", type="pil", width=500)

                caption_img.change(fn=dense_caption, inputs=caption_img, outputs=caption_result)

        demo.launch()

main()