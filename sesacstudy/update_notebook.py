import json

with open('c:/Users/EL066/sesac/dev/sesacstudy/0703/speech-services/speech-chatbot.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Cell 1: installations
nb['cells'][0]['source'] = [
    "%pip install gradio\n",
    "%pip install python-dotenv\n",
    "%pip install requests\n",
    "%pip install azure-cognitiveservices-speech\n"
]

# Cell 2: code
code = """from dotenv import load_dotenv
import gradio as gr
import os
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

def request_stt(audio_path):
    endpoint_str = os.getenv('ENDPOINT')
    api_key = os.getenv('SPEECH_KEY')

    if audio_path is None:
        return ''

    # The SDK natively supports region
    region = "koreacentral"
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    # Set language to English (en-US)
    speech_config.speech_recognition_language = "en-US"

    # Audio Configuration from file
    audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Recognizing speech...")
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
        return ""
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return ""
    
    return ""

def change_audio(audio_path):
    print("Audio path:", audio_path)
    text = request_stt(audio_path=audio_path)
    return text

with gr.Blocks() as demo:
    gr.Markdown('record data is created')

    with gr.Column(scale=1):
        gr.Markdown('<h3>STT (English)</h3>')
        input_mic = gr.Audio(
            label="마이크 입력", sources=["microphone"], type="filepath", 
            waveform_options = gr.WaveformOptions(
                waveform_color = "#01C6FF",
                waveform_progress_color = "#01C6FF",
                skip_length=2
            )
        )
        output_textbox = gr.Textbox(label="텍스트", placeholder="변환된 텍스트", interactive=False)
        # using change instead of stop_recording is more robust for microphone and clear actions
        input_mic.change(fn=change_audio, inputs=[input_mic], outputs = [output_textbox])

demo.launch()
"""

nb['cells'][1]['source'] = [line + "\n" for line in code.split("\n")]
nb['cells'][1]['source'][-1] = nb['cells'][1]['source'][-1].rstrip('\n')

with open('c:/Users/EL066/sesac/dev/sesacstudy/0703/speech-services/speech-chatbot.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
