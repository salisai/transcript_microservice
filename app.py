from flask import Flask, jsonify 
from flask_cors import CORS 
from routes.transcript import bp 
from utils.errors import TranscriptError

app = Flask(__name__)
# attach cors middleware 
CORS(app)

app.register_blueprint(bp)

# centralized error handling 
@app.errorhandler(TranscriptError)
def handle_custom_error(e):
    return jsonify({
        "error": {
            "code": e.code,
            "message": e.message
        }
    }), e.status_code

@app.errorhandler(404)
def handle_not_found(e):
    return jsonify({
        "error": {
            "code": "NOT_FOUND",
            "message": "The requested endpoint was not found"
        }
    }), 404

@app.errorhandler(500)
def handle_internal_error(e):
    return jsonify({
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "An internal server error occurred"
        }
    }), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)