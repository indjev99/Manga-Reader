# azure_translator.py

import os, requests, uuid, json

subscription_key = '31d329dea86649d9a7465195ff72d1a7'
endpoint = 'https://api.cognitive.microsofttranslator.com'
path = '/translate?api-version=3.0'


headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}


def translate(text, source, dest):
    params = '&from=' + source + '&to=' + dest
    constructed_url = endpoint + path + params
    body = [{
        'text': text
    }]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    return response[0]['translations'][0]['text']