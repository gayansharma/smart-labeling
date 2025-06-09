from quality_check import check_quality
from defect_detection import detect_defects
from label_generator import generate_label
from database import insert_product

def main():
    name = "TestProduct"
    batch = "B123"
    weight = 200
    temp = 25
    size = 50

    if check_quality(weight, temp, size) and detect_defects("sample.jpg") == "No defects":
        label_path = generate_label(name, batch)
        insert_product(name, batch, temp, weight, size, label_path)
        print("Product processed and labeled.")
    else:
        print("Product failed QC or defect check.")

if __name__ == "__main__":
    main()