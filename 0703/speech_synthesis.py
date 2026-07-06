'''
  For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk 
'''

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

# 이 스크립트가 있는 폴더 기준 경로 (사용자/절대경로 하드코딩 제거)
BASE_DIR = Path(__file__).resolve().parent

# Creates an instance of a speech config with specified subscription key and service region.
speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("SERVICE_REGION")

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Note: the voice setting will not overwrite the voice element in input SSML.
# speech_config.speech_synthesis_voice_name = "ko-KR-SeoHyeonNeural"

# text = "배고프다. 빨리 밥 먹으러 가요."

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

ssml_string = open(BASE_DIR / "ssml.xml", "r", encoding="utf-8").read()
speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_string).get()

stream = speechsdk.AudioDataStream(speech_synthesis_result)
stream.save_to_wav_file(str(BASE_DIR / "audiofile.wav"))

# # use the default speaker as audio output.
# speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# result = speech_synthesizer.speak_text_async(text).get()
# # Check result
# if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#     print("Speech synthesized for text [{}]".format(text))
# elif result.reason == speechsdk.ResultReason.Canceled:
#     cancellation_details = result.cancellation_details
#     print("Speech synthesis canceled: {}".format(cancellation_details.reason))
#     if cancellation_details.reason == speechsdk.CancellationReason.Error:
#         print("Error details: {}".format(cancellation_details.error_details))
