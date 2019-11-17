# image_initializer.py

import azure_text_fetcher
import text_blob_classifier
import numpy as np
import json
import os

from collections import namedtuple
from azure_speech_creator import create_speech_file

SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp']


def check_link(image_url):
    return np.any([(image_format in image_url) for image_format in SUPPORTED_FORMATS])


def extract_blobs(image_url):
    if check_link(image_url):
        return text_blob_classifier.analyze_image(azure_text_fetcher.analyze_text(image_url))
    else:
        return []


def generate_speech_files(image_blob_lists, url_hash):
    for i in range(len(image_blob_lists)):
        for j in range(len(image_blob_lists[i])):
            create_speech_file(image_blob_lists[i][j][0], url_hash, i, j)


def json_filename(url_hash):
    return './cache/json/' + str(url_hash) + '.json'


def initialize_images(image_urls, image_szs, url_hash, url):
    filename = json_filename(url_hash)
    if os.path.isfile(filename):
        with open(filename, 'r') as infile:
            data = json.load(infile)
            image_blob_lists = data['image_blob_lists']
            image_sizes = data['image_sizes']
    else:
        image_blob_lists = [extract_blobs(image_url) for image_url in image_urls]
        image_sizes = [[sz['w'], sz['h']] for sz in image_szs]
        generate_speech_files(image_blob_lists, url_hash)

        data = {}
        data['url'] = url
        data['image_blob_lists'] = image_blob_lists
        data['image_sizes'] = image_sizes
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)

    return image_blob_lists, image_sizes
