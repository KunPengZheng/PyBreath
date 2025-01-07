import xlwings as xw


def xw_map(file_path):
    try:
        # 打开 Excel 应用程序（隐藏窗口）
        app = xw.App(visible=False)
        workbook = xw.Book(file_path)  # 打开指定的 Excel 文件
        sheet = workbook.sheets[0]  # 使用第一个工作表
        return {"app": app, "sheet": sheet, "workbook": workbook}
    except Exception as e:
        raise Exception(f"错误: {e}")


def xw_save(workbook, app):
    # 保存并关闭
    workbook.save()
    workbook.close()
    app.quit()


def beautify(sheet):
    """
    美化
    """
    try:
        used_range = sheet.used_range  # 获取可用区间
        used_range.columns.autofit()  # 自动调整所有列宽
        used_range.rows.autofit()  # 自动调整所有行高
        used_range.api.HorizontalAlignment = -4108  # xlCenter，水平居中
        used_range.api.VerticalAlignment = -4108  # xlCenter，垂直居中
    except Exception as e:
        raise Exception(f"错误: {e}")


def calculate_formula_1(sheet, file_path, column_list, target_column, callback):
    """
    获取指定列每一行的内容，然后赋值到对应行指定列

    :param file_path: openpyxl 的 Worksheet 对象，表示 Excel 工作表。
    :param column_list: 需要查找的列名列表（list）。
    :param target_column: 需要赋值的列名。
    :param callback: 计算规则的回调由调用者指定。
    :raises: 异常。
    """
    try:
        # range包头不包尾，所以+1
        for row in range(2, sheet.used_range.last_cell.row + 1):
            column_result_dic = {}  # 空字典
            for i in range(len(column_list)):
                # sheet.range(f"{column_list[i]}{row}").value 获取某个单元格的值
                column_result_dic[column_list[i]] = sheet.range(f"{column_list[i]}{row}").value  # 添加
                pass
            # print(row, column_result_dic)
            # 单元格赋值
            sheet.range(f"{target_column}{row}").value = callback(column_result_dic)

    except Exception as e:
        raise Exception(f"错误: {e}")


def get_last_row_num(sheet, column_name):
    """
    获取指定列最后一行有数据的行号

    :param column_name: 列名字
    """
    return sheet.range(column_name + str(sheet.cells.last_cell.row)).end('up').row


def get_range_row_value(sheet, column_name, start_row, last_row):
    """
    读取指定范围的所有值，并返回一个列表（或单个值，如果范围只有一个单元格）

    :param column_name: 列名字
    :param start_row: 开始行号
    :param last_row: 结束行号
    """
    return sheet.range(f'{column_name}{start_row}:{column_name}{last_row}').value


def set_cell_value(sheet, column_name, row_value, value):
    """
    设置指定单元格单元格内容

    :param column_name: 列名字
    :param row_value: 指定行号
    :param value: 赋值内容
    """
    sheet.range(f"{column_name}{row_value}").value = value
