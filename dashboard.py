import streamlit as st
import os
import pandas as pd
from generate_pdf import generate_pdf_label

# Create folders if they don't exist
os.makedirs("generated_labels", exist_ok=True)
os.makedirs("generated_labels/pdf", exist_ok=True)
os.makedirs("generated_labels/qr", exist_ok=True)
os.makedirs("generated_labels/barcode", exist_ok=True)

CSV_FILE = "generated_labels/label_data.csv"

st.title("Smart Product Labeling System")

# Form to collect product details
with st.form("product_form"):
    name = st.text_input("Product Name")
    batch = st.text_input("Batch Number")
    product_id = st.text_input("Product ID / Serial Number")
    temperature = st.number_input("Temperature (°C)", format="%.2f")
    weight = st.number_input("Weight (g)", format="%.2f")
    size = st.text_input("Size")
    status = st.selectbox("Quality Status", ["PASSED", "FAILED"])
    defect = st.text_input("Defect Info", value="NONE")
    location = st.text_input("Manufacturing Location")
    operator_id = st.text_input("Tested By / Operator ID")
    description = st.text_area("Product Description")
    packaging = st.text_input("Packaging Type")
    mfg_date = st.date_input("Manufacturing Date")
    exp_date = st.date_input("Expiry Date")
    notes = st.text_area("Custom Notes / Alerts")

    submitted = st.form_submit_button("Generate Label")

if submitted:
    pdf_file, qr_file, barcode_file = generate_pdf_label(
        name,
        batch,
        temperature,
        weight,
        size,
        status,
        defect,
        location,
        operator_id,
        description,
        packaging,
        mfg_date.strftime("%d-%m-%Y"),
        exp_date.strftime("%d-%m-%Y"),
        notes,
        product_id,
        save_dir="generated_labels"
    )

    # Save data to CSV
    new_data = pd.DataFrame([{
        "Product Name": name,
        "Batch Number": batch,
        "Product ID": product_id,
        "Temperature (°C)": temperature,
        "Weight (g)": weight,
        "Size": size,
        "Status": status,
        "Defect Info": defect,
        "Location": location,
        "Operator ID": operator_id,
        "Description": description,
        "Packaging": packaging,
        "MFG Date": mfg_date.strftime("%d-%m-%Y"),
        "EXP Date": exp_date.strftime("%d-%m-%Y"),
        "Notes": notes
    }])

    if os.path.exists(CSV_FILE):
        existing_data = pd.read_csv(CSV_FILE)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(CSV_FILE, index=False)

    st.success("Label generated and saved successfully!")
    st.download_button("Download PDF Label", open(pdf_file, "rb"), file_name=os.path.basename(pdf_file))
    st.image(qr_file, caption="QR Code")
    st.image(barcode_file, caption="Barcode")
