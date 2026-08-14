import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Configuration for backend URLs
BACKEND_LIST_URL = "http://172.17.0.4:8001/list-files"
BACKEND_UPLOAD_URL = "http://172.17.0.3:8002/upload-file"

@app.route("/")
def index():
    """Renders the main page."""
    return render_template("index.html")

@app.route("/api/list-files", methods=["GET"])
def api_list_files():
    """API endpoint to trigger file listing from the backend."""
    try:
        response = requests.get(BACKEND_LIST_URL)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Failed to fetch files. Status: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/upload-file", methods=["POST"])
def api_upload_file():
    """API endpoint to handle file uploads from the frontend."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        try:
            # Forward the file to the backend upload service
            files = {'file': (file.filename, file.stream, file.content_type)}
            response = requests.post(BACKEND_UPLOAD_URL, files=files)
            
            if response.status_code == 200:
                return jsonify(response.json())
            else:
                return jsonify({"error": f"Failed to upload file. Status: {response.status_code}"}), response.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=8003, debug=True)
