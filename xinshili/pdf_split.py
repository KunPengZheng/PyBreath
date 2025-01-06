import os

import pikepdf
import pdfplumber
import re


def extract_text_from_pdf(pdf_path):
    extract_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # page.extract_text(): 扫描文字
            # replace去除字符串空格
            extract_text += page.extract_text().replace(" ", "")
    # print(f"打印内容：{extract_text}")
    # 扫描所有pdf的文本内容，正则匹配获取到面单号
    return re.findall(r'\b\d{22,34}\b', extract_text)


def split_pdf(input_pdf_path, output_folder, matches):
    with pikepdf.open(input_pdf_path) as pdf:
        total_pages = len(pdf.pages)

        for page_num in range(total_pages):
            new_pdf = pikepdf.Pdf.new()
            new_pdf.pages.append(pdf.pages[page_num])

            # 使用匹配到的面单号作为文件名
            if page_num < len(matches):
                num_ = matches[page_num]
            else:
                num_ = f"page_{page_num + 1}"  # 如果没有匹配到，使用默认编号

            output_pdf_path = os.path.join(output_folder, f"{num_}.pdf")
            new_pdf.save(output_pdf_path)
            print(f"保存了 {output_pdf_path}")
