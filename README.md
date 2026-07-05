---
 
## System Architecture
 
```
 IMU / Pressure / DVL / GPS ──► Sensor Acquisition + Error-State EKF ──┐
                                                                        │
 Camera (30 FPS) ──► Enhancement ──► YOLOv8n Inference ──► Detections ─┼──► MQTT ──► Host Dashboard
                                                                        │
                                                                        └──► Alerts / Logging
```
 
**AI pipeline**: Camera → Enhancement (~15–20 ms/frame) → YOLOv8n @ 320×320 (~25–35 ms/frame on Jetson Nano GPU) → NMS → Detection output
**Throughput**: ~15–20 FPS end-to-end, ~50–70 ms latency (capture to detection)
 
---
 
## Repository Structure
 
```
project/
 ├── sensors/
 │   ├── imu.py         # 200 Hz IMU driver
 │   ├── pressure.py    # 30 Hz pressure → depth conversion
 │   ├── dvl.py         # 10 Hz Doppler Velocity Log driver
 │   └── fusion.py       # Error-State EKF
 ├── ai/
 │   ├── preprocess.py   # WB, dehaze, CLAHE, bilateral filter
 │   └── infer.py        # YOLOv8n inference wrapper
 ├── comm/
 │   └── mqtt_client.py  # MQTT publisher (detections, sensor state)
 ├── dashboard/
 │   └── app.py          # Flask dashboard: live feed + status API
 └── main.py             # Main acquisition/inference/comm loop
```
 
---
 
## Hardware
 
- **Edge device**: NVIDIA Jetson Nano (or Orin Nano for headroom)
- **Camera**: USB/CSI underwater-rated camera, 30 FPS
- **IMU**: 200 Hz (I2C/SPI, e.g. MPU-9250 class)
- **Pressure sensor**: 30 Hz depth sensor (e.g. MS5837/BAR30 class)
- **DVL**: 10 Hz bottom-lock velocity sensor (e.g. Teledyne/Nortek class)
- **GPS**: surface-only fix
- **Host computer**: any machine on the same network/tether running the MQTT broker + dashboard
Jetson Nano was chosen over Raspberry Pi because the enhancement pipeline + YOLOv8n inference together need GPU parallelism to hit real-time frame rates; a Pi alone struggles past single-digit FPS under this same workload.
 
---
 
## Getting Started
 
### 1. Install dependencies
```bash
pip install ultralytics opencv-python-headless paho-mqtt flask onnxruntime
```
 
### 2. Export your trained model
```bash
yolo export model=best.pt format=onnx imgsz=320
```
Place the resulting `best.onnx` at the path expected by `ai/infer.py`.
 
### 3. Start an MQTT broker (host machine)
```bash
# e.g. via Mosquitto
mosquitto -v
```
 
### 4. Run the edge pipeline (Jetson Nano)
```bash
python main.py
```
 
### 5. Launch the dashboard (host machine)
```bash
python dashboard/app.py
```
Visit `http://<host-ip>:5000/video_feed` for the annotated live stream and `/status` for JSON telemetry.
 
---
 
## MQTT Topics
 
| Topic | Payload |
|---|---|
| `auv/detections` | list of `{cls, conf, box}` |
| `auv/sensors` | fused EKF state (position, velocity, attitude, depth) |
| `auv/health` | inference FPS, latency, system temp (optional) |
 
---
 
## Roadmap / Known Limitations
 
- [ ] Replace placeholder sensor drivers with real I2C/serial parsing
- [ ] Complete Error-State EKF prediction/correction equations
- [ ] Add IOU-based tracker to stabilize low-recall detections across frames
- [ ] Optional: TensorRT engine conversion for further inference speedup
- [ ] Add alert thresholds config (depth limits, comms timeout, sensor dropout)
---
