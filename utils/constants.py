# ==========================
# MODEL PATHS
# ==========================

YOLO_MODEL_PATH = (
    "weights/yolov8n.pt"
)

HELMET_MODEL_PATH = (
    "weights/helmet.pt"
)

PLATE_MODEL_PATH = (
    "weights/license_plate.pt"
)


# ==========================
# DATABASE
# ==========================

DATABASE_PATH = (
    "database/violations.db"
)


# ==========================
# COCO CLASSES
# ==========================

PERSON_CLASS = 0

MOTORCYCLE_CLASS = 3


# ==========================
# HELMET MODEL CLASSES
# ==========================

WITH_HELMET = 0

WITHOUT_HELMET = 1


# ==========================
# DETECTION THRESHOLDS
# ==========================

VEHICLE_CONFIDENCE_THRESHOLD = 0.25
HELMET_CONFIDENCE_THRESHOLD = 0.30

PLATE_CONFIDENCE_THRESHOLD = 0.03


# ==========================
# VIOLATION TYPES
# ==========================

TRIPLE_RIDING = (
    "TRIPLE_RIDING"
)

NO_HELMET = (
    "NO_HELMET"
)


# ==========================
# OUTPUT DIRECTORIES
# ==========================

EVIDENCE_FOLDER = (
    "outputs/evidence"
)

PLATE_FOLDER = (
    "outputs/plates"
)

ANNOTATED_FOLDER = (
    "outputs/annotated"
)