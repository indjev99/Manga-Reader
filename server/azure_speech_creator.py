# azure_speech_creator.py

import azure.cognitiveservices.speech as speechsdk

from playsound import playsound
from rolling_hash import rolling_hash

# Azure preliminaries begin
speech_key, service_region = '6ec4bdec3a1341f3a5cb925e616deea2', 'uksouth'
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Azure preliminaries end


def speech_filename(image_url, blob_id, lang):
    url_hash = rolling_hash(image_url)
    return './cache/speech/' + str(url_hash) + '_' + str(blob_id) + '_' + lang + '.wav'


def create_speech_file(input_text, image_url, blob_id, lang):
    audio_output = speechsdk.AudioOutputConfig(filename=speech_filename(image_url, blob_id, lang))
    if (lang == 'ja'): speech_config.speech_synthesis_language = 'ja-JP'
    else: speech_config.speech_synthesis_language = 'en-UK'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)
    result = speech_synthesizer.speak_text_async(input_text).get()


def play_speech_file(image_url, blob_id, lang):
    playsound(speech_filename(image_url, blob_id, lang))