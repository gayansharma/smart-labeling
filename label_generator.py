import qrcode
import os
from datetime import datetime

def generate_label(product_name, batch_no):
    data = f"Product: {product_name}\nBatch: {batch_no}\nTime: {datetime.now()}"
    qr = qrcode.make(data)
    path = f"labels/{product_name}_{batch_no}.png"
    os.makedirs("labels", exist_ok=True)
    qr.save(path)
    return path