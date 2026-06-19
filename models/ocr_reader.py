import easyocr
import cv2
import re
import os

from utils.constants import (
    PLATE_FOLDER
)


class OCRReader:

    def __init__(self):

        self.reader = easyocr.Reader(
            ['en'],
            gpu=False
        )

        os.makedirs(
            PLATE_FOLDER,
            exist_ok=True
        )

    def preprocess_plate(
        self,
        plate_img
    ):

        gray = cv2.cvtColor(
            plate_img,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.resize(
            gray,
            None,
            fx=8,
            fy=8,
            interpolation=cv2.INTER_CUBIC
        )

        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )

        return gray

    def clean_text(
        self,
        text
    ):

        text = text.upper()

        text = re.sub(
            r'[^A-Z0-9]',
            '',
            text
        )

        return text

    def extract_plate_pattern(
        self,
        text
    ):

        patterns = [

            r'[A-Z]{2}[0-9]{2}[A-Z]{1,3}[0-9]{3,4}',

            r'[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}'
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text
            )

            if match:

                return match.group()

        return None

    def read_number(
        self,
        image,
        plate_bbox=None
    ):

        try:

            if plate_bbox is None:
                return "PLATE_NOT_READ"

            x1, y1, x2, y2 = plate_bbox

            padding_x = 100
            padding_y = 80

            x1 = max(
                0,
                x1 - padding_x
            )

            y1 = max(
                0,
                y1 - padding_y
            )

            x2 = min(
                image.shape[1],
                x2 + padding_x
            )

            y2 = min(
                image.shape[0],
                y2 + padding_y
            )

            plate_img = image[
                y1:y2,
                x1:x2
            ]

            if plate_img.size == 0:
                return "PLATE_NOT_READ"

            plate_path = (
                f"{PLATE_FOLDER}/latest_plate.jpg"
            )

            cv2.imwrite(
                plate_path,
                plate_img
            )

            processed = (
                self.preprocess_plate(
                    plate_img
                )
            )

            cv2.imwrite(
                f"{PLATE_FOLDER}/processed_plate.jpg",
                processed
            )

            results = self.reader.readtext(
                processed,
                allowlist=
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                detail=1,
                paragraph=False
            )

            print(
                "\n===== OCR RESULTS ====="
            )

            all_text = ""

            for r in results:

                print(r)

                all_text += (
                    " " + r[1]
                )

            print(
                "=======================\n"
            )

            all_text = (
                self.clean_text(
                    all_text
                )
            )

            plate = (
                self.extract_plate_pattern(
                    all_text
                )
            )

            if plate:
                return plate

            if len(all_text) >= 6:
                return all_text

            # OCR failed -> return image path
            failed_plate_path = (
                f"{PLATE_FOLDER}/ocr_failed_plate.jpg"
            )

            cv2.imwrite(
                failed_plate_path,
                plate_img
            )

            return failed_plate_path

        except Exception as e:

            print(
                f"OCR Error: {e}"
            )

            return "PLATE_NOT_READ"