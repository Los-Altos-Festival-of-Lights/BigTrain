from flask import Flask, render_template, jsonify, request
import os, requests

app = Flask(__name__)

# Replace these values with your FalconPlayer API endpoints
FALCON_PLAYER_BASE_URL = "http://" + os.environ.get('FALCON_IP', '10.2.0.1') + "/"
STATUS_ENDPOINT = 'fppd/status'
SEQUENCES_ENDPOINT = 'playlists/playable'
STOP_ENDPOINT = 'playlists/stop'
MUTE_ENDPOINT = 'system/volume'
SHUTDOWN_ENDPOINT = 'system/shutdown'

selected_sequence = ""

def send_request(endpoint, **kwargs):
    try:
        response = requests.post(FALCON_PLAYER_BASE_URL + endpoint, **kwargs)
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return 500, {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def status():
    status_code, response = send_request(STATUS_ENDPOINT)
    if status_code == 500:
        response = "Not Connected"
    elif status_code == 200 and response["status"]["name"] == "idle":
        response = "Ready"
    elif status_code == 200 and response["status"]["name"] == "playing":
        response = "Playing " + response["current_sequence"]
    return jsonify(response), status_code

@app.route('/api/sequences', methods=['GET'])
def sequences():
    status_code, response = send_request(SEQUENCES_ENDPOINT)
    return jsonify(response), status_code

@app.route('/api/select_sequence', methods=['POST'])
def select_sequence():
    selected_sequence = request.form.get()
    return jsonify(selected_sequence), 200

@app.route('/api/play', methods=['POST'])
def start():
    status_code, response = send_request(f"playlist/{selected_sequence}/start")
    return jsonify(response), status_code

@app.route('/api/stop', methods=['GET'])
def stop():
    status_code, response = send_request(STOP_ENDPOINT)
    return jsonify(response), status_code

@app.route('/api/mute', methods=['POST'])
def mute():
    status_code, response = send_request(MUTE_ENDPOINT, data={"volume": 0})
    return jsonify(response), status_code

@app.route('/api/shutdown', methods=['GET'])
def shutdown():
    status_code, response = send_request(SHUTDOWN_ENDPOINT)
    return jsonify(response), status_code