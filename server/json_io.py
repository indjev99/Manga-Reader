# json_io.py

from image_initializer import initialize_images
from text_voicer import voice_text_on_image

from flask import Flask, jsonify, request, render_template
app = Flask(__name__)


@app.route('/')
def home_page():
    return "Home page!"


@app.route('/init_images_request', methods=['POST'])
def init_images_request():

    data = request.get_json(force=True)
    initialize_images(data)

    return 'OK'


@app.route('/register_mouse_request', methods=['POST'])
def register_mouse_request():
    
    data = request.get_json(force=True)
    voice_text_on_image(data['id'], data['x'], data['y'])

    return 'OK'


if __name__ == '__main__':
	app.run()