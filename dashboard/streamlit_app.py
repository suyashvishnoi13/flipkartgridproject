import streamlit as st
import pandas as pd
import sqlite3
import os
import sys
import traceback
import io
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak
)
from reportlab.lib.styles import (
    getSampleStyleSheet
)

ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.append(ROOT_DIR)

from app import TrafficVision

st.set_page_config(
    page_title="TrafficVision AI",
    page_icon="🚦",
    layout="wide"
)

# -------------------------
# HEADER
# -------------------------

st.markdown(
    """
    # 🚦 TrafficVision AI
    ### Smart Traffic Violation Detection System
    """
)

# -------------------------
# PATHS
# -------------------------

UPLOAD_DIR = os.path.join(
    ROOT_DIR,
    "uploads",
    "input_images"
)

DB_PATH = os.path.join(
    ROOT_DIR,
    "database",
    "violations.db"
)

EVIDENCE_DIR = os.path.join(
    ROOT_DIR,
    "outputs",
    "evidence"
)

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)
def generate_pdf_report(df):

    import io

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "TrafficVision AI Violation Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    for index, row in df.iterrows():

        elements.append(
            Paragraph(
                f"<b>Record ID:</b> {row['id']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Violation:</b> {row['violation_type']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Vehicle Number:</b> {row['vehicle_number']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Confidence:</b> {round(row['confidence'],2)}",
                styles["Normal"]
            )
        )

        if (
            "evidence_path" in row
            and
            os.path.exists(
                row["evidence_path"]
            )
        ):

            try:

                elements.append(
                    Image(
                        row["evidence_path"],
                        width=180,
                        height=130
                    )
                )

            except:
                pass

        elements.append(
            Spacer(1, 15)
        )

        # Page break every 3 records
        if (
            (index + 1) % 3 == 0
        ):
            elements.append(
                PageBreak()
            )

    doc.build(elements)

    buffer.seek(0)

    return buffer
# -------------------------
# SIDEBAR
# -------------------------

with st.sidebar:

    st.title("⚙ System")

    st.success(
        "AI Engine Online"
    )

    st.write(
        f"Database: {'✅' if os.path.exists(DB_PATH) else '❌'}"
    )

# -------------------------
# UPLOAD
# -------------------------

st.header("📤 Upload Image")

uploaded_file = st.file_uploader(
    "Choose Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    save_path = os.path.join(
        UPLOAD_DIR,
        uploaded_file.name
    )

    with open(save_path, "wb") as f:
        f.write(
            uploaded_file.getbuffer()
        )

    col1, col2 = st.columns(2)

    with col1:

        st.image(
            save_path,
            caption="Input Image",
            use_container_width=True
        )

    if st.button(
        "🚀 Analyze Image"
    ):

        with st.spinner(
            "Running AI Detection..."
        ):

            detector = TrafficVision()

            result = detector.process_image(
                save_path
            )

        st.success(
            "Detection Completed"
        )

        st.subheader(
            "📋 Violation Report"
        )

        colA, colB, colC = st.columns(3)

        with colA:
            st.metric(
                "Violations",
                len(
                    result["violations"]
                )
            )

        with colB:
            st.metric(
                "Vehicles",
                len(
                    result["rider_results"]
                )
            )

        with colC:
            st.metric(
                "Helmet Detections",
                len(
                    result["helmet_results"]
                )
            )

        st.json(result)
# -------------------------
# DATA MANAGEMENT
# -------------------------

st.divider()

st.header(
    "⚙ Data Management"
)

col_clear, col_export = st.columns(2)

with col_clear:

    if st.button(
        "🗑 Clear All Data",
        use_container_width=True
    ):

        try:

            conn = sqlite3.connect(
                DB_PATH
            )

            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM violations"
            )

            conn.commit()

            conn.close()

            if os.path.exists(
                EVIDENCE_DIR
            ):

                for file in os.listdir(
                    EVIDENCE_DIR
                ):

                    file_path = os.path.join(
                        EVIDENCE_DIR,
                        file
                    )

                    if os.path.isfile(
                        file_path
                    ):

                        os.remove(
                            file_path
                        )

            st.success(
                "All records deleted successfully."
            )

            st.rerun()

        except Exception as e:

            st.error(
                str(e)
            )

# -------------------------
# ANALYTICS
# -------------------------

st.divider()

st.header(
    "📊 Analytics Dashboard"
)

if os.path.exists(DB_PATH):

    conn = sqlite3.connect(
        DB_PATH
    )

    try:

        df = pd.read_sql_query(
            """
            SELECT *
            FROM violations
            ORDER BY id DESC
            """,
            conn
        )

        total = len(df)

        helmet = len(
            df[
                df["violation_type"]
                ==
                "NO_HELMET"
            ]
        )

        triple = len(
            df[
                df["violation_type"]
                ==
                "TRIPLE_RIDING"
            ]
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Violations",
            total
        )

        col2.metric(
            "Helmet Violations",
            helmet
        )

        col3.metric(
            "Triple Riding",
            triple
        )

        st.divider()

        chart_data = pd.DataFrame(
            {
                "Violation":
                [
                    "NO_HELMET",
                    "TRIPLE_RIDING"
                ],

                "Count":
                [
                    helmet,
                    triple
                ]
            }
        )

        st.subheader(
            "Violation Distribution"
        )

        st.bar_chart(
            chart_data.set_index(
                "Violation"
            )
        )

        st.divider()

        st.subheader(
            "Violation History"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        # -------------------------
        # PDF EXPORT
        # -------------------------

        with col_export:

            if len(df):

                pdf_bytes = generate_pdf_report(
                    df
                )

                st.download_button(

                    label=
                    "📄 Export PDF Report",

                    data=
                    pdf_bytes,

                    file_name=
                    "TrafficVision_Report.pdf",

                    mime=
                    "application/pdf",

                    use_container_width=
                    True
                )

    except Exception:

        st.code(
            traceback.format_exc()
        )

    finally:

        conn.close()


# -------------------------
# EVIDENCE
# -------------------------

st.divider()

st.header(
    "📷 Latest Evidence"
)

if os.path.exists(EVIDENCE_DIR):

    files = sorted(
        [
            os.path.join(
                EVIDENCE_DIR,
                f
            )
            for f in os.listdir(
                EVIDENCE_DIR
            )
        ],
        reverse=True
    )

    if len(files):

        st.image(
            files[0],
            caption="Latest Violation Evidence",
            use_container_width=True
        )

st.divider()

st.success(
    "TrafficVision AI Running Successfully"
)