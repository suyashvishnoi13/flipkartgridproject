from ultralytics import YOLO

from utils.constants import (
    PERSON_CLASS,
    MOTORCYCLE_CLASS,
    VEHICLE_CONFIDENCE_THRESHOLD
)


class VehicleDetector:

    def __init__(self, model_path):

        self.model = YOLO(model_path)

    def detect(self, image):

        results = self.model(
            image,
            conf=VEHICLE_CONFIDENCE_THRESHOLD,
            verbose=False
        )

        detections = []

        for result in results:

            for box in result.boxes:

                cls = int(box.cls[0])

                if cls not in [
                    PERSON_CLASS,
                    MOTORCYCLE_CLASS
                ]:
                    continue

                conf = float(box.conf[0])

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                detections.append({

                    "class_id": cls,

                    "class_name":
                    "person"
                    if cls == PERSON_CLASS
                    else "motorcycle",

                    "confidence": conf,

                    "bbox": [
                        x1,
                        y1,
                        x2,
                        y2
                    ]
                })

        print("\n===== VEHICLE DETECTIONS =====")

        persons = 0
        motorcycles = 0

        for det in detections:

            print(det)

            if det["class_name"] == "person":
                persons += 1

            elif det["class_name"] == "motorcycle":
                motorcycles += 1

        print(
            f"\nTotal Persons: {persons}"
        )

        print(
            f"Total Motorcycles: {motorcycles}"
        )

        print(
            "=============================\n"
        )

        return detections