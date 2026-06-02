import socket
import subprocess

import pyautogui

from flask import Flask, send_from_directory
from flask_socketio import SocketIO

pyautogui.FAILSAFE = False

app = Flask(__name__, static_folder="static")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@socketio.on("mousemove")
def handle_mousemove(data):
    dx = data.get("dx", 0)
    dy = data.get("dy", 0)
    pyautogui.moveRel(int(dx), int(dy), duration=0)


@socketio.on("leftclick")
def handle_leftclick():
    pyautogui.click()


@socketio.on("rightclick")
def handle_rightclick():
    pyautogui.rightClick()


@socketio.on("scroll")
def handle_scroll(data):
    dx = data.get("dx", 0)
    dy = data.get("dy", 0)
    pyautogui.scroll(int(-dy))


@socketio.on("sleep")
def handle_sleep():
    subprocess.Popen(["pmset", "sleepnow"])


if __name__ == "__main__":
    port = 5050
    ip = get_local_ip()
    print(f"\n  Mac Remote running.")
    print(f"  Open on your phone: http://{ip}:{port}\n")
    socketio.run(app, host="0.0.0.0", port=port, debug=False, allow_unsafe_werkzeug=True)
