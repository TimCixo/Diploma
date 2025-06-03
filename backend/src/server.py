from flask import Flask, request, jsonify
import subprocess
import os
import threading
import requests
import time

app = Flask(__name__)

# Path to the frontend directory
FRONTEND_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'frontend')

# Simple microcontroller client communicating over HTTP
class Microcontroller:
    def __init__(self, host: str = '192.168.1.50'):
        # Base address of the device on the local network
        self.base_url = f'http://{host}'

    def send_command(self, pin: int, value: int, delay: float = 0):
        payload = {'pin': pin, 'value': value, 'delay': delay}
        try:
            requests.post(f'{self.base_url}/command', json=payload, timeout=2)
        except requests.RequestException as exc:
            # In this simple example we just log errors
            print('Failed to send command:', exc)

microcontroller = Microcontroller()

# In-memory algorithm storage
current_algorithm = []

@app.route('/program', methods=['POST'])
def program():
    """Receive microcontroller config and algorithm."""
    global current_algorithm, microcontroller
    data = request.get_json(force=True)

    if isinstance(data, dict):
        config = data.get('config') or {}
        algo = data.get('algorithm')
    else:
        config = {}
        algo = data

    host = config.get('host')
    if host:
        microcontroller = Microcontroller(host)

    if algo is not None:
        current_algorithm = algo

    return jsonify({'status': 'loaded'})

@app.route('/run', methods=['POST'])
def run_algorithm():
    for step in current_algorithm:
        pin = step.get('pin')
        value = step.get('value')
        delay = step.get('delay', 0)
        microcontroller.send_command(pin, value, delay)
        time.sleep(delay)
    return jsonify({'status': 'completed'})

@app.route('/')
def index():
    return jsonify({'message': 'Server running', 'frontend': 'http://localhost:3000'})

# Helper to start react dev server
def start_react():
    subprocess.Popen(['npm', 'start'], cwd=FRONTEND_PATH)

if __name__ == '__main__':
    threading.Thread(target=start_react, daemon=True).start()
    app.run(debug=True)
