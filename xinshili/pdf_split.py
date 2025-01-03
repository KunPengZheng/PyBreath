import pikepdf
import pdfplumber
import re


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    # print(f"打印内容：{text}")
    return text


def split_pdf(input_pdf_path, output_folder):
    # 打开原始 PDF
    with pikepdf.open(input_pdf_path) as pdf:
        total_pages = len(pdf.pages)

        for page_num in range(total_pages):
            # 创建一个新的 PDF 实例
            new_pdf = pikepdf.Pdf.new()

            # 添加页面
            new_pdf.pages.append(pdf.pages[page_num])

            num_ = matches[page_num]

            # 设置输出文件名
            output_pdf_path = f"{output_folder}" + num_ + ".pdf"

            # 保存新 PDF 文件
            new_pdf.save(output_pdf_path)

            print(f"保存了 {output_pdf_path}")


# 示例使用
input_pdf = "/Users/zkp/Desktop/B&Y/pdf/新年礼物-01-03-12单.pdf"  # 输入 PDF 文件路径
output_folder = "/Users/zkp/Desktop/B&Y/pdf/"  # 输出目录路径

text = extract_text_from_pdf(input_pdf)

pattern = r'\b\d{22,34}\b'
matches = re.findall(pattern, text)

split_pdf(input_pdf, output_folder)
