# json_io.py

from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/')
def home_page():
    return "Home page!"

@app.route('/init_images', methods=['POST'])
def init_images():

    data = request.get_json(force=True)
    # print(data)

    return 'OK'

@app.route('/register_mouse', methods=['POST'])
def register_mouse():
    
    data = request.get_json(force=True)
    # print(data)

    return 'OK'

if __name__ == '__main__':
	# run!
	app.run()