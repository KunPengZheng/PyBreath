from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment


def expand_sku_rows(file1, file2, output_file, sku_column_file1="SKU", box_column_file1="总共箱数",
                    sku_column_file2="SKU/SKU"):
    """
    根据文件 1 的 SKU 和箱数，将 SKU 数据按箱数扩展后，复制到文件 2 的 SKU/SKU 列中。

    :param file1: 输入的 Excel 文件 1，包含 SKU 和箱数
    :param file2: 输入的 Excel 文件 2，目标 SKU 列
    :param output_file: 输出的 Excel 文件路径
    :param sku_column_file1: 文件 1 中的 SKU 列名
    :param box_column_file1: 文件 1 中的箱数列名
    :param sku_column_file2: 文件 2 中的 SKU 列名
    """
    try:
        # 加载文件 1
        wb1 = load_workbook(file1, data_only=True)
        ws1 = wb1.active

        # 获取文件 1 的列名到索引的映射
        headers_file1 = {cell.value: idx for idx, cell in enumerate(ws1[1])}

        # 确保列名存在
        if sku_column_file1 not in headers_file1 or box_column_file1 not in headers_file1:
            raise ValueError(f"文件 1 中未找到列: {sku_column_file1} 或 {box_column_file1}")

        # 提取文件 1 的 SKU 和箱数
        sku_idx_file1 = headers_file1[sku_column_file1]
        box_idx_file1 = headers_file1[box_column_file1]

        expanded_rows = []
        for row in ws1.iter_rows(min_row=2, values_only=True):
            sku = row[sku_idx_file1]
            box_count = row[box_idx_file1]
            if sku and isinstance(box_count, (int, float)):  # 确保 SKU 和箱数有效
                expanded_rows.extend([sku] * int(box_count))

        # 加载文件 2
        wb2 = load_workbook(file2)
        ws2 = wb2.active

        # 获取目标列的索引
        headers_file2 = {cell.value: idx for idx, cell in enumerate(ws2[1])}
        if sku_column_file2 not in headers_file2:
            raise ValueError(f"文件 2 中未找到列: {sku_column_file2}")

        sku_idx_file2 = headers_file2[sku_column_file2]

        # 清空目标列的数据并填充扩展数据
        for row_idx in range(2, ws2.max_row + 1):
            ws2.cell(row=row_idx, column=sku_idx_file2 + 1).value = None

        for idx, sku in enumerate(expanded_rows, start=2):
            ws2.cell(row=idx, column=sku_idx_file2 + 1).value = sku

        # 调整单元格宽度并居中
        for column_cells in ws2.columns:
            max_length = 0
            column_letter = column_cells[0].column_letter
            for cell in column_cells:
                if cell.value:
                    cell_length = len(str(cell.value))
                    if cell_length > max_length:
                        max_length = cell_length
                    cell.alignment = Alignment(horizontal="center", vertical="center")
            adjusted_width = max_length + 2
            ws2.column_dimensions[column_letter].width = adjusted_width

        # 保存输出文件
        wb2.save(output_file)
        print(f"结果已保存到文件: {output_file}")

    except Exception as e:
        print(f"执行过程中发生错误: {e}")


# 示例调用
file1_path = "/Users/zkp/Desktop/B&Y/入库单/zbw/zyl美西改美中仓库.xlsx"  # 替换为 Excel 文件 1 的路径
file2_path = "/Users/zkp/Desktop/B&Y/入库单/zbw/入库模版.xlsx"  # 替换为 Excel 文件 2 的路径
output_file_path = "/Users/zkp/Desktop/B&Y/入库单/zbw/output.xlsx"  # 替换为输出文件路径

expand_sku_rows(file1_path, file2_path, output_file_path)
