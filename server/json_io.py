# json_io.py

from image_initializer import initialize_images
from text_voicer import voice_text_on_image
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route('/')
def home_page():
    return 'Home page!'


@app.route('/init_images_request', methods=['POST'])
def init_images_request():
    global image_blob_lists, image_sizes, url_hash
    
    print('Initializing images...')

    data = request.get_json(force=True)
    url_hash = abs(hash(data['url']))
    image_blob_lists, image_sizes = initialize_images(data['image_urls'], data['image_sizes'], url_hash, data['url'])

    return 'OK'


@app.route('/register_mouse_request', methods=['POST'])
def register_mouse_request():
    
    data = request.get_json(force=True)
    voice_text_on_image(data['id'], data['x'], data['y'], image_blob_lists, image_sizes, url_hash)

    return 'OK'


if __name__ == '__main__':
	app.run()