import xlwings as xw


def beautify(file_path):
    """
    美化
    """
    try:
        # 打开 Excel 应用程序（隐藏窗口）
        app = xw.App(visible=False)
        workbook = xw.Book(file_path)  # 打开指定的 Excel 文件
        sheet = workbook.sheets[0]  # 使用第一个工作表

        used_range = sheet.used_range  # 获取可用区间
        used_range.columns.autofit()  # 自动调整所有列宽
        used_range.rows.autofit()  # 自动调整所有行高
        used_range.api.HorizontalAlignment = -4108  # xlCenter，水平居中
        used_range.api.VerticalAlignment = -4108  # xlCenter，垂直居中

        # 保存并关闭
        workbook.save()
        workbook.close()
        app.quit()

    except Exception as e:
        raise Exception(f"错误: {e}")


def calculate_formula_1(file_path, column_list, target_column, callback):
    """
    获取指定列每一行的内容，然后赋值到对应行指定列

    :param file_path: openpyxl 的 Worksheet 对象，表示 Excel 工作表。
    :param column_list: 需要查找的列名列表（list）。
    :param target_column: 需要赋值的列名。
    :param callback: 计算规则的回调由调用者指定。
    :raises: 异常。
    """
    try:
        # 打开 Excel 应用程序（隐藏窗口）
        app = xw.App(visible=False)
        workbook = xw.Book(file_path)  # 打开指定的 Excel 文件
        sheet = workbook.sheets[0]  # 使用第一个工作表

        # range包头不包尾，所以+1
        for row in range(2, sheet.used_range.last_cell.row + 1):
            column_result_dic = {}  # 空字典
            for i in range(len(column_list)):
                # sheet.range(f"{column_list[i]}{row}").value 获取某个单元格的值
                column_result_dic[column_list[i]] = sheet.range(f"{column_list[i]}{row}").value  # 添加
                pass
            print(row, column_result_dic)
            # 单元格赋值
            sheet.range(f"{target_column}{row}").value = callback(column_result_dic)

        # 保存并关闭
        workbook.save()
        workbook.close()
        app.quit()

    except Exception as e:
        raise Exception(f"错误: {e}")
