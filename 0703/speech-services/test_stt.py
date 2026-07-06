import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()
api_key = os.getenv('SPEECH_KEY')
region = os.getenv('REGION', 'koreacentral')

speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)

# Create a dummy audio config that doesn't actually use mic or file, just to test auth
# Actually we can just use default microphone or a non-existent file, it will fail on file not found
# To test auth we need a real connection. We can use a push stream
stream = speechsdk.audio.PushAudioInputStream()
audio_config = speechsdk.audio.AudioConfig(stream=stream)

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
print("Connecting...")
result = speech_recognizer.recognize_once_async().get()

print(f"Reason: {result.reason}")
if result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print(f"Cancellation Reason: {cancellation_details.reason}")
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print(f"Error details: {cancellation_details.error_details}")
