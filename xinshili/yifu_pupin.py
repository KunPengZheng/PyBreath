import re
import os
from openpyxl import load_workbook


def lenb_minus_len(text):
    """
    计算类似 Excel 公式 LENB(A1) - LEN(A1) 的值：
    计算字符串中所有中文字符和中文符号占用的字节数与字符数的差值
    """
    if not isinstance(text, str):  # 处理 None 或非字符串情况
        return 0

    # 匹配所有中文字符（基本汉字 + 符号）
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')  # 匹配汉字
    # 中文符号（全角标点）
    chinese_symbols = re.compile(r'[，。？！【】（）《》“”‘’：；￥— –]')  # 匹配常见中文符号，包括破折号（—）

    chinese_chars = chinese_pattern.findall(text) + chinese_symbols.findall(text)  # 获取所有中文字符+符号

    # 计算 UTF-8 编码后的字节数
    utf8_length = len(text.encode('utf-8'))
    # 计算普通字符长度
    char_length = len(text)
    # 计算额外的字节数（相当于 Excel 公式 LENB(A1) - LEN(A1)）
    extra_bytes = utf8_length - char_length
    return extra_bytes


def replace_chinese_symbols(text):
    """
    替换中文符号为对应的英文符号
    """
    if not isinstance(text, str):  # 处理 None 或非字符串情况
        return ""

    # 定义符号映射（中文符号 -> 英文符号）
    symbol_map = {
        "，": ",", "。": ".", "？": "?", "！": "!", "【": "[", "】": "]",
        "（": "(", "）": ")", "《": "<", "》": ">", "“": "\"", "”": "\"",
        "‘": "'", "’": "'", "：": ":", "；": ";", "￥": "$", "—": "-", "–": "-",
        "m²": "", "｜": "", "®": "", "™": "", "©": "", "2024": "2025", "ö": "",
        "Lord": "",
        "Psalm": "",
        "Disneyland": "",
        "Jesus": "",
        "Ukraine": "",
        "Toy Story": "",
        "Disney": "",
        "Mickey": "",
        "nike": "",
        "Doraemon": "",
    }

    # 使用正则替换，忽略大小写
    for zh_symbol, en_symbol in symbol_map.items():
        text = re.sub(re.escape(zh_symbol), en_symbol, text, flags=re.IGNORECASE)

    return text


def process_excel(filepath, column_letter="B", result_column_b="E", result_column_c="D"):
    """
    读取 Excel 文件：
    1. 计算 `LENB(A1) - LEN(A1)` 差值，写入 B 列
    2. 替换中文符号为英文符号，写入 C 列
    """
    workbook = load_workbook(filename=filepath)
    sheet = workbook.active  # 选择默认工作表

    for row in range(1, sheet.max_row + 1):  # 遍历所有行
        cell = sheet[f"{column_letter}{row}"]  # 读取 A 列的单元格
        text = str(cell.value) if cell.value else ""  # 处理空值

        # 计算中文字符和符号的字节差值
        # difference = lenb_minus_len(text)
        # sheet[f"{result_column_b}{row}"] = difference

        # 替换中文符号为英文符号
        replaced_text = replace_chinese_symbols(text)
        sheet[f"{result_column_c}{row}"] = replaced_text

    # 保存 Excel
    workbook.save(filepath)
    print(f"处理完成，已更新 {filepath}")


def rename_files_in_folder(folder_path, index=1):
    # 获取文件夹中的所有文件
    files = sorted(os.listdir(folder_path))  # 按名称排序，避免乱序

    for file in files:
        old_path = os.path.join(folder_path, file)

        # 确保是文件，而不是文件夹
        if os.path.isfile(old_path):
            file_extension = os.path.splitext(file)[1]  # 获取文件扩展名
            new_name = f"{index}{file_extension}"  # 生成新文件名
            new_path = os.path.join(folder_path, new_name)

            # 避免文件名冲突
            while os.path.exists(new_path):
                index += 1
                new_name = f"{index}{file_extension}"
                new_path = os.path.join(folder_path, new_name)

            os.rename(old_path, new_path)  # 重命名文件
            print(f"重命名: {file} → {new_name}")
            index += 1  # 递增索引


process_excel("/Users/zkp/Desktop/未命名文件夹/20250303黑色女装标题.xlsx")
process_excel("/Users/zkp/Desktop/未命名文件夹/20250304黑色女装标题.xlsx")
process_excel("/Users/zkp/Desktop/未命名文件夹/20250305白色女装标题J041-K080.xlsx")
process_excel("/Users/zkp/Desktop/未命名文件夹/20250306白色女装标题K081-K100.xlsx")
process_excel("/Users/zkp/Desktop/未命名文件夹/20250306黑色女装标题L001-L100.xlsx")
process_excel("/Users/zkp/Desktop/未命名文件夹/20250308白色女装标题.xlsx")
process_excel("/Users/zkp/Desktop/未命名文件夹/20250310黑色女装标题.xlsx")
process_excel("/Users/zkp/Desktop/未命名文件夹/20250310黑色女装标题H301-H400.xlsx")

# rename_files_in_folder(r"/Users/zkp/Desktop/0315服装230/图片")


