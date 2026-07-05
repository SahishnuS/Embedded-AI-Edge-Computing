import json, paho.mqtt.client as mqtt

class Comm:
    def __init__(self, broker="localhost"):
        self.client = mqtt.Client()
        self.client.connect(broker, 1883)

    def publish_detections(self, dets):
        self.client.publish("auv/detections", json.dumps(dets))

    def publish_sensors(self, state):
        self.client.publish("auv/sensors", json.dumps(state))
      
