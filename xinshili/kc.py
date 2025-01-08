import xlwings as xw


def merge_and_sum_sku(input_file, output_file):
    """
    将 SKU 列相同内容的行合并，并将对应的产品总数列的数值相加
    :param input_file: 输入 Excel 文件路径
    :param output_file: 输出 Excel 文件路径
    """
    app = xw.App(visible=False)  # 隐藏 Excel 窗口
    try:
        # 打开输入文件
        wb = app.books.open(input_file)
        sheet = wb.sheets.active  # 获取活动工作表

        # 获取数据范围
        data = sheet.range("A1").expand("table").value  # 获取整个表格数据
        header = data[0]  # 表头
        rows = data[1:]  # 数据部分

        # 检查列名
        if "SKU" not in header or "产品总数" not in header:
            raise ValueError("表格中未找到 'sku' 或 '产品总数' 列，请检查数据格式。")

        # 获取列索引
        sku_index = header.index("SKU")
        product_total_index = header.index("产品总数")

        # 使用字典合并数据
        result_dict = {}
        for row in rows:
            sku = str(row[sku_index]).strip() if row[sku_index] else None
            product_total = row[product_total_index] if isinstance(row[product_total_index], (int, float)) else 0
            if sku:
                result_dict[sku] = result_dict.get(sku, 0) + product_total

        # 转换为列表形式
        result_data = [["SKU", "产品总数"]]  # 新表头
        result_data.extend([[sku, total] for sku, total in result_dict.items()])

        # 写入新工作表
        new_sheet = wb.sheets.add(name="合并结果")
        new_sheet.range("A1").value = result_data

        # 保存输出文件
        wb.save(output_file)
        print(f"合并结果已保存到: {output_file}")

    except Exception as e:
        print(f"执行过程中发生错误: {e}")
    finally:
        app.quit()


# 示例使用
input_file = "/Users/zkp/Downloads/order_120250108092648725_1573179_副本.xlsx"  # 输入文件路径
output_file = "/Users/zkp/Downloads/xsxsxs.xlsx"  # 输出文件路径
merge_and_sum_sku(input_file, output_file)
