# azure_text_fetcher.py

import time

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

# AZURE preliminaries BEGIN
subscription_key = 'da819e01c47543acba4d2ab761442f18'
endpoint = 'https://mangaplus.cognitiveservices.azure.com/'
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

vision_base_url = 'https://uksouth.api.cognitive.microsoft.com/vision/v2.0/'
analyze_url = vision_base_url + "analyze"
# AZURE preliminaries END


def analyze_text(image_url):

    recognize_printed_results = computervision_client.batch_read_file(image_url, raw=True)

    operation_location_remote = recognize_printed_results.headers["Operation-Location"]
    operation_id = operation_location_remote.split("/")[-1]

    while True:
        printed_text_results = computervision_client.get_read_operation_result(operation_id)
        if printed_text_results.status not in ['NotStarted', 'Running']:
            break
        time.sleep(1)

    text_boxes = []
    if printed_text_results.status == TextOperationStatusCodes.succeeded:
        for text_result in printed_text_results.recognition_results:
            for line in text_result.lines:
                text_boxes.append((line.text, line.bounding_box))

    return text_boxes

