import os
import re
from openpyxl import load_workbook
import pandas as pd


def count_no_track(file_path, column_name="快递"):
    try:
        # 加载 Excel 文件
        workbook = load_workbook(file_path)
        sheet = workbook.active  # 默认读取第一个表

        # 获取列头
        headers = [cell.value for cell in sheet[1]]

        # 确定目标列的索引
        if column_name not in headers:
            raise ValueError(f"列名 '{column_name}' 不存在！")

        column_index = headers.index(column_name) + 1

        # 定义正则模式用于匹配 "无轨迹"（忽略空格和大小写）
        pattern = re.compile(r"^\s*无轨迹\s*$", re.IGNORECASE)

        # 遍历数据行统计总数和 "无轨迹" 的数量
        total_count = 0
        no_track_count = 0

        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            cell_value = row[column_index - 1]
            if cell_value is not None:
                total_count += 1
                if pattern.match(str(cell_value)):  # 使用正则匹配
                    no_track_count += 1

        return total_count, no_track_count

    except Exception as e:
        print(f"发生错误: {e}")
        return 0, 0


def handle_file(input_file):
    # 获取文件后缀
    file_extension = os.path.splitext(input_file)[1].lower()  # 获取文件后缀，转为小写
    file_dir = os.path.dirname(input_file)  # 获取文件路径
    file_name = os.path.splitext(os.path.basename(input_file))[0]  # 文件名不带后缀

    if file_extension == '.csv':
        # CSV 转换为 XLSX
        xlsx_file_path = os.path.join(file_dir, f"{file_name}.xlsx")
        try:
            # 读取 CSV 文件
            data = pd.read_csv(input_file, encoding='utf-8')
            # 保存为 XLSX 文件
            data.to_excel(xlsx_file_path, index=False)
            print(f"已将 CSV 文件转换为 XLSX 文件：{xlsx_file_path}")

            # 删除原始 CSV 文件
            os.remove(input_file)
            print(f"已删除原始 CSV 文件：{input_file}")

            return xlsx_file_path
        except Exception as e:
            print(f"处理 CSV 文件时发生错误：{e}")
            return None
    else:
        # 如果不是 CSV 文件，直接返回路径
        print("文件不是 CSV 格式，执行其他逻辑")
        return input_file


input_file = input("请输入文件的绝对路径：")
xlsx_path = handle_file(input_file)
total_count, no_track_count = count_no_track(xlsx_path, column_name="快递")
print(f"总条数（除列头）：{total_count}")
print(f"内容为 '无轨迹' 的总数：{no_track_count}")
