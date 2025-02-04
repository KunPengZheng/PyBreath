import openpyxl
import pandas as pd

from xinshili.gjgz_plus111 import check_and_add_courier_column, extract_and_process_data, RowName, CourierStateMapKey, \
    update_courier_status_for_results


def remove_duplicates_by_column(input_file, column_name):
    """
    删除指定列中重复的行，仅保留第一条，并覆盖源文件。

    参数：
    - input_file: str，输入文件路径
    - column_name: str，要检查重复的列名
    """
    try:
        # 读取 Excel 文件
        df = pd.read_excel(input_file)
        # 检查列名是否存在
        if column_name not in df.columns:
            raise ValueError(f"列 '{column_name}' 不存在于输入文件中！")
        # 删除指定列的重复项，仅保留第一条
        df_deduplicated = df.drop_duplicates(subset=[column_name], keep='first')
        df_deduplicated.to_excel(input_file, index=False)
    except Exception as e:
        print(f"处理文件时发生错误：{e}")


def delete_rows_based_on_conditions(filepath):
    wb = openpyxl.load_workbook(filepath)
    sheet = wb.active  # 默认使用活动工作表

    data = pd.read_excel(filepath)
    # 获取 'Shipping service/物流渠道' 和 'Recipient/收件人' 列的索引
    shipping_service_col = data.columns.get_loc('Shipping service/物流渠道') + 1  # openpyxl索引从1开始
    recipient_col = data.columns.get_loc('Recipient/收件人') + 1  # openpyxl索引从1开始

    # 记录要删除的行
    rows_to_delete = []

    # 遍历所有行（从第二行开始，跳过表头）
    for row in range(2, sheet.max_row + 1):
        shipping_service_value = sheet.cell(row=row, column=shipping_service_col).value
        recipient_value = sheet.cell(row=row, column=recipient_col).value

        # 如果满足删除条件，则标记该行
        if shipping_service_value == '上传物流面单(Upload_Shipping_Label)' and recipient_value != 'KJ':
            rows_to_delete.append(row)

    # 删除标记的行（从最后一行开始删除，避免索引错误）
    for row in reversed(rows_to_delete):
        sheet.delete_rows(row)

    # 保存更新后的文件
    wb.save(filepath)
    print(f"文件已更新：{filepath}")


def delete_rows_not_tracking(filepath):
    wb = openpyxl.load_workbook(filepath)
    sheet = wb.active  # 默认使用活动工作表

    data = pd.read_excel(filepath)
    # 获取 'Courier/快递' 列的索引
    courier_col = data.columns.get_loc('Courier/快递') + 1  # openpyxl索引从1开始

    # 记录要删除的行
    rows_to_delete = []

    # 遍历所有行（从第二行开始，跳过表头）
    for row in range(2, sheet.max_row + 1):
        courier_value = sheet.cell(row=row, column=courier_col).value

        # 如果 'Courier/快递' 列的内容不为 'tracking'，则标记删除
        if courier_value != 'tracking':
            rows_to_delete.append(row)

    # 删除标记的行（从最后一行开始删除，避免索引错误）
    for row in reversed(rows_to_delete):
        sheet.delete_rows(row)

    # 保存更新后的文件
    wb.save(filepath)
    print(f"文件已更新：{filepath}")


xlsx_path = input("请输入文件的绝对路径：")
remove_duplicates_by_column(xlsx_path, 'Tracking No./物流跟踪号')
delete_rows_based_on_conditions(xlsx_path)
check_and_add_courier_column(xlsx_path)
results = extract_and_process_data(xlsx_path, RowName.Courier, 100)

update_courier_status_for_results(xlsx_path, results[CourierStateMapKey.not_yet_results])
update_courier_status_for_results(xlsx_path, results[CourierStateMapKey.pre_ship_results])
update_courier_status_for_results(xlsx_path, results[CourierStateMapKey.unpaid_results])
update_courier_status_for_results(xlsx_path, results[CourierStateMapKey.delivered_results])
update_courier_status_for_results(xlsx_path, results[CourierStateMapKey.no_tracking_results])
update_courier_status_for_results(xlsx_path, results[CourierStateMapKey.tracking_results])

delete_rows_not_tracking(xlsx_path)

# no_tracking_count = len(results[CourierStateMapKey.not_yet_results]) + len(
#     results[CourierStateMapKey.pre_ship_results]) + len(results[CourierStateMapKey.no_tracking_results])
# tracking_count = len(results[CourierStateMapKey.unpaid_results]) + len(
#     results[CourierStateMapKey.delivered_results]) + len(results[CourierStateMapKey.tracking_results])
# print(f"没有轨迹数： {no_tracking_count} 条，有轨迹数： {tracking_count} 条")
# print(f"\nunpaid数： {len(results[CourierStateMapKey.unpaid_results])} 条")
# print(f"\nnot_yet数： {len(results[CourierStateMapKey.not_yet_results])} 条")
# print(f"\npre_ship数： {len(results[CourierStateMapKey.pre_ship_results])} 条")
# print(f"\ndelivered数： {len(results[CourierStateMapKey.delivered_results])} 条")
