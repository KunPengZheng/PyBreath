import os
import re
from openpyxl import load_workbook
import pandas as pd
from collections import Counter, defaultdict


def count_no_track(file_path, column_name="快递"):
    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]
        if column_name not in headers:
            raise ValueError(f"列名 '{column_name}' 不存在！")
        column_index = headers.index(column_name) + 1
        pattern = re.compile(r"^\s*无轨迹\s*$", re.IGNORECASE)
        total_count = 0
        no_track_count = 0
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            cell_value = row[column_index - 1]
            if cell_value is not None:
                total_count += 1
                if pattern.match(str(cell_value)):
                    no_track_count += 1
        return total_count, no_track_count
    except Exception as e:
        print(f"发生错误: {e}")
        return 0, 0


def count_warehouse_distribution(file_path, warehouse_column="发货仓库", courier_column="快递"):
    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]
        if warehouse_column not in headers or courier_column not in headers:
            raise ValueError(f"列名 '{warehouse_column}' 或 '{courier_column}' 不存在！")
        warehouse_index = headers.index(warehouse_column) + 1
        courier_index = headers.index(courier_column) + 1
        pattern = re.compile(r"^\s*无轨迹\s*$", re.IGNORECASE)
        warehouse_counter = Counter()
        warehouse_no_track_counter = defaultdict(int)
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            warehouse_name = row[warehouse_index - 1]
            courier_status = row[courier_index - 1]
            if warehouse_name is not None:
                warehouse_counter[warehouse_name] += 1
                if courier_status is not None and pattern.match(str(courier_status)):
                    warehouse_no_track_counter[warehouse_name] += 1
        return warehouse_counter, warehouse_no_track_counter
    except Exception as e:
        print(f"发生错误: {e}")
        return Counter(), defaultdict(int)


def count_store_distribution_and_no_track(file_path, store_column="店铺", courier_column="快递"):
    """
    统计店铺列的分布情况以及对应的 '无轨迹' 数量。
    :param file_path: Excel 文件路径
    :param store_column: 店铺列名
    :param courier_column: 快递列名
    :return: 各店铺的总数和 '无轨迹' 数量的 Counter 对象
    """
    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]
        if store_column not in headers or courier_column not in headers:
            raise ValueError(f"列名 '{store_column}' 或 '{courier_column}' 不存在！")
        store_index = headers.index(store_column) + 1
        courier_index = headers.index(courier_column) + 1
        pattern = re.compile(r"^\s*无轨迹\s*$", re.IGNORECASE)
        store_counter = Counter()
        store_no_track_counter = Counter()
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            store_name = row[store_index - 1]
            courier_status = row[courier_index - 1]
            if store_name is not None:
                store_counter[store_name] += 1
                if courier_status is not None and pattern.match(str(courier_status)):
                    store_no_track_counter[store_name] += 1
        return store_counter, store_no_track_counter
    except Exception as e:
        print(f"发生错误: {e}")
        return Counter(), Counter()


def handle_file(input_file):
    file_extension = os.path.splitext(input_file)[1].lower()
    file_dir = os.path.dirname(input_file)
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    if file_extension == '.csv':
        xlsx_file_path = os.path.join(file_dir, f"{file_name}.xlsx")
        try:
            data = pd.read_csv(input_file, encoding='utf-8')
            data.to_excel(xlsx_file_path, index=False)
            print(f"已将 CSV 文件转换为 XLSX 文件：{xlsx_file_path}")
            os.remove(input_file)
            print(f"已删除原始 CSV 文件：{input_file}")
            return xlsx_file_path
        except Exception as e:
            print(f"处理 CSV 文件时发生错误：{e}")
            return None
    else:
        print("文件不是 CSV 格式，执行其他逻辑")
        return input_file


# 主程序
input_file = input("请输入文件的绝对路径：")
xlsx_path = handle_file(input_file)

# 统计 "快递" 列的相关信息
total_count, no_track_count = count_no_track(xlsx_path, column_name="快递")
print(f"总条数（除列头）：{total_count}")
print(f"内容为 '无轨迹' 的总数：{no_track_count}")

# 统计 "发货仓库" 分布及对应的 "无轨迹" 数量
warehouse_distribution, warehouse_no_track = count_warehouse_distribution(
    xlsx_path, warehouse_column="发货仓库", courier_column="快递"
)

print("\n发货仓库分布情况：")
for warehouse, count in warehouse_distribution.items():
    no_track_count = warehouse_no_track[warehouse]
    print(f"{warehouse}: 总数 {count} 条，其中 '无轨迹' {no_track_count} 条")

# 统计店铺分布情况及 '无轨迹' 数量
store_distribution, store_no_track_distribution = count_store_distribution_and_no_track(
    xlsx_path, store_column="店铺", courier_column="快递"
)

print("\n店铺分布及对应的 '无轨迹' 情况：")
for store, count in store_distribution.items():
    no_track_count = store_no_track_distribution[store]
    print(f"{store}: 总数 {count} 条，其中 '无轨迹' {no_track_count} 条")