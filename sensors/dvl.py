import threading, time

class DVL:
    """Doppler Velocity Log — body-frame velocity + bottom lock status. ~10 Hz."""
    def __init__(self, rate_hz=10):
        self.rate = rate_hz
        self.latest = None
        self._lock = threading.Lock()

    def read_raw(self):
        # replace with actual serial/UDP parse (e.g. Teledyne, Nortek protocol)
        return {"vx": 0.0, "vy": 0.0, "vz": 0.0, "bottom_lock": True, "t": time.time()}

    def start(self):
        def loop():
            while True:
                data = self.read_raw()
                with self._lock:
                    self.latest = data
                time.sleep(1 / self.rate)
        threading.Thread(target=loop, daemon=True).start()

    def get(self):
        with self._lock:
            return self.latest
