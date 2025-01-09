import os
import xlwings as xw


def merge_based_on_largest_header(input_folder, output_file):
    """
    合并文件夹中多个文件的相同列名数据，选择表头最多的文件作为模板。

    :param input_folder: 文件夹路径，包含多个 Excel 文件
    :param output_file: 输出的合并结果文件路径
    """
    app = xw.App(visible=False)
    try:
        # 读取所有文件表头长度并找到表头最多的文件
        largest_header_file = None
        largest_header = []
        for file_name in os.listdir(input_folder):
            if file_name.endswith(".xlsx"):
                file_path = os.path.join(input_folder, file_name)
                wb = app.books.open(file_path)
                ws = wb.sheets[0]
                headers = ws.range("A1").expand("right").value
                if len(headers) > len(largest_header):
                    largest_header = headers
                    largest_header_file = file_path
                wb.close()

        if not largest_header_file:
            raise FileNotFoundError("未找到任何 .xlsx 文件")

        print(f"表头最多的文件: {largest_header_file}")
        print(f"表头内容: {largest_header}")

        # 创建结果数据字典
        result_data = {header: [] for header in largest_header}

        # 遍历所有文件并合并数据
        for file_name in os.listdir(input_folder):
            if file_name.endswith(".xlsx"):
                file_path = os.path.join(input_folder, file_name)
                wb = app.books.open(file_path)
                ws = wb.sheets[0]
                headers = ws.range("A1").expand("right").value
                rows = ws.range("A2").expand("table").value if ws.range("A2").value else []

                # 将行数据转换为字典形式
                for row in rows:
                    row_dict = {headers[idx]: row[idx] for idx in range(len(headers)) if headers[idx] in result_data}
                    for header in largest_header:
                        value = row_dict.get(header, None)
                        # 如果是运单号列，强制转换为字符串并处理为文本形式
                        if header == "运单号" and value is not None:
                            value = f"'{str(value)}"  # 添加前置单引号，确保Excel读取为文本格式
                        result_data[header].append(value)

                wb.close()

        # 写入合并结果到输出文件
        output_wb = app.books.add()
        output_ws = output_wb.sheets[0]

        # 写入表头
        output_ws.range("A1").value = list(result_data.keys())

        # 写入数据
        output_ws.range("A2").value = list(zip(*result_data.values()))

        # 强制设置运单号列为文本格式
        for col_idx, header in enumerate(result_data.keys(), start=1):
            if header == "运单号":
                column_range = output_ws.range(output_ws.cells(2, col_idx), output_ws.cells(len(result_data[header]) + 1, col_idx))
                column_range.number_format = "@"  # 设置为文本格式

        # 自动调整列宽
        output_ws.autofit()

        # 保存结果文件
        output_wb.save(output_file)
        output_wb.close()
        print(f"合并完成，结果已保存到: {output_file}")

    except Exception as e:
        print(f"执行过程中发生错误: {e}")
    finally:
        app.quit()


# 示例使用
input_folder = "/Users/zkp/Desktop/B&Y/合并/mult"  # 替换为存放 Excel 文件的文件夹路径
output_file = "/Users/zkp/Desktop/B&Y/合并/mult/combined.xlsx"  # 替换为输出文件路径
merge_based_on_largest_header(input_folder, output_file)