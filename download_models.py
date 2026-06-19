import os
import gdown

os.makedirs("weights", exist_ok=True)

models = {
    "yolov8n.pt": "1f_nDy9IcGaBqDX_WtgF0a-JAMDqgStAW",
    "helmet.pt": "13dAI_IvmNmSW6V-OWRvZN45gVrjd-t2m",
    "license_plate.pt": "1D1Y8EvzZgJwCbjdsWOUk8y2fRcDMLCuO"
}

for filename, file_id in models.items():
    output = f"weights/{filename}"

    if not os.path.exists(output):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)

print("All models downloaded successfully.")
