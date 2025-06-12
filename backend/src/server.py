import asyncio
import json
import os
import socket
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import websockets

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Location of the React frontend
FRONTEND_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'frontend')

WS_PORT = 8765
DISCOVERY_PORT = 37020

connected_devices = {}  # device_id -> websocket
known_devices = {}      # device_id -> info dictionary
current_configuration = {}

# ----------------------- HTTP API -----------------------
@app.route('/configuration', methods=['POST'])
def configuration():
    """Store configuration JSON and broadcast it to connected devices."""
    global current_configuration
    current_configuration = request.get_json(force=True) or {}
    message = json.dumps({'configuration': current_configuration})
    for ws in list(connected_devices.values()):
        asyncio.run_coroutine_threadsafe(ws.send(message), ws.loop)
    return jsonify({'status': 'ok'})

@app.route('/devices', methods=['GET'])
def devices():
    return jsonify(list(known_devices.values()))

@app.route('/devices/<device_id>', methods=['GET'])
def device_info(device_id):
    info = known_devices.get(device_id)
    if not info:
        return jsonify({'error': 'not found'}), 404
    return jsonify(info)

@app.route('/')
def index():
    return jsonify({'message': 'backend running'})

# ----------------------- UDP Discovery -----------------------
def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('8.8.8.8', 80))
        ip = sock.getsockname()[0]
    except OSError:
        ip = '127.0.0.1'
    finally:
        sock.close()
    return ip

def discovery_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', DISCOVERY_PORT))
    while True:
        data, addr = sock.recvfrom(1024)
        if data.decode().strip() == 'DISCOVER_MASTER':
            response = json.dumps({'host': get_local_ip(), 'port': WS_PORT})
            sock.sendto(response.encode(), addr)

# ----------------------- WebSocket -----------------------
async def ws_handler(websocket, path):
    try:
        handshake = await websocket.recv()
        info = json.loads(handshake)
        device_id = info.get('id', websocket.remote_address[0])
    except Exception:
        await websocket.close()
        return
    known_devices[device_id] = {'id': device_id, 'ip': websocket.remote_address[0]}
    connected_devices[device_id] = websocket
    if current_configuration:
        await websocket.send(json.dumps({'configuration': current_configuration}))
    try:
        async for _ in websocket:
            pass
    finally:
        connected_devices.pop(device_id, None)
        known_devices.pop(device_id, None)

async def websocket_server():
    async with websockets.serve(ws_handler, '0.0.0.0', WS_PORT):
        await asyncio.Future()

def start_websocket(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_server())

# ----------------------- Frontend Helper -----------------------
def start_react():
    """Ensure dependencies and launch the React development server."""
    if not os.path.exists(os.path.join(FRONTEND_PATH, 'package.json')):
        print("Frontend submodule not found. Did you run 'git submodule update --init --recursive'?", flush=True)
        return

    npm = 'npm.cmd' if os.name == 'nt' else 'npm'
    # Install packages if node_modules folder is missing
    if not os.path.exists(os.path.join(FRONTEND_PATH, 'node_modules')):
        subprocess.run([npm, 'install'], cwd=FRONTEND_PATH, check=False)
    subprocess.Popen([npm, 'run', 'dev'], cwd=FRONTEND_PATH)

if __name__ == '__main__':
    ws_loop = asyncio.new_event_loop()
    threading.Thread(target=start_websocket, args=(ws_loop,), daemon=True).start()
    threading.Thread(target=discovery_server, daemon=True).start()
    threading.Thread(target=start_react, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
