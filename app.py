import streamlit as st
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import io

# ------------------------
# Streamlit UI
# ------------------------
st.set_page_config(page_title="Smart Labeling System", page_icon="📦", layout="centered")

st.title("📦 Smart Labeling System (MVP)")

# Inputs
product_id = st.text_input("Product ID / Serial Number")
description = st.text_area("Product Description")
packaging_type = st.selectbox("Packaging Type", ["Box", "Bottle", "Pouch", "Packet", "Other"])
mfg_date = st.date_input("Manufacturing Date")
exp_date = st.date_input("Expiry Date")
location = st.text_input("Manufacturing Location")
operator = st.text_input("Tested By / Operator ID")
notes = st.text_area("Custom Notes / Alerts")

if st.button("Generate Label"):
    if not product_id or not description:
        st.error("⚠️ Please fill at least Product ID and Description!")
    else:
        # ------------------------
        # Generate QR Code
        # ------------------------
        qr_data = f"""
        Product ID: {product_id}
        Description: {description}
        MFG Date: {mfg_date}
        EXP Date: {exp_date}
        Packaging: {packaging_type}
        Location: {location}
        Operator: {operator}
        Notes: {notes}
        """
        qr = qrcode.make(qr_data)
        qr_buffer = io.BytesIO()
        qr.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)

        # ------------------------
        # Generate PDF
        # ------------------------
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=A4)
        width, height = A4

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, height - 80, "SMART LABEL REPORT")

        # Fields
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 120, f"Product ID / Serial Number: {product_id}")
        c.drawString(50, height - 140, f"Product Description: {description}")
        c.drawString(50, height - 160, f"Packaging Type: {packaging_type}")
        c.drawString(50, height - 180, f"Manufacturing Date: {mfg_date}")
        c.drawString(50, height - 200, f"Expiry Date: {exp_date}")
        c.drawString(50, height - 220, f"Manufacturing Location: {location}")
        c.drawString(50, height - 240, f"Tested By / Operator ID: {operator}")
        c.drawString(50, height - 260, f"Custom Notes / Alerts: {notes}")

        # Date & Time
        c.drawString(50, height - 300, f"Label Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # QR Code
        c.drawInlineImage(qr_buffer, width - 200, height - 300, 120, 120)

        c.save()
        pdf_buffer.seek(0)

        # ------------------------
        # Streamlit Output
        # ------------------------
        st.success("✅ Label generated successfully!")
        st.image(qr_buffer, caption="Generated QR Code", width=200)

        st.download_button(
            "📥 Download PDF Label",
            data=pdf_buffer,
            file_name=f"label_{product_id}.pdf",
            mime="application/pdf"
        )
