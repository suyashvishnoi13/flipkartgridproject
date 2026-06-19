import cv2

from models.vehicle_detector import VehicleDetector
from models.triple_riding_detector import TripleRidingDetector
from models.helmet_detector import HelmetDetector
from models.plate_detector import PlateDetector
from models.ocr_reader import OCRReader

from services.violation_engine import ViolationEngine
from services.evidence_generator import EvidenceGenerator
from services.database_service import DatabaseService
from services.helmet_vehicle_mapper import HelmetVehicleMapper

from utils.constants import *


class TrafficVision:

    def __init__(self):

        self.vehicle_detector = VehicleDetector(
            YOLO_MODEL_PATH
        )

        self.helmet_detector = HelmetDetector(
            HELMET_MODEL_PATH
        )

        self.plate_detector = PlateDetector(
            PLATE_MODEL_PATH
        )

        self.triple_detector = TripleRidingDetector()

        self.ocr = OCRReader()

        self.engine = ViolationEngine()

        self.mapper = HelmetVehicleMapper()

        self.evidence_generator = (
            EvidenceGenerator()
        )

        self.db = DatabaseService(
            DATABASE_PATH
        )

    def process_image(self, image_path):

        image = cv2.imread(image_path)

        if image is None:

            return {
                "success": False,
                "message": "Image not found"
            }

        # --------------------------------
        # Vehicle Detection
        # --------------------------------

        detections = (
            self.vehicle_detector.detect(
                image
            )
        )

        # --------------------------------
        # Helmet Detection
        # --------------------------------

        helmet_results = (
            self.helmet_detector.detect(
                image
            )
        )

        # --------------------------------
        # Plate Detection
        # --------------------------------

        plate_results = (
            self.plate_detector.detect(
                image
            )
        )

        # --------------------------------
        # Helmet ↔ Vehicle Mapping
        # --------------------------------

        vehicle_helmet_map = (
            self.mapper.map_helmets_to_bikes(
                detections,
                helmet_results
            )
        )

        # --------------------------------
        # Triple Riding Detection
        # --------------------------------

        rider_results = (
            self.triple_detector.count_riders(
                vehicle_helmet_map
            )
        )

        print("\n===== RIDER RESULTS =====")

        for rider in rider_results:
            print(rider)

        print("========================\n")

        # --------------------------------
        # Violation Analysis
        # --------------------------------

        violations = (
            self.engine.analyze(
                rider_results,
                helmet_results
            )
        )

        # --------------------------------
        # OCR
        # --------------------------------

        vehicle_number = "PLATE_NOT_READ"

        try:

            valid_plates = [

                plate

                for plate in plate_results

                if plate["confidence"] > 0.25

            ]

            if len(valid_plates) > 0:

                best_plate = max(
                    valid_plates,
                    key=lambda x:
                    x["width"] * x["height"]
                )

                vehicle_number = (
                    self.ocr.read_number(
                        image,
                        best_plate["bbox"]
                    )
                )

                print(
                    f"OCR Candidate: "
                    f"{vehicle_number}"
                )

                if (
                    vehicle_number ==
                    "PLATE_NOT_READ"
                ):

                    for plate in valid_plates:

                        text = (
                            self.ocr.read_number(
                                image,
                                plate["bbox"]
                            )
                        )

                        if (
                            text
                            and
                            text != "PLATE_NOT_READ"
                        ):

                            vehicle_number = text
                            break

        except Exception as e:

            print(
                f"OCR Error: {e}"
            )

        # --------------------------------
        # No Violations
        # --------------------------------

        if not violations:

            return {

                "success": True,

                "violations": [],

                "message":
                "No Violations Found",

                "vehicle_number":
                vehicle_number,

                "rider_results":
                rider_results,

                "helmet_results":
                helmet_results,

                "plate_results":
                plate_results,

                "vehicle_helmet_map":
                vehicle_helmet_map
            }

        # --------------------------------
        # Evidence Generation
        # --------------------------------

        evidence_path = (
            self.evidence_generator
            .save_violation(
                image.copy(),
                violations
            )
        )

        # --------------------------------
        # Database Storage
        # --------------------------------

        for violation in violations:

            self.db.insert_violation(

                violation_type=
                violation["type"],

                vehicle_number=
                vehicle_number,

                confidence=
                violation["confidence"],

                evidence_path=
                evidence_path
            )

        # --------------------------------
        # Final Output
        # --------------------------------

        return {

            "success": True,

            "violations":
            violations,

            "vehicle_number":
            vehicle_number,

            "evidence_path":
            evidence_path,

            "rider_results":
            rider_results,

            "helmet_results":
            helmet_results,

            "plate_results":
            plate_results,

            "vehicle_helmet_map":
            vehicle_helmet_map
        }


if __name__ == "__main__":

    app = TrafficVision()

    result = app.process_image(
        "uploads/input_images/image4.jpg"
    )

    print(
        "\n========== RESULT =========="
    )

    print(result)