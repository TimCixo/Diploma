# Remote Microcontroller Management System
<img src="https://github.com/user-attachments/assets/8d5e995b-b206-477a-bcdd-f1b7938c5cc6" width="250px" align="right">

A system designed for remote control and configuration of microcontrollers. It consists of two main components: a microcontroller and a web interface. 

The microcontroller executes server instructions and interacts with connected components, while the web interface allows users to configure settings, manage firmware, and design workflows through a visual interface. This solution provides flexibility and simplicity for managing electronic systems remotely.

## Wi-Fi communication

The backend communicates with the microcontroller over the local network. On startup you specify the device IP when uploading the program. Each algorithm step is sent to the microcontroller as an HTTP request, so both devices must be connected to the same Wi‑Fi network.

## Running the backend and frontend

1. Install Python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. From the repository root, run the server:
   ```bash
   python backend/src/server.py
   ```
   The server will automatically start the React development server and provide a link to `http://localhost:3000`.

3. Send the microcontroller configuration and algorithm:
   - `POST /program` – JSON containing `config` (with the device IP) and `algorithm`.
   - `POST /run` – execute the uploaded algorithm by sending commands over Wi‑Fi.
