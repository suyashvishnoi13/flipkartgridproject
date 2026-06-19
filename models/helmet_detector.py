from ultralytics import YOLO

from utils.constants import (
    WITH_HELMET,
    WITHOUT_HELMET,
    HELMET_CONFIDENCE_THRESHOLD
)


class HelmetDetector:

    def __init__(self, model_path):

        self.model = YOLO(model_path)

    def detect(self, image):

        results = self.model(
            image,
            verbose=False
        )

        detections = []

        for result in results:

            for box in result.boxes:

                cls = int(box.cls[0])

                conf = float(box.conf[0])

                if conf < HELMET_CONFIDENCE_THRESHOLD:
                    continue

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                if cls == WITH_HELMET:

                    class_name = "helmet"

                elif cls == WITHOUT_HELMET:

                    class_name = "no_helmet"

                else:

                    class_name = "unknown"

                detections.append({

                    "class_id": cls,

                    "class_name": class_name,

                    "confidence": conf,

                    "bbox": [
                        x1,
                        y1,
                        x2,
                        y2
                    ]
                })

        print("\n===== HELMET DETECTIONS =====")

        for det in detections:
            print(det)

        print("============================\n")

        return detections