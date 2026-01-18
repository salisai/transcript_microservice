from flask import Flask, jsonify 
from flask_cors import CORS 
from routes.transcript import bp 
from utils.errors import TranscriptError

app = Flask(__name__)
CORS(app)

app.register_blueprint(bp)

@app.errorhanlder(TranscriptError)
def handle_custom_error(e):
    return jsonify({
        "error": {
            "code": e.code,
            "message": e.message
        }
    })