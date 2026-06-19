import cv2


def draw_detections(image, detections):

    for det in detections:

        x1, y1, x2, y2 = det["bbox"]

        class_id = det["class_id"]

        if class_id == 0:
            label = "Person"

        elif class_id == 3:
            label = "Motorcycle"

        else:
            continue

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            image,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

    return image