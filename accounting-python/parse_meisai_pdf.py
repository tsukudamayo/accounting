from datetime import datetime
import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import pandas as pd


data_dir = "./data"
filename = "meisai_202408.pdf"
year = "24"
filepath = os.path.join(data_dir, filename)

date_description = "お取引日お取引内容"
amount = "お取引金額お取引手数料"
title = "ご利用明細書"
black_list = set([
    "PDF出力日：",
    "PAGE",
    "株式会社ゆうちょ銀行",
    "お取引通貨",
    "ご利用通貨",
    "ご利用手数料",
    "ご利用金額",
    "ATM手数料",
    "換算レート",
    "為替手数料",
    "確定",
    "",
    "****-****-****-****",
    "＊＊＊　＊＊　様",
    "1",
])

category = None
year_flg = f"{year}/"
_amount = []
_date = []
_description = []

# TODO
if filename == "meisai_202304.pdf":
    _date.append("2023-04-01")
    _description.append("MONDIALKAFFEE328GOLDRUSH")

if filename == "meisai_202305.pdf":
    _date.append("2023-05-01")
    _date.append("2023-05-01")
    _description.append("MONDIALKAFFEE328GOLDRUSH")
    _description.append("MONDIALKAFFEE328GOLDRUSH")

for idx_1, page_layout in enumerate(extract_pages(filepath)):
    print(f"idx_1 ===== {idx_1}")
    for idx_2, element in enumerate(page_layout):
        if isinstance(element, LTTextContainer):
            text = element.get_text()
            text = text.replace(" ", "")
            text = text.split("\n")

            print(text)
            if text[0] in black_list:
                continue

            if text[0] == date_description:
                category = date_description
            elif year_flg in text[0]:
                category = date_description
            elif text[0] == amount:
                category = amount
            elif text[0] == "JPY":
                category = amount
            elif text[0] == title:
                category = title

            #print("category : ", category)
            
            if category == date_description:
                if year_flg in text[0]:
                    category = date_description
                    print("text[0] = ", text[0])
                    # TODO ex: [ご利用明細書 PDF出力日: 2024/08/04]
                    try:
                        date_format = datetime.strptime(text[0], "%y/%m/%d")
                    except ValueError as e:
                        print(e)
                        continue
                    date = date_format.strftime("%Y-%m-%d")
                    print(date)
                    _date.append(date)
                else:
                    if text[0] == date_description:
                        pass
                    else:
                        print(f" description == {text[0]}")
                        _description.append(text[0])

            elif category == amount:
                for t in text:
                    _t = t.replace(",", "")
                    _t = _t.replace(".00", "")

                    if "-" in _t:
                        _t = _t.replace("-", "")
                        if _t.isdigit():
                            print(f"-{_t}")
                            _amount.append(-float(_t))
                            continue

                    if _t.isdigit():
                        print(_t)
                        _amount.append(float(_t))
            else:
                pass

print("amount length : ", len(_amount))
print("description length : ", len(_description))
print("date length : ", len(_date))


df = pd.DataFrame({
    "transaction_date": _date,
    "description": _description,
    "debbit_amount": _amount,
})

df.to_csv(filepath.replace("pdf", "csv"), index=False)

