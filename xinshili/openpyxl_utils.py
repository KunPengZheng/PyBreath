from openpyxl import load_workbook
from openpyxl.utils import get_column_letter


def load_excel_file(file_path):
    """
    加载 Excel 文件
    """
    try:
        return load_workbook(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"未找到文件: {file_path}")
    except Exception as e:
        raise Exception(f"加载文件 {file_path} 时发生错误: {e}")


def get_active_sheet(workbook):
    """
    获取活动表
    """
    try:
        return workbook.active
    except Exception as e:
        raise Exception(f"获取活动表时发生错误: {e}")


def find_column(sheet, column_name):
    """
    动态查找指定列名的列号。

    :param sheet: openpyxl 的 Worksheet 对象，表示 Excel 工作表。
    :param column_name: 需要查找的单一列名（字符串）。
    :return: 对应的列号（整数）。
    :raises: 如果未找到指定列名，抛出 ValueError。

    eg: find_column(sheet,"价格")
    """
    try:
        # 遍历工作表的每一列
        for col in sheet.iter_cols(1, sheet.max_column):
            # 获取当前列的第一行值（表头）
            header = col[0].value

            # 如果表头匹配目标列名，返回对应的列号
            if header == column_name:
                return col[0].column

        # 如果未找到目标列名，抛出异常
        raise ValueError(f"未找到列名: {column_name}")

    except Exception as e:
        # 捕获异常，并抛出自定义错误信息
        raise Exception(f"查找列时发生错误: {e}")


def find_columns(sheet, column_names):
    """
    动态查找多个列名的列号。

    :param sheet: openpyxl 的 Worksheet 对象，表示 Excel 工作表。
    :param column_names: 需要查找的列名列表（list）。
    :return: 包含列名和对应列号的字典 {列名: 列号}。
    :raises: 当某些列名未找到时，抛出 ValueError。
    """
    column_map = {}
    missing_columns = []

    for column_name in column_names:
        try:
            # 调用单列查找函数
            column_map[column_name] = find_column(sheet, column_name)
        except ValueError:
            # 如果列名未找到，记录到缺失列表
            missing_columns.append(column_name)

    # 如果有未找到的列名，抛出异常
    if missing_columns:
        raise ValueError(f"未找到以下列名: {missing_columns}")

    return column_map


def get_cell_value(sheet, row, column):
    """
    通过 openpyxl 获取工作表 sheet 中第 row 行的 column 列单元格的值
    eg: get_columns_value_by_row(sheet1,1,"A")
    """
    return sheet.cell(row, column).value


def get_merged_cell_value(sheet, row, col):
    """
    获取合并单元格的内容，如果单元格是合并区域中的一部分，获取合并区域的左上角单元格的值。
    :param sheet: 工作表
    :param row: 行号
    :param col: 列号
    :return: 单元格的值
    """
    # 遍历所有合并单元格的区域
    for merged_cell in sheet.merged_cells.ranges:
        # 检查当前单元格是否在合并单元格的范围内
        if merged_cell.min_row <= row <= merged_cell.max_row and merged_cell.min_col <= col <= merged_cell.max_col:
            # 如果该单元格在合并区域内，则返回该合并区域的左上角单元格的值
            top_left_cell = sheet.cell(row=merged_cell.min_row, column=merged_cell.min_col)
            return top_left_cell.value

    # 如果没有合并单元格，直接返回单元格的值
    return sheet.cell(row=row, column=col).value


def set_cell_value(sheet, row, column, value):
    """
    通过 openpyxl 设置工作表 sheet 中第 row 行的 column 列单元格的值
    eg: set_columns_value_by_row(sheet1,1,"A","黑色")
    """
    sheet.cell(row, column).value = value


def generate_column_name():
    """
    生成从 A 列到 BZ 列的常量，例如 column_A = "A"
    """
    for i in range(1, 79):  # 1 到 78 对应 A 到 BZ
        column_letter = get_column_letter(i)
        print(f"column_{column_letter} = \"{column_letter}\"")


def generate_column_value():
    """
    生成 A 列到 BZ 列对应的数字常量，例如 column_A = "1"
    """
    columns = {}
    for i in range(1, 79):  # 1 到 78 对应 A 到 BZ
        column_letter = get_column_letter(i)  # 获取列名
        columns[column_letter] = i

    # 打印常量
    for col, num in columns.items():
        print(f"column_{col} = {num}")


def get_max_row(sheet):
    # 获取最大行号
    return sheet.max_row
