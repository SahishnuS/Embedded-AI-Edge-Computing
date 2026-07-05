class ErrorStateEKF:
    def __init__(self):
        self.state = {"pos": [0,0,0], "vel": [0,0,0], "att": [0,0,0]}

    def predict(self, imu_data, dt):
        # integrate IMU into nominal state (simplified placeholder)
        pass

    def correct_depth(self, depth):
        self.state["pos"][2] = depth  # simplified update

    def correct_dvl(self, velocity):
        self.state["vel"] = velocity

    def get_state(self):
        return self.state
