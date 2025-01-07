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


def calculate_formula(sheet, column_list, target_column, callback):
    """
    根据指定规则计算值并写入目标列。

    :param sheet: Excel 工作表对象。
    :param column_list: 需要读取的列名列表（list）。
    :param target_column: 需要赋值的目标列名。
    :param callback: 计算规则的回调函数，由调用者定义。
    :raises Exception: 如果发生错误，抛出异常。
    """
    try:
        # 遍历从第二行到最后一行的数据
        # 2 是起始值，表示从 Excel 工作表的第 2 行开始遍历（一般第 1 行是表头，所以从第 2 行开始处理实际数据）。
        # range 的结束值是非包含的，因此要加 1 才能遍历到最后一行。
        # ⚠️： sheet.used_range.last_cell.row 返回的是 Excel 工作表中最后一个“使用过”的单元格的行号，而不仅仅是有效数据的行号。
        for row in range(2, sheet.used_range.last_cell.row + 1):
            column_result_dic = {}  # 用于存储当前行的列值

            # 读取指定列的值
            for col in column_list:
                cell_value = sheet.range(f"{col}{row}").value
                column_result_dic[col] = cell_value

            # print(f"Row {row}: {column_result_dic}")

            # 如果所有需要的列值都存在，则进行计算
            if all(column_result_dic[col] is not None for col in column_list):
                calculated_value = callback(column_result_dic)
                sheet.range(f"{target_column}{row}").value = calculated_value
            else:
                print(f"Row {row} has missing values, skipping calculation.")

    except Exception as e:
        raise Exception(f"Error during calculation: {e}")


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
