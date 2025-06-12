# Remote Microcontroller Management System
<img src="https://github.com/user-attachments/assets/8d5e995b-b206-477a-bcdd-f1b7938c5cc6" width="250px" align="right">

A system designed for remote control and configuration of microcontrollers. It consists of two main components: a microcontroller and a web interface. 

The microcontroller executes server instructions and interacts with connected components, while the web interface allows users to configure settings, manage firmware, and design workflows through a visual interface. This solution provides flexibility and simplicity for managing electronic systems remotely.

## Wi-Fi communication

The backend communicates with the microcontroller over the local network. On startup you specify the device IP when uploading the program. Each algorithm step is sent to the microcontroller as an HTTP request, so both devices must be connected to the same Wi‑Fi network.

## Running the backend and frontend

1. Create and activate a virtual environment and install the Python dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows use venv\Scripts\activate
   pip install -r backend/requirements.txt
   ```
2. From the repository root, run the server:
   ```bash
   python backend/src/server.py
   ```
   The server will automatically start the React development server and provide a link to `http://localhost:3000`.

3. Upload the microcontroller program:
   - `POST /configuration` – send the workflow configuration in JSON format. A typical payload looks like:
   ```json
   {
       "entry": "node_0",
       "exit": "node_4",
       "pins": {
           "Push Button": {"pin": 2, "direction": "input"},
           "Potentiometer": {"pin": 5, "direction": "input"},
           "Piezo Buzzer": {"pin": 9, "direction": "output"}
       },
       "constants": {},
       "variables": {
           "hardware_11: Signal": 0,
           "hardware_12: Wiper": 0
       },
       "nodes": [
           {"id": "node_0", "type": "input", "outputs": ["node_4", "node_2", "node_3"]},
           {"id": "node_1", "type": "output", "outputs": []},
           {
               "id": "node_2",
               "type": "input_component",
               "outputs": {"variable": "var_hardware_11: Signal"},
               "pins": {"pin1": 2}
           },
           {
               "id": "node_3",
               "type": "input_component",
               "outputs": {"variable": "var_hardware_12: Wiper"},
               "pins": {"pin1": 5}
           },
           {
               "id": "node_4",
               "type": "output_component",
               "outputs": ["node_1"],
               "pins": {"pin1": 9},
               "params": {}
           }
       ]
   }
   ```
   All connected devices will immediately receive this configuration over the WebSocket connection.


## Backend API

- `POST /configuration` – upload the microcontroller algorithm configuration in JSON.
- `GET /devices` – list microcontrollers discovered on the local network.
- `GET /devices/<id>` – information about a specific device.

The server listens for UDP broadcasts with the `DISCOVER_MASTER` message and
responds with its IP address and WebSocket port so that ESP32 devices can find
it. After discovery a device connects via WebSocket to receive JSON commands.
