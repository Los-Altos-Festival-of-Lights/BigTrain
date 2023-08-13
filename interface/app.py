from flask import Flask, render_template, jsonify, request
import os, requests

app = Flask(__name__)

# Replace these values with your FalconPlayer API endpoints
FALCON_PLAYER_BASE_URL = "http://" + os.environ.get('FALCON_IP', '10.2.0.1') + "/api/"
STATUS_ENDPOINT = 'fppd/status'
SEQUENCES_ENDPOINT = 'playlists/playable'
STOP_ENDPOINT = 'playlists/stop'
VOLUME_ENDPOINT = 'fppd/volume'
MUTE_ENDPOINT = 'system/volume'
SHUTDOWN_ENDPOINT = 'system/shutdown'

selected_sequence = ""


def send_request(endpoint, method, jsonify=True, **kwargs):
    try:
        if method == "get":
            response = requests.get(FALCON_PLAYER_BASE_URL + endpoint, timeout=5, **kwargs)
        else:
            response = requests.post(FALCON_PLAYER_BASE_URL + endpoint, timeout=5, **kwargs)
        if jsonify:
            return response.status_code, response.json()
        else:
            return response.status_code, response

    except requests.exceptions.RequestException as e:
        return 500, {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def status():
    status_code, response = send_request(STATUS_ENDPOINT, "get")
    if status_code == 500:
        # response = {"status": "Playing", "sequence": "HEHEE.fseq"}
        response = {"status": "Not Connected"}
    elif status_code == 200 and response["status_name"] == "idle":
        response = {"status": "Ready"}
    elif status_code == 200 and response["status_name"] == "playing":
        response = {"status": "Playing", "sequence": response["current_sequence"]}
    return jsonify(response), status_code

@app.route('/api/sequences', methods=['GET'])
def sequences():
    status_code, response = send_request(SEQUENCES_ENDPOINT, "get")
    return jsonify(response), status_code

@app.route('/api/play', methods=['POST'])
def play():
    res = request.get_json(force=True)
    selected_sequence = res.get("sequence")
    schema = {"command":"Start Playlist At Item","args":[selected_sequence,1,True,False]}
    print(schema)
    status_code, response = send_request(f"command", "post", False, json=schema)
    return jsonify(str(response)), status_code

@app.route('/api/stop', methods=['POST'])
def stop():
    status_code, response = send_request(STOP_ENDPOINT, "get", False)
    return jsonify(str(response)), status_code

@app.route('/api/mute', methods=['POST'])
def mute():
    status_code, response = send_request(VOLUME_ENDPOINT, "get")
    if response["volume"] != 0:
        status_code, response = send_request(MUTE_ENDPOINT, "post", data={"volume": 0})
    else:
        status_code, response = send_request(MUTE_ENDPOINT, "post", data={"volume": 100})
    return jsonify(response), status_code

@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    status_code, response = send_request(SHUTDOWN_ENDPOINT, "get")
    return jsonify(response), status_code