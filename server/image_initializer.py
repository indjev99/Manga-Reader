# image_initializer.py

import azure_text_fetcher
import text_blob_classifier
import numpy as np
import json
import os

from collections import namedtuple
from azure_speech_creator import create_speech_file

SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp']
Size = namedtuple('Size', 'width height')


def check_link(image_url):
    return np.any([(image_format in image_url) for image_format in SUPPORTED_FORMATS])


def extract_blobs(image_url, image_size):
    if check_link(image_url) and image_size.width > 5 and image_size.height > 5:
        return text_blob_classifier.analyze_image(azure_text_fetcher.analyze_text(image_url))
    else:
        return []


def generate_speech_files(image_blob_list, image_url):
    for i in range(len(image_blob_list)):
        create_speech_file(image_blob_list[i][0], image_url, i)


def json_filename(image_url):
    url_hash = abs(hash(image_url[15:]))
    return './cache/json/' + str(url_hash) + '.json'


def initialize_image(image_url, image_size):
    filename = json_filename(image_url)

    if os.path.isfile(filename):
        with open(filename, 'r') as infile:
            data = json.load(infile)
            image_blob_list = data['image_blob_list']
    else:
        image_blob_list = extract_blobs(image_url, image_size)
        data = {}
        data['image_url'] = image_url
        data['image_blob_list'] = image_blob_list
        generate_speech_files(image_blob_list, image_url)
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)

    return image_blob_list


def initialize_images(image_urls, image_szs):
    image_sizes = [Size(sz['w'], sz['h']) for sz in image_szs]
    image_blob_lists = [initialize_image(image_urls[i], image_sizes[i]) for i in range(len(image_urls))]
    return image_blob_lists, image_sizes
