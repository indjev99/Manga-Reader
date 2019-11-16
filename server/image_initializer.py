import azure_text_fetcher
import text_blob_classifier
import numpy as np

SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp']


def check_link(image_url):
    global SUPPORTED_FORMATS
    return np.any([(image_format in image_url) for image_format in SUPPORTED_FORMATS])


def initialize_images(image_urls):
    blob_list_list = [
        text_blob_classifier.analyze_image(azure_text_fetcher.analyze_text(image_url))
        for image_url in image_urls if check_link(image_url)]
    return blob_list_list
