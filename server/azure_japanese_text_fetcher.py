# azure_japanese_text_fetcher.py

import requests

# AZURE preliminaries BEGIN
subscription_key = 'da819e01c47543acba4d2ab761442f18'

endpoint = 'https://mangaplus.cognitiveservices.azure.com/'
headers = {'Ocp-Apim-Subscription-Key': subscription_key}
params = {'language': 'ja', 'detectOrientation': 'true'}
ocr_url = endpoint + 'vision/v2.1/ocr'
# AZURE preliminaries END


def analyze_japanese_text(image_url):
    data = {'url': image_url}
    response = requests.post(ocr_url, headers=headers, params=params, json=data)
    response.raise_for_status()

    analysis = response.json()

    line_infos = [region['lines'] for region in analysis['regions']]
    word_infos = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata['words']:
                word_infos.append(word_info)

    text_boxes = []
    for word in word_infos:
        bbox_info = [int(num) for num in word['boundingBox'].split(',')]
        text = word['text']
        bbox = [bbox_info[0], bbox_info[1],
                bbox_info[0] + bbox_info[2], bbox_info[1],
                bbox_info[0] + bbox_info[2], bbox_info[1] + bbox_info[3],
                bbox_info[0], bbox_info[1] + bbox_info[3]]

        text_boxes.append((text, bbox))

    return text_boxes
