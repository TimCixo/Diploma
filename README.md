# Remote Microcontroller Management System
<img src="https://github.com/user-attachments/assets/8d5e995b-b206-477a-bcdd-f1b7938c5cc6" width="250px" align="right">

A system designed for remote control and configuration of microcontrollers. It consists of two main components: a microcontroller and a web interface. 

The microcontroller executes server instructions and interacts with connected components, while the web interface allows users to configure settings, manage firmware, and design workflows through a visual interface. This solution provides flexibility and simplicity for managing electronic systems remotely.

## Backend server

To receive configuration from the frontend, start the provided Python server:

```bash
python backend/server.py --ip 127.0.0.1 --port 8000
```

The frontend can send the configuration JSON to `http://127.0.0.1:8000/configuration`.
The server prints the received data to the console. Example using `curl`:

```bash
curl -X POST -H "Content-Type: application/json" \
    -d '{"foo": "bar"}' http://127.0.0.1:8000/configuration
```


