import azure.cognitiveservices.speech as speechsdk

# Azure preliminaries begin
speech_key, service_region = "6ec4bdec3a1341f3a5cb925e616deea2", "uksouth"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Azure preliminaries end


def execute_text_to_speech(input_text):
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = speech_synthesizer.speak_text_async(input_text).get()

    if result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")
