from openpyxl import load_workbook, Workbook


def aggregate_and_save(input_file, output_file):
    """
    汇总 SKU 和客户的出库数量，并对客户列排序后保存到新的文件。
    :param input_file: 输入文件路径
    :param output_file: 输出文件路径
    """
    try:
        # 加载输入文件
        wb = load_workbook(input_file)
        sheet = wb.active

        # 获取列索引
        data = sheet.iter_rows(min_row=2, values_only=True)  # 跳过表头
        header = [cell.value for cell in sheet[1]]  # 获取表头
        ar_index = header.index("SKU")
        az_index = header.index("Outbound Qty/出库数量")
        b_index = header.index("Client/客户")

        # 汇总数据到字典
        result_dict = {}
        for row in data:
            ar_value = row[ar_index]
            az_value = row[az_index]
            b_value = row[b_index]

            if ar_value is not None and b_value is not None:
                key = (ar_value, b_value)
                result_dict[key] = result_dict.get(key, 0) + (az_value if isinstance(az_value, (int, float)) else 0)

        # 对结果按客户列排序（其次按 SKU 排序）
        sorted_results = sorted(result_dict.items(), key=lambda x: (x[0][1], x[0][0]))

        # 创建新的工作簿
        new_wb = Workbook()
        new_sheet = new_wb.active
        new_sheet.title = "汇总结果"

        # 写入表头
        new_sheet.append(["SKU", "Client/客户", "Outbound Qty/出库数量"])

        # 写入汇总结果
        for (ar, b), total in sorted_results:
            new_sheet.append([ar, b, total])

        # 保存到新文件
        new_wb.save(output_file)
        print(f"汇总结果已保存到文件: {output_file}")

    except Exception as e:
        print(f"执行过程中发生错误: {e}")


input_file2 = "/Users/zkp/Desktop/B&Y/未命名文件夹/ParcelOutbound_20250112125241.xlsx"
output_file2 = "/Users/zkp/Desktop/B&Y/未命名文件夹/ParcelOutbound_20250112125241_temp.xlsx"
aggregate_and_save(input_file2, output_file2)
