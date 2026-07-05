import threading, time

class IMU:
    def __init__(self, rate_hz=200):
        self.rate = rate_hz
        self.latest = None
        self._lock = threading.Lock()

    def read_raw(self):
        # replace with actual I2C/SPI read
        return {"accel": (0,0,9.8), "gyro": (0,0,0), "t": time.time()}

    def start(self):
        def loop():
            while True:
                data = self.read_raw()
                with self._lock:
                    self.latest = data
                time.sleep(1/self.rate)
        threading.Thread(target=loop, daemon=True).start()

    def get(self):
        with self._lock:
            return self.latest
