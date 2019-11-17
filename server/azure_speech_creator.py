# azure_speech_creator.py

import azure.cognitiveservices.speech as speechsdk

from playsound import playsound

# Azure preliminaries begin
speech_key, service_region = '6ec4bdec3a1341f3a5cb925e616deea2', 'uksouth'
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Azure preliminaries end


def speech_filename(url_hash, image_id, blob_id):
    return './cache/speech/' + str(url_hash) + '_' + str(image_id) + '_' + str(blob_id) + '.wav'


def create_speech_file(input_text, url_hash, image_id, blob_id):
    audio_output = speechsdk.AudioOutputConfig(filename=speech_filename(url_hash, image_id, blob_id))
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)
    result = speech_synthesizer.speak_text_async(input_text).get()


def play_speech_file(url_hash, image_id, blob_id):
    playsound(speech_filename(url_hash, image_id, blob_id))
