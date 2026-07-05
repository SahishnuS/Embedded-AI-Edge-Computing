from ultralytics import YOLO

class Detector:
    def __init__(self, weights="best.onnx"):
        self.model = YOLO(weights)

    def predict(self, frame):
        results = self.model(frame, imgsz=320, verbose=False)[0]
        return [
            {"cls": r.cls.item(), "conf": r.conf.item(), "box": r.xyxy.tolist()}
            for r in results.boxes
        ]
