import os
import pandas as pd

from zipfile import ZipFile
from src.pdf.parser import parse_pdf
from settings import OUTPUT_DIR


def create_csv_file(file_paths, option):
    output_files = []
    if option == "multi":
        output_file_path = os.path.join(OUTPUT_DIR, 'result.zip')
    else:
        output_file_path = os.path.join(OUTPUT_DIR, 'result.csv')
    multi_pdf_info = {"Co./Last Name": [], "Addr 1 - Line 1": [], "- Line 2": [], "- Line 3": [], "- Line 4": [],
                      "Card ID": [], "Sales Status": [], "Date": [], "Customer PO": [], "Item Number": [],
                      "Quantity": [], "Price": [], "Total": [], "Comment": []}
    for file_path in file_paths:
        pdf_info = parse_pdf(file_path=file_path)
        if option == "multi":
            s_output_file_path = os.path.join(OUTPUT_DIR, f'{pdf_info["Customer PO"][0]}.csv')
            pd.DataFrame(pdf_info).to_csv(s_output_file_path, header=False, sep=",", mode="w")
            output_files.append(s_output_file_path)
        else:
            for p_key in multi_pdf_info.keys():
                multi_pdf_info[p_key] += pdf_info[p_key]
            pd.DataFrame(multi_pdf_info).to_csv(output_file_path, header=False, sep=",", mode="w")
    if option == "multi":
        zip_obj = ZipFile(output_file_path, 'w')
        for o_file in output_files:
            zip_obj.write(o_file, os.path.basename(o_file))
        zip_obj.close()

    print(f"[INFO] Successfully saved in {output_file_path}")

    return output_file_path


if __name__ == '__main__':
    create_csv_file(file_paths=[""], option="")
