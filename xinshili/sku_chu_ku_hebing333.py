import csv
from collections import defaultdict
from openpyxl import Workbook


def extract_and_count_sku_from_csv_to_xlsx(input_file, output_file, column_name="SKU"):
    """
    从 CSV 文件提取 SKU 列中的内容，以 `*` 为分隔符统计每个标识的数量，并输出为 XLSX 文件。

    :param input_file: 输入 CSV 文件路径
    :param output_file: 输出统计结果的 XLSX 文件路径
    :param column_name: 要统计的列名，默认是 "SKU"
    """
    try:
        # 初始化统计字典
        sku_counts = defaultdict(int)

        # 打开 CSV 文件并读取
        with open(input_file, mode="r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            if column_name not in reader.fieldnames:
                raise ValueError(f"列名 '{column_name}' 不存在于文件中")

            # 遍历文件行
            for row in reader:
                sku_data = row[column_name]
                if not sku_data:
                    continue

                # 分割并统计 SKU
                for part in sku_data.split():
                    if "*" in part:
                        sku, count = part.split("*")
                        sku_counts[sku] += int(count)

        # 创建新的 XLSX 文件并写入统计结果
        wb = Workbook()
        ws = wb.active
        ws.title = "SKU统计"

        # 写入表头
        ws.append(["SKU", "数量"])

        # 写入数据
        for sku, count in sku_counts.items():
            ws.append([sku, count])

        # 自动调整列宽
        for column_cells in ws.columns:
            max_length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
            col_letter = column_cells[0].column_letter
            ws.column_dimensions[col_letter].width = max_length + 2

        # 保存文件
        wb.save(output_file)
        print(f"统计完成，结果已保存到: {output_file}")

    except Exception as e:
        print(f"执行过程中发生错误: {e}")


if __name__ == "__main__":
    # 示例输入和输出路径
    input_csv_file = "/Users/zkp/Desktop/B&Y/库存_统计sku/91单减库存_1 (1).csv"  # 替换为实际输入 CSV 文件路径
    output_xlsx_file = "/Users/zkp/Desktop/B&Y/库存_统计sku/91单减库存_1 (1)_统计.xlsx"  # 替换为实际输出 XLSX 文件路径

    # 调用统计函数
    extract_and_count_sku_from_csv_to_xlsx(input_csv_file, output_xlsx_file)
