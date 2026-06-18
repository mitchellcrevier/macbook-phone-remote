import ctypes
import os
import socket
import subprocess

import pyautogui

from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO

pyautogui.FAILSAFE = False

try:
    from ApplicationServices import AXIsProcessTrustedWithOptions
    AXIsProcessTrustedWithOptions({'AXTrustedCheckOptionPrompt': True})
except Exception:
    pass

app = Flask(__name__, static_folder="static")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

_connection_count = 0
_overlay_proc = None

OVERLAY_BIN = os.path.join(os.path.dirname(__file__), "cursor_overlay_bin")

try:
    _sl = ctypes.CDLL('/System/Library/PrivateFrameworks/SkyLight.framework/SkyLight')
    _cg = ctypes.CDLL('/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics')
    _cg.CGSMainConnectionID.restype = ctypes.c_uint
    _sl.CGSSetCursorScale.restype = ctypes.c_int
    _sl.CGSSetCursorScale.argtypes = [ctypes.c_uint, ctypes.c_double]
    _sl.CGSGetCursorScale.restype = ctypes.c_int
    _sl.CGSGetCursorScale.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_double)]
    _CGS_AVAILABLE = True
except Exception as e:
    _CGS_AVAILABLE = False
    print(f"[cursor] CGS unavailable: {e}", flush=True)


def _set_cursor_scale(scale: float):
    if not _CGS_AVAILABLE:
        return -1
    conn = _cg.CGSMainConnectionID()
    result = _sl.CGSSetCursorScale(conn, ctypes.c_double(scale))
    print(f"[cursor] CGSSetCursorScale({scale}) conn={conn} result={result}", flush=True)
    return result


def _start_overlay():
    global _overlay_proc
    if _overlay_proc is None or _overlay_proc.poll() is not None:
        _overlay_proc = subprocess.Popen(
            [OVERLAY_BIN],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"[overlay] started pid={_overlay_proc.pid}", flush=True)


def _stop_overlay():
    global _overlay_proc
    if _overlay_proc and _overlay_proc.poll() is None:
        _overlay_proc.terminate()
    _overlay_proc = None


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


@socketio.on("connect")
def handle_connect():
    global _connection_count
    _connection_count += 1
    print(f"[ws] connect — total={_connection_count}", flush=True)
    if _connection_count == 1:
        r = _set_cursor_scale(3.0)
        if r != 0:
            _start_overlay()


@socketio.on("disconnect")
def handle_disconnect():
    global _connection_count
    _connection_count = max(0, _connection_count - 1)
    print(f"[ws] disconnect — total={_connection_count}", flush=True)
    if _connection_count == 0:
        _set_cursor_scale(1.0)
        _stop_overlay()


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


@socketio.on("volume")
def handle_volume(data):
    level = max(0, min(100, int(data.get("level", 50))))
    subprocess.run(["osascript", "-e", f"set volume output volume {level}"])


@app.route("/volume")
def get_volume():
    result = subprocess.run(
        ["osascript", "-e", "output volume of (get volume settings)"],
        capture_output=True, text=True
    )
    try:
        level = int(result.stdout.strip())
    except ValueError:
        level = 50
    return jsonify({"level": level})


@socketio.on("sleep")
def handle_sleep():
    subprocess.Popen(["pmset", "sleepnow"])


@socketio.on("type")
def handle_type(data):
    text = data.get("text", "")
    if not text:
        return
    escaped = text.replace('\\', '\\\\').replace('"', '\\"')
    subprocess.run(
        ['osascript', '-e', f'tell application "System Events" to keystroke "{escaped}"'],
        capture_output=True, check=False
    )


@socketio.on("key")
def handle_key(data):
    key = data.get("key", "")
    count = max(1, int(data.get("count", 1)))
    if key == "Backspace":
        for _ in range(count):
            pyautogui.press('backspace')
    elif key == "Enter":
        pyautogui.press('enter')
    elif key == "Tab":
        pyautogui.press('tab')
    elif key == "Escape":
        pyautogui.press('esc')


if __name__ == "__main__":
    port = 5050
    ip = get_local_ip()
    print(f"\n  Mac Remote running.")
    print(f"  Open on your phone: http://{ip}:{port}\n")
    socketio.run(app, host="0.0.0.0", port=port, debug=False, allow_unsafe_werkzeug=True)
