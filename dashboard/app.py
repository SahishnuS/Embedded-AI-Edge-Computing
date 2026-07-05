import json, threading, cv2
from flask import Flask, Response, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)
state = {"detections": [], "sensors": {}, "alerts": []}
latest_frame = None
_lock = threading.Lock()

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    with _lock:
        if msg.topic == "auv/detections":
            state["detections"] = payload
        elif msg.topic == "auv/sensors":
            state["sensors"] = payload
            # simple alert rule
            depth = payload.get("depth_m", 0)
            state["alerts"] = ["DEPTH LIMIT EXCEEDED"] if depth > 50 else []

def mqtt_thread():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("localhost", 1883)
    client.subscribe([("auv/detections", 0), ("auv/sensors", 0)])
    client.loop_forever()

threading.Thread(target=mqtt_thread, daemon=True).start()

@app.route("/status")
def status():
    with _lock:
        return jsonify(state)

def gen_frames():
    cap = cv2.VideoCapture(0)  # or read from a shared frame buffer set by main.py
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        with _lock:
            for d in state["detections"]:
                x1, y1, x2, y2 = map(int, d["box"][0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        _, buf = cv2.imencode(".jpg", frame)
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buf.tobytes() + b"\r\n")

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
