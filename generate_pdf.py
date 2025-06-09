from fpdf import FPDF
import qrcode
import barcode
from barcode.writer import ImageWriter
from datetime import datetime
import os

def generate_pdf_label(name, batch, temperature, weight, size, status, defect,
                       location, operator_id, description, packaging,
                       mfg_date, exp_date, notes, product_id, save_dir):

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    base_filename = f"{name}_{batch}_{timestamp}"

    # Save QR code with product info
    qr_data = f"Product: {name}\nBatch: {batch}\nTemp: {temperature}°C\nWeight: {weight}g\nStatus: {status}\nID: {product_id}"
    qr = qrcode.make(qr_data)
    qr_path = os.path.join(save_dir, "qr", f"{base_filename}_qr.png")
    qr.save(qr_path)

    # Save Barcode with Product ID
    CODE128 = barcode.get_barcode_class("code128")
    code = CODE128(product_id, writer=ImageWriter())
    barcode_path = os.path.join(save_dir, "barcode", f"{base_filename}_barcode.png")
    code.save(barcode_path)

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Product Label Report", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Date & Time: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", ln=True)
    pdf.cell(200, 10, txt=f"Product Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Batch Number: {batch}", ln=True)
    pdf.cell(200, 10, txt=f"Product ID / Serial Number: {product_id}", ln=True)
    pdf.cell(200, 10, txt=f"Temperature: {temperature} °C", ln=True)
    pdf.cell(200, 10, txt=f"Weight: {weight} g", ln=True)
    pdf.cell(200, 10, txt=f"Size: {size}", ln=True)
    pdf.cell(200, 10, txt=f"Quality Status: {status}", ln=True)
    pdf.cell(200, 10, txt=f"Defect Info: {defect}", ln=True)
    pdf.cell(200, 10, txt=f"Manufacturing Location: {location}", ln=True)
    pdf.cell(200, 10, txt=f"Tested By / Operator ID: {operator_id}", ln=True)
    pdf.cell(200, 10, txt=f"Packaging Type: {packaging}", ln=True)
    pdf.cell(200, 10, txt=f"MFG Date: {mfg_date}", ln=True)
    pdf.cell(200, 10, txt=f"EXP Date: {exp_date}", ln=True)
    pdf.multi_cell(200, 10, txt=f"Description: {description}")
    pdf.multi_cell(200, 10, txt=f"Notes: {notes}")

    # Insert QR Code image
    pdf.image(qr_path, x=10, y=pdf.get_y() + 10, w=50)

    pdf_path = os.path.join(save_dir, "pdf", f"{base_filename}_label.pdf")
    pdf.output(pdf_path)

    return pdf_path, qr_path, barcode_path
