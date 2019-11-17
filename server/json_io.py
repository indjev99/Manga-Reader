# json_io.py

from image_initializer import initialize_images
from text_voicer import voice_text_on_image
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route('/')
def home_page():
    return 'Home page!'


input_language = 'en'
output_language = 'en'

@app.route('/init_images_request', methods=['POST'])
def init_images_request():
    global image_blob_lists, image_urls, image_sizes
    
    print('Initializing images...')

    data = request.get_json(force=True)
    image_urls = data['image_urls']
    image_blob_lists, image_sizes = initialize_images(image_urls, data['image_sizes'])

    return 'OK'


@app.route('/register_mouse_request', methods=['POST'])
def register_mouse_request():
    
    data = request.get_json(force=True)
    voice_text_on_image(data['id'], data['x'], data['y'], image_blob_lists, image_urls, image_sizes, output_language)

    return 'OK'


@app.route('/set_output_language_request', methods=['POST'])
def set_output_language_request():
    global output_language

    data = request.get_json(force=True)
    output_language = data

    return 'OK'


if __name__ == '__main__':
    PYTHONHASHSEED = 0
    app.run()