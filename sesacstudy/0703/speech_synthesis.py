'''
  For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk 
'''

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os

load_dotenv()

# Creates an instance of a speech config with specified subscription key and service region.
speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("SERVICE_REGION")

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Note: the voice setting will not overwrite the voice element in input SSML.
# speech_config.speech_synthesis_voice_name = "ko-KR-SeoHyeonNeural"

# text = "배고프다. 빨리 밥 먹으러 가요."

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

ssml_string = open("C:\\Users\\EL066\\sesac\\dev\\sesacstudy\\0703\\ssml.xml", "r", encoding="utf-8").read()
speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_string).get()

stream = speechsdk.AudioDataStream(speech_synthesis_result)
stream.save_to_wav_file("C:\\Users\\EL066\\sesac\\dev\\sesacstudy\\0703\\audiofile.wav")

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
