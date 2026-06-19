import cv2
import os
from datetime import datetime


class EvidenceGenerator:

    def __init__(self):

        self.output_dir = "outputs/evidence"

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

    def save_violation(
        self,
        image,
        violations
    ):

        if len(violations) == 0:
            return None

        # -----------------------
        # Create Violation Label
        # -----------------------

        label = " | ".join(
            [
                violation["type"]
                for violation in violations
            ]
        )

        # -----------------------
        # Timestamp
        # -----------------------

        timestamp = (
            datetime.now()
            .strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        )

        # -----------------------
        # Top Red Banner
        # -----------------------

        cv2.rectangle(
            image,
            (0, 0),
            (image.shape[1], 80),
            (0, 0, 255),
            -1
        )

        cv2.putText(
            image,
            f"VIOLATION: {label}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            3
        )

        # -----------------------
        # Timestamp Bottom
        # -----------------------

        cv2.putText(
            image,
            timestamp,
            (
                20,
                image.shape[0] - 20
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # -----------------------
        # Green Border
        # -----------------------

        cv2.rectangle(
            image,
            (5, 5),
            (
                image.shape[1] - 5,
                image.shape[0] - 5
            ),
            (0, 255, 0),
            4
        )

        # -----------------------
        # Save Image
        # -----------------------

        filename = (
            "evidence_"
            +
            datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
            +
            ".jpg"
        )

        path = os.path.join(
            self.output_dir,
            filename
        )

        cv2.imwrite(
            path,
            image
        )

        print(
            f"Evidence Saved: {path}"
        )

        return path