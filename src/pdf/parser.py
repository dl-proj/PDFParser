import fitz

from settings import BOTTOM_PADDING


def extract_interest_info(info_words, left, right, top, bottom_ret=False):
    if bottom_ret:
        interest_info = []
    else:
        interest_info = ""
    for i_word in info_words:
        if not bottom_ret:
            if left <= i_word[0] <= right and top <= i_word[1] <= top + BOTTOM_PADDING:
                interest_info += i_word[4] + " "
        else:
            if left <= i_word[0] <= right and top <= i_word[1]:
                interest_info.append([i_word[0], i_word[1], i_word[4]])
    if not bottom_ret:
        interest_info = interest_info[:-1]

    return interest_info


def parse_pdf(file_path):
    pdf_info = {"Co./Last Name": ["SPOTLIGHT"], "Addr 1 - Line 1": ["SPOTLIGHT"], "- Line 2": ["VADAIN,"],
                "- Line 3": ["57 MAGNESIUM DRIVE"], "- Line 4": ["CRESTMEAD  QLD  4132"],
                "Card ID": ["102288"], "Sales Status": ["O"], "Date": [], "Customer PO": [], "Item Number": [],
                "Quantity": [], "Price": [], "Total": [], "Comment": []}

    doc = fitz.open(file_path)
    page = doc[0]
    pdf_words = page.getText("words")
    init_comment = ""
    product_info = []
    price_info = []
    qty_info = []
    total_info = []
    for i, word in enumerate(pdf_words):
        if word[4] == "PURCHASE" and pdf_words[i + 1][4] == "ORDER" and pdf_words[i + 2][4] == "DATE":
            date_info = extract_interest_info(info_words=pdf_words, left=word[0], right=pdf_words[i + 2][2],
                                              top=word[3])
            pdf_info["Date"].append(date_info)
        elif word[4] == "PURCHASE" and pdf_words[i + 1][4] == "ORDER" and pdf_words[i + 2][4] == "NO":
            customer_po_info = extract_interest_info(info_words=pdf_words, left=word[0], right=pdf_words[i + 2][2],
                                                     top=word[3])
            pdf_info["Customer PO"].append(customer_po_info)
        elif word[4] == "ORDER" and pdf_words[i + 1][4] == "NO" and pdf_words[i + 2][4] == "CONTACT":
            init_comment_info = extract_interest_info(info_words=pdf_words, left=word[0] - 10,
                                                      right=pdf_words[i + 1][2] + 10, top=word[3])
            init_comment += init_comment_info + "; "
        elif word[4] == "CONTACT" and pdf_words[i + 1][4] == "STORE":
            init_comment_info = extract_interest_info(info_words=pdf_words, left=word[0] - 30,
                                                      right=word[2] + 40, top=word[3])
            init_comment += init_comment_info + "; "
        elif word[4] == "STORE" and pdf_words[i + 1][4] == "NAME":
            init_comment_info = extract_interest_info(info_words=pdf_words, left=word[0] - 30,
                                                      right=word[2] + 30, top=word[3])
            init_comment += init_comment_info + "; "
        elif word[4] == "PRODUCT" and pdf_words[i + 1][4] == "QTY":
            product_info = extract_interest_info(info_words=pdf_words, left=word[0], right=pdf_words[i + 1][2] - 20,
                                                 top=word[3], bottom_ret=True)
        elif word[4] == "QTY" and pdf_words[i + 1][4] == "UNIT":
            qty_info = extract_interest_info(info_words=pdf_words, left=word[0] - 10, right=word[2] + 3,
                                             top=word[3], bottom_ret=True)
        elif word[4] == "UNIT" and pdf_words[i + 1][4] == "PRICE":
            price_info = extract_interest_info(info_words=pdf_words, left=word[0], right=pdf_words[i + 1][2] + 10,
                                               top=word[3], bottom_ret=True)
        elif word[4] == "LINE" and pdf_words[i + 1][4] == "TOTAL":
            total_info = extract_interest_info(info_words=pdf_words, left=word[0], right=pdf_words[i + 1][2] + 10,
                                               top=word[3], bottom_ret=True)

    sorted_y_product_info = sorted(zip(qty_info, price_info, total_info), key=lambda k: k[0][1])
    for s_y_info in sorted_y_product_info:
        y_line = s_y_info[0][1]
        pdf_info["Quantity"].append(s_y_info[0][2])
        pdf_info["Price"].append(s_y_info[1][2].replace("$", ""))
        pdf_info["Total"].append(s_y_info[2][2].replace("$", ""))
        init_item_info = ""
        for p_info in product_info:
            if y_line - 5 <= p_info[1] <= y_line + 5:
                init_item_info += p_info[2] + " "
        pdf_info["Item Number"].append(init_item_info[:-1].replace("102288.", ""))

    pdf_info["Comment"].append(init_comment[:-2])
    pdf_info["Co./Last Name"] = len(pdf_info["Item Number"]) * pdf_info["Co./Last Name"]
    pdf_info["Addr 1 - Line 1"] = len(pdf_info["Item Number"]) * pdf_info["Addr 1 - Line 1"]
    pdf_info["- Line 2"] = len(pdf_info["Item Number"]) * pdf_info["- Line 2"]
    pdf_info["- Line 3"] = len(pdf_info["Item Number"]) * pdf_info["- Line 3"]
    pdf_info["- Line 4"] = len(pdf_info["Item Number"]) * pdf_info["- Line 4"]
    pdf_info["Card ID"] = len(pdf_info["Item Number"]) * pdf_info["Card ID"]
    pdf_info["Sales Status"] = len(pdf_info["Item Number"]) * pdf_info["Sales Status"]
    pdf_info["Date"] = len(pdf_info["Item Number"]) * pdf_info["Date"]
    pdf_info["Customer PO"] = len(pdf_info["Item Number"]) * pdf_info["Customer PO"]
    pdf_info["Comment"] = len(pdf_info["Item Number"]) * pdf_info["Comment"]

    return pdf_info


if __name__ == '__main__':
    parse_pdf(file_path="")
