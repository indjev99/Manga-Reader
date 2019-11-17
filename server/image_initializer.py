# image_initializer.py

import azure_text_fetcher
import text_blob_classifier
import numpy as np
import json
import os

from azure_speech_creator import create_speech_file
from azure_translator import translate
from rolling_hash import rolling_hash

SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp']


def check_link(image_url):
    return np.any([(image_format in image_url) for image_format in SUPPORTED_FORMATS])


def extract_blobs(image_url, image_size, in_lang):
    if check_link(image_url) and image_size.width > 5 and image_size.height > 5:
        return text_blob_classifier.analyze_image(azure_text_fetcher.analyze_text(image_url, in_lang))
    else:
        return []


def generate_speech_files(image_blob_list, image_url, in_lang):
    for i in range(len(image_blob_list)):
        if in_lang == 'en': other_lang = 'ja'
        else: other_lang = 'en'
        create_speech_file(image_blob_list[i][0], image_url, i, in_lang, in_lang)
        translation = translate(image_blob_list[i][0], in_lang, other_lang)
        create_speech_file(translation, image_url, i, in_lang, other_lang)


def json_filename(image_url, in_lang):
    url_hash = rolling_hash(image_url)
    return './cache/json/' + str(url_hash) + '_' + in_lang + '.json'


def initialize_image(image_url, image_size, in_lang):
    filename = json_filename(image_url, in_lang)

    if os.path.isfile(filename):
        with open(filename, 'r') as infile:
            data = json.load(infile)
            image_blob_list = data['image_blob_list']
    else:
        image_blob_list = extract_blobs(image_url, image_size, in_lang)
        data = {}
        data['image_url'] = image_url
        data['image_blob_list'] = image_blob_list
        generate_speech_files(image_blob_list, image_url, in_lang)
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)

    return image_blob_list


def initialize_images(image_urls, image_sizes, in_lang):
    image_blob_lists = [initialize_image(image_urls[i], image_sizes[i], in_lang) for i in range(len(image_urls))]
    return image_blob_lists
