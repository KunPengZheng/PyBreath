import os

import fitz
import pikepdf
import re

from openpyxl.workbook import Workbook

from xinshili.utils import get_filename_without_extension, ensure_directory_exists


def save_waybill_numbers_to_excel(waybill_numbers, output_folder):
    """
    将运单号逐行写入到 Excel 文件
    """
    wb = Workbook()
    ws = wb.active
    # ws.title = "运单号"

    # 写入标题行
    ws.append(["运单号"])

    # 写入运单号
    for number in waybill_numbers:
        ws.append([number])

    # 保存文件
    output_file_path = os.path.join(output_folder, "运单号列表.xlsx")
    wb.save(output_file_path)
    print(f"运单号列表已保存为：{output_file_path}")


def split_pdf(input_pdf_path, output_folder):
    """
    裁剪pdf
    :param input_pdf_path: 需要裁剪pdf文件路径
    :param output_folder: 裁剪后的pdf输出的文件夹
    """
    with pikepdf.open(input_pdf_path) as pdf:
        for page_num in range(len(pdf.pages)):
            new_pdf = pikepdf.Pdf.new()
            new_pdf.pages.append(pdf.pages[page_num])
            output_pdf_path = os.path.join(output_folder, f"page_{page_num + 1}.pdf")
            new_pdf.save(output_pdf_path)


def extract_text_from_pdf(folder_path):
    """
    裁剪pdf
    :param folder_path: pdf的文件路径
    """
    for root, dirs, files in os.walk(folder_path):  # 遍历文件夹
        nums = []  # 扫描到的名单号
        for file in files:
            absolute_path = os.path.join(root, file)  # 拼接绝对路径
            doc = fitz.open(absolute_path)
            text = ""
            for page in doc:
                text += page.get_text().replace(" ", "")  # 提取文本内容
                print(f"{absolute_path}  文件扫描到的内容：")
                print(text)
            findall = re.findall(r'\b\d{22,34}\b', text)
            print(f"{absolute_path} 文件正则匹配到的面单号：{findall}")
            print()
            # 判断 findall 列表不为空并且 findall[0] 存在，表示匹配到了。如果没匹配到的不会以名单号重命名
            if findall and findall[0]:
                os.rename(absolute_path, os.path.dirname(absolute_path) + "/" + findall[0] + ".pdf")
                # 记录单号
                nums.append(findall[0])
        save_waybill_numbers_to_excel(nums, folder_path)


def extract_text_from_pdf_not_sku(folder_path):
    """
    裁剪pdf
    :param folder_path: pdf的文件路径
    """
    for root, dirs, files in os.walk(folder_path):  # 遍历文件夹
        nums = []  # 扫描到的名单号
        for file in files:
            absolute_path = os.path.join(root, file)  # 拼接绝对路径
            doc = fitz.open(absolute_path)
            text = ""
            for page in doc:
                text += page.get_text().replace(" ", "")  # 提取文本内容
                print(f"{absolute_path}  文件扫描到的内容：")
                print(text)
            findall = re.findall(r'\b\d{22,34}\b', text)
            print(f"{absolute_path} 文件正则匹配到的面单号：{findall}")
            print()
            if '*' not in text:  # 筛选没有 *（一般指面单上指没带sku）
                # 判断 findall 列表不为空并且 findall[0] 存在，表示匹配到了。如果没匹配到的不会以名单号重命名
                if findall and findall[0]:
                    os.rename(absolute_path, os.path.dirname(absolute_path) + "/" + findall[0] + ".pdf")
                    # 记录单号
                    nums.append(findall[0])
        save_waybill_numbers_to_excel(nums, folder_path)

#
# # 示例使用
# input_pdf = input("请输入源表文件的绝对路径：")
# output_folder = "/Users/zkp/Desktop/B&Y/pdf/" + get_filename_without_extension(input_pdf) + "/"  # 输出目录路径
# ensure_directory_exists(output_folder)
#
# split_pdf(input_pdf, output_folder)
# extract_text_from_pdf(output_folder)
