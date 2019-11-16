import azure_text_fetcher
import text_blob_classifier


def initialize_images(image_urls):
    blob_list_list = [
        text_blob_classifier.analyze_image(azure_text_fetcher.analyze_text(image_url)) for image_url in image_urls]
    return blob_list_list
