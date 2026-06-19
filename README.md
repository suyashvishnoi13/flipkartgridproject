# 🚦 TrafficVision AI

> AI-Powered Traffic Violation Detection and Evidence Generation System

TrafficVision AI is a computer vision–based intelligent traffic monitoring platform designed to automatically detect traffic violations, extract vehicle information, generate digital evidence, and provide analytics through an interactive dashboard.

The system leverages Deep Learning, Computer Vision, OCR, and Data Analytics to assist traffic authorities in reducing manual monitoring efforts and improving enforcement efficiency.

---

## 🎯 Problem Statement

Modern traffic surveillance systems generate thousands of images daily. Manual inspection of these images is:

* Time-consuming
* Labor-intensive
* Error-prone
* Difficult to scale

TrafficVision AI automates the complete violation detection workflow by identifying violations, recognizing vehicle registration numbers, generating evidence, and storing records for future analysis.

---

# ✨ Key Features

### 🪖 Helmet Violation Detection

Detects riders who are not wearing helmets using a custom-trained YOLOv8 helmet detection model.

### 👥 Triple Riding Detection

Identifies motorcycles carrying more than the permitted number of riders.

### 🚗 Vehicle Detection

Detects and classifies vehicles using YOLOv8.

### 🔤 Automatic Number Plate Recognition (ANPR)

Detects number plates and extracts registration numbers using EasyOCR.

### 📸 Evidence Generation

Automatically generates annotated evidence images containing:

* Violation Type
* Vehicle Number
* Timestamp
* Detection Confidence

### 💾 Violation Database

Stores all detected violations and metadata using SQLite.

### 📊 Analytics Dashboard

Interactive Streamlit dashboard for:

* Violation Statistics
* Evidence Viewer
* Violation History
* CSV Export

---

# 🏗 System Architecture

```text
Traffic Image
      │
      ▼
Image Processing
      │
      ▼
Vehicle Detection (YOLOv8)
      │
      ├── Helmet Detection
      │
      ├── Triple Riding Detection
      │
      └── Number Plate OCR
      │
      ▼
Violation Engine
      │
      ▼
Evidence Generation
      │
      ▼
SQLite Database
      │
      ▼
Streamlit Dashboard
```

---

# ⚙️ Technology Stack

## Computer Vision

* YOLOv8
* OpenCV
* EasyOCR

## Backend

* Python
* SQLite

## Dashboard

* Streamlit
* Plotly
* Pandas

## Deep Learning

* PyTorch
* Ultralytics YOLO

---

# 📂 Project Structure

```text
TrafficVisionAI/
│
├── dashboard/
│   └── streamlit_app.py
│
├── database/
│   └── violations.db
│
├── models/
│   ├── vehicle_detector.py
│   ├── helmet_detector.py
│   ├── triple_riding_detector.py
│   ├── plate_detector.py
│   ├── ocr_reader.py
│   └── helmet_api.py
│
├── services/
│   ├── pipeline_service.py
│   ├── violation_engine.py
│   ├── helmet_vehicle_mapper.py
│   ├── evidence_generator.py
│   └── database_service.py
│
├── outputs/
│   ├── annotated/
│   ├── evidence/
│   └── plates/
│
├── uploads/
│
├── utils/
│   ├── constants.py
│   └── image_utils.py
│
├── weights/
│   ├── yolov8n.pt
│   ├── helmet.pt
│   └── license_plate.pt
│
├── app.py
├── requirements.txt
├── README.md
└── architecture.png
```

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone https://github.com/your-username/TrafficVisionAI.git

cd TrafficVisionAI
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Download Models

Place the following files inside:

```text
weights/
```

### Vehicle Detection Model

```text
weights/yolov8n.pt
```

### Helmet Detection Model

```text
weights/helmet.pt
```

### License Plate Detection Model

```text
weights/license_plate.pt
```

---

# ▶️ Running the Application

## Run Detection Pipeline

```bash
python app.py
```

---

## Launch Dashboard

```bash
streamlit run dashboard/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

---

# 📸 Sample Output

### Violation Detected

```text
NO_HELMET
```

### Vehicle Number

```text
UP32LD5986
```

### Confidence Score

```text
94.7%
```

### Evidence File

```text
outputs/evidence/evidence_20260619_120538.jpg
```

---

# 🗄 Database Schema

### Table: violations

| Field          | Type     |
| -------------- | -------- |
| id             | INTEGER  |
| violation_type | TEXT     |
| vehicle_number | TEXT     |
| confidence     | REAL     |
| evidence_path  | TEXT     |
| timestamp      | DATETIME |

---

# 📊 Dashboard Features

### Analytics

* Total Violations
* Helmet Violations
* Triple Riding Violations
* Daily Violation Trends

### Violation History

Search and view previous violations.

### Evidence Viewer

View generated evidence images directly from the dashboard.

### CSV Export

Download violation records for reporting and analysis.

---

# 📈 Performance Metrics

The system can be evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score
* mAP@50
* OCR Recognition Accuracy

---

# 🔮 Future Enhancements

* Real-Time CCTV Video Processing
* Red-Light Violation Detection
* Wrong-Side Driving Detection
* Seatbelt Violation Detection
* Illegal Parking Detection
* E-Challan Integration
* Cloud Deployment
* Multi-Camera Support
* Smart City Integration

---

# 👥 Team

### TrafficVision AI

AI-Based Traffic Violation Detection and Monitoring System

Built using:

* Computer Vision
* Deep Learning
* OCR
* Streamlit
* SQLite

---

# 📜 License

MIT License

Copyright (c) 2026 TrafficVision AI
