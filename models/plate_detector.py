from ultralytics import YOLO

from utils.constants import (
    PLATE_CONFIDENCE_THRESHOLD
)


class PlateDetector:

    def __init__(self, model_path):

        self.model = YOLO(model_path)

    def detect(self, image):

        results = self.model(
            image,
            imgsz=1280,
            conf=0.03,
            verbose=False
        )

        detections = []

        print("\n===== RAW PLATE DETECTIONS =====")

        for result in results:

            for box in result.boxes:

                conf = float(box.conf[0])

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                width = x2 - x1
                height = y2 - y1

                print(
                    f"Conf={conf:.3f} | "
                    f"BBox={[x1,y1,x2,y2]}"
                )

                # Very low confidence filter
                if conf < PLATE_CONFIDENCE_THRESHOLD:
                    continue

                # Reject tiny noise boxes
                if width < 15 or height < 8:
                    continue

                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                detections.append({

                    "confidence": conf,

                    "bbox": [
                        x1,
                        y1,
                        x2,
                        y2
                    ],

                    "width": width,

                    "height": height,

                    "center": [
                        center_x,
                        center_y
                    ]
                })

        # Sort by confidence
        detections.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )

        print("===============================\n")

        print(
            "\n===== FILTERED PLATE DETECTIONS ====="
        )

        if not detections:

            print(
                "No plates detected."
            )

        else:

            for idx, det in enumerate(
                detections,
                start=1
            ):

                print(
                    f"{idx}. "
                    f"Conf={det['confidence']:.3f} "
                    f"BBox={det['bbox']}"
                )

        print(
            "====================================\n"
        )

        return detections