from flask import Flask, send_from_directory, make_response

app = Flask(__name__)

@app.route('/')
def index():
    response = make_response(send_from_directory('.', 'index.html'))
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    return response

@app.route('/<path:path>')
def serve_file(path):
    response = make_response(send_from_directory('.', path))
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    return response

app.run(host='0.0.0.0', port=8000)