import os
import ntpath
import pandas as pd

from src.pdf.parser import parse_pdf
from settings import OUTPUT_DIR


def create_csv_file(file_path):
    file_name = ntpath.basename(file_path).replace(".pdf", "")
    output_file_path = os.path.join(OUTPUT_DIR, f'{file_name}_result.csv')
    pdf_info = parse_pdf(file_path=file_path)
    pd.DataFrame(pdf_info, columns=list(pdf_info.keys())).to_csv(output_file_path, index=True, header=True, mode="w")

    print(f"[INFO] Successfully saved in {output_file_path}")

    return output_file_path


if __name__ == '__main__':
    import glob
    from settings import CUR_DIR
    for f_path in glob.glob(os.path.join(CUR_DIR, 'test', '*.pdf')):
        create_csv_file(file_path=f_path)
