# image_initializer.py

import azure_text_fetcher
import text_blob_classifier
from collections import namedtuple
import numpy as np

SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp']
Size = namedtuple('Size', 'width height')

def check_link(image_url):
    return np.any([(image_format in image_url) for image_format in SUPPORTED_FORMATS])


def extract_blobs(image_url):
    if check_link(image_url):
        return text_blob_classifier.analyze_image(azure_text_fetcher.analyze_text(image_url))
    else:
        return []


def initialize_images(image_urls, image_szs):
    image_blob_lists = [extract_blobs(image_url) for image_url in image_urls]
    image_sizes = [Size(sz['w'], sz['h']) for sz in image_szs]
    return image_blob_lists, image_sizes
