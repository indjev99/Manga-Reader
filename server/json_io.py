# json_io.py

from image_initializer import initialize_images
from text_voicer import voice_text_on_image
from flask import Flask, jsonify, request, render_template
from collections import namedtuple

Size = namedtuple('Size', 'width height')

app = Flask(__name__)

input_language = 'en'
output_language = 'en'


@app.route('/')
def home_page():
    return 'Home page!'


@app.route('/init_images_request', methods=['POST'])
def init_images_request():
    global image_blob_lists, image_urls, image_sizes
    
    print('Initializing images...')

    data = request.get_json(force=True)
    image_urls = data['image_urls']
    image_sizes = [Size(sz['w'], sz['h']) for sz in data['image_sizes']]
    image_blob_lists = initialize_images(image_urls, image_sizes, input_language)

    return 'OK'


@app.route('/register_mouse_request', methods=['POST'])
def register_mouse_request():
    
    data = request.get_json(force=True)
    voice_text_on_image(data['id'], data['x'], data['y'], image_blob_lists, image_urls, image_sizes, input_language, output_language)

    return 'OK'


@app.route('/set_output_language_request', methods=['POST'])
def set_output_language_request():
    global output_language

    data = request.get_json(force=True)
    output_language = data

    return 'OK'

@app.route('/set_input_language_request', methods=['POST'])
def set_input_language_request():
    global input_language, image_blob_lists

    data = request.get_json(force=True)
    input_language = data
    image_blob_lists = initialize_images(image_urls, image_sizes, input_language)

    return 'OK'


if __name__ == '__main__':
    PYTHONHASHSEED = 0
    app.run()