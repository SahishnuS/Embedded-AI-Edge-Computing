import threading, time

class PressureSensor:
    """Converts raw pressure (kPa) to depth (m). ~30 Hz."""
    def __init__(self, rate_hz=30, fluid_density=1025, g=9.81):
        self.rate = rate_hz
        self.density = fluid_density
        self.g = g
        self.latest = None
        self._lock = threading.Lock()

    def read_raw_kpa(self):
        # replace with actual I2C read (e.g. MS5837 / BAR30)
        return 101.3  # surface pressure placeholder

    def pressure_to_depth(self, kpa):
        pa = kpa * 1000
        return (pa - 101325) / (self.density * self.g)

    def start(self):
        def loop():
            while True:
                kpa = self.read_raw_kpa()
                with self._lock:
                    self.latest = {"depth_m": self.pressure_to_depth(kpa), "t": time.time()}
                time.sleep(1 / self.rate)
        threading.Thread(target=loop, daemon=True).start()

    def get(self):
        with self._lock:
            return self.latest
