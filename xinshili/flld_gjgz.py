import os
import re
from datetime import datetime, timedelta

import pandas as pd
from openpyxl import load_workbook

from xinshili.fs_utils_plus import get_token, brief_sheet_value, ClientConstants, brief_sheet_bg
from xinshili.gjgz_plus333 import RowName, check_and_add_courier_column, extract_and_process_data_flld, \
    update_courier_status_flld, count_pattern_state, CourierStateMapKey, Pattern
from xinshili.utils import convert_csv_to_xlsx, delete_file, getYmd, round2, is_us_weekend, natural_key


def extract_path_before_csv(file_path):
    # 判断文件路径是否以 .csv 结尾
    if file_path.endswith('.csv'):
        # 提取 .csv 前的所有字符
        base_path = file_path.rsplit('.csv', 1)[0]
        xlsx_ = base_path + ".xlsx"
        convert_csv_to_xlsx(file_path, xlsx_)
        delete_file(file_path)
        return xlsx_
    else:
        return file_path


def str_strip(filepath: str, column_name: str):
    data = pd.read_excel(filepath)
    data[column_name] = data[column_name].str.replace('\t', '', regex=False).str.strip()
    data.to_excel(filepath, index=False)


def get_unpaid_tracking_data(file_path, courier_column='Courier/快递', waybill_column='单号',
                             tracking_column='快递单号', key_value='unpaid'):
    # 读取Excel文件
    data = pd.read_excel(file_path)

    # 确保必要的列存在
    if courier_column not in data.columns or waybill_column not in data.columns or tracking_column not in data.columns:
        raise ValueError(f"文件中缺少必要的列，请检查列名是否正确")

    # 筛选出 Courier/快递 列内容为 'unpaid' 的数据
    unpaid_data = data[data[courier_column].str.strip().str.lower() == key_value]

    # 使用 map 存储结果，单号列作为 key，快递单号列作为 value
    result_map = dict(zip(unpaid_data[waybill_column], unpaid_data[tracking_column]))

    return result_map


def get_days_difference(file_path, column_name="打单时间"):
    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active
        # 获取表头
        headers = [cell.value for cell in sheet[1]]
        if column_name not in headers:
            raise ValueError(f"列名 '{column_name}' 不存在！")
        # 获取列索引
        column_index = headers.index(column_name) + 1
        # 获取第一条数据
        first_row_value = sheet.cell(row=2, column=column_index).value  # 假设数据从第二行开始
        if not first_row_value:
            raise ValueError(f"'{column_name}' 列的第一条数据为空！")

        # 获取当前年份
        current_year = datetime.now().year

        # 检查日期类型，如果是字符串并且没有年份，补充当前年份
        if isinstance(first_row_value, str):
            # 如果是字符串并且没有年份，补充当前年份
            if len(first_row_value.split('-')) == 2:  # 格式为 'MM-DD' 或 'DD-MM'
                first_row_value = f"{current_year}-{first_row_value}"
            # 尝试解析日期
            outbound_time = datetime.strptime(first_row_value, "%Y-%m-%d %H:%M")
        elif isinstance(first_row_value, datetime):
            # 如果是已经是 datetime 类型，直接处理
            outbound_time = first_row_value
        else:
            raise ValueError(f"无法解析日期: {first_row_value}")

        # 格式化为 "%Y/%m/%d" 格式
        formatted_date = outbound_time.strftime("%Y/%m/%d")
        return formatted_date
    except Exception as e:
        print(f"发生错误: {e}")
        return None


def merge_csv_files_to_excel(csv_files, output_dir):
    """
    合并多个 CSV 文件，只保留第一个文件的列头，并保存为 Excel 文件。
    同时提取“打单时间”首条值的月份格式（如2025.5）和日期（如05-24），打印有效行数。
    """
    if not csv_files:
        print("❌ 输入文件列表为空")
        return

    combined_df = pd.DataFrame()

    for i, file in enumerate(csv_files):
        try:
            df = pd.read_csv(file, dtype=str).fillna("")
            if df.empty:
                print(f"⚠️ 文件为空，已跳过: {file}")
                continue

            if i == 0:
                combined_df = df
            else:
                if df.columns.equals(combined_df.columns):
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                else:
                    print(f"⚠️ 列不匹配，跳过文件: {file}")
        except Exception as e:
            print(f"❌ 读取失败: {file}，原因: {e}")

    if combined_df.empty:
        print("❌ 无有效数据，未生成 Excel 文件")
        return

    # 有效行：去除全空行
    valid_rows = combined_df[combined_df.apply(lambda row: row.astype(str).str.strip().any(), axis=1)]
    valid_count = len(valid_rows)

    # 提取“打单时间”第一条数据并处理
    if "打单时间" in valid_rows.columns:
        first_time_str = valid_rows["打单时间"].dropna().astype(str).str.strip().iloc[0]
        try:
            # 解析格式，如 05-24 14:54
            dt = datetime.strptime(first_time_str, "%m-%d %H:%M")
            # 添加年份，拼接为 “2025.5”
            month_info = f"2025.{dt.month}"
            # 获取日期部分
            date_only = dt.strftime("%d")
            print(f"📅 打单时间首条记录：{first_time_str}")
            print(f"📅 转换后的月份格式：{month_info}")
            print(f"📅 提取的日期：{date_only}")
        except Exception as e:
            print(f"⚠️ 时间格式解析失败: {first_time_str}，错误: {e}")
    else:
        print("⚠️ 未找到“打单时间”列，跳过时间处理")

    print(f"✅ 有效数据行数（不含表头）：{valid_count}")

    # ✅ 创建输出目录（如果不存在）
    output_dir_month = output_dir + month_info + "/"
    create_dir = os.path.dirname(output_dir + month_info + "/")
    os.makedirs(create_dir, exist_ok=True)

    output_path = output_dir_month + f"打单时间{date_only}_{valid_count}.xlsx"

    combined_df.to_excel(output_path, index=False)
    print(f"✅ 合并完成，保存至: {output_path}")


def xsxs(output_file):
    patterns = {
        "no_track": Pattern.no_track,
        "delivered": Pattern.delivered,
        "unpaid": Pattern.unpaid,
        "not_yet": Pattern.not_yet,
        "pre_ship": Pattern.pre_ship,
        "irregular_no_tracking": Pattern.irregular_no_tracking,
        "no_tracking": Pattern.no_tracking,
        "tracking": Pattern.tracking
    }

    count_dict = count_pattern_state(output_file, RowName.Courier, patterns)

    no_track_count = count_dict["no_track"]
    delivered_count = count_dict["delivered"]
    unpaid_count = count_dict["unpaid"]
    not_yet_count = count_dict["not_yet"]
    pre_ship_count = count_dict["pre_ship"]
    irregular_no_tracking_count = count_dict["irregular_no_tracking"]
    no_tracking_count = count_dict["no_tracking"]
    tracking_count = count_dict["tracking"]

    delivered_count_int = int(delivered_count)
    unpaid_count_int = int(unpaid_count)
    not_yet_count_int = int(not_yet_count)
    pre_ship_count_int = int(pre_ship_count)
    irregular_no_tracking_count_int = int(irregular_no_tracking_count)
    no_tracking_count_int = int(no_tracking_count)
    tracking_count_int = int(tracking_count)
    no_track_count_int = int(no_track_count)
    total_count_int = no_track_count_int + delivered_count + unpaid_count + tracking_count

    # 计算百分比
    swl = round2(100 - ((no_track_count_int) / total_count_int * 100))
    wswl = round2(100 - swl)
    qsl = round2((delivered_count_int / total_count_int) * 100)
    unpaidl = round2((unpaid_count_int / total_count_int) * 100)
    not_yetl = round2((not_yet_count_int / total_count_int) * 100)
    pre_shipl = round2((pre_ship_count_int / total_count_int) * 100)
    irregular_no_trackingl = round2((irregular_no_tracking_count_int / total_count_int) * 100)
    no_tracking_countl = round2((no_tracking_count_int / total_count_int) * 100)
    tracking_countl = round2((tracking_count_int / total_count_int) * 100)


def go(input_path):
    if input_path is None:
        input_path = input("请输入文件的绝对路径：")
    xlsx_path = extract_path_before_csv(input_path)
    str_strip(xlsx_path, "快递单号")
    check_and_add_courier_column(xlsx_path)
    results = extract_and_process_data_flld(xlsx_path, RowName.Courier, 100, "快递单号")

    update_courier_status_flld(xlsx_path, results[CourierStateMapKey.not_yet_map], "快递单号")
    update_courier_status_flld(xlsx_path, results[CourierStateMapKey.pre_ship_map], "快递单号")
    update_courier_status_flld(xlsx_path, results[CourierStateMapKey.unpaid_map], "快递单号")
    update_courier_status_flld(xlsx_path, results[CourierStateMapKey.delivered_map], "快递单号")
    update_courier_status_flld(xlsx_path, results[CourierStateMapKey.no_tracking_map], "快递单号")
    update_courier_status_flld(xlsx_path, results[CourierStateMapKey.tracking_map], "快递单号")
    update_courier_status_flld(xlsx_path, results[CourierStateMapKey.alert_map], "快递单号")

    total_count, no_track_count = count_pattern_state(xlsx_path, RowName.Courier, Pattern.no_track)
    track_count = total_count - no_track_count
    total_count2, delivered_count = count_pattern_state(xlsx_path, RowName.Courier, Pattern.delivered)
    total_count3, unpaid_count = count_pattern_state(xlsx_path, RowName.Courier, Pattern.unpaid)
    total_count4, not_yet_count = count_pattern_state(xlsx_path, RowName.Courier, r"not_yet")
    total_count5, pre_ship_count = count_pattern_state(xlsx_path, RowName.Courier, r"pre_ship")
    total_count6, alert_count = count_pattern_state(xlsx_path, RowName.Courier, Pattern.alert)

    text = ""
    fs_text = ""
    ck_time = get_days_difference(xlsx_path)
    gz_time = getYmd()
    interval_time = (datetime.strptime(gz_time, "%Y/%m/%d") - datetime.strptime(ck_time, "%Y/%m/%d")).days
    is_usweekend = is_us_weekend(ck_time)
    date_obj = datetime.strptime(ck_time, "%Y/%m/%d").date()
    previous_day = date_obj - timedelta(days=1)
    actual_interval = 0
    if is_usweekend == 6:  # 6是中国周日，美国周六
        actual_interval = interval_time - 2
    elif is_usweekend == 0:  # 0是中国周一，美国周日
        actual_interval = interval_time - 1

    text += f"打单日期：{ck_time}"
    text += f"\n跟踪日期：{gz_time}"

    text += f"\n订单总数：{total_count}"
    fs_text += f"\n订单总数：{total_count}"

    swl = round2(100 - ((int(no_track_count) / int(total_count)) * 100))
    wswl = round2(100 - swl)
    text += f"\n上网：（{track_count}, {swl}%）"
    fs_text += f"\n上网：（{track_count}, {swl}%）"

    text += f"\n未上网：（{no_track_count}, {wswl}%）"
    fs_text += f"\n未上网：（{no_track_count}, {wswl}%）"

    not_yet_countl = round2((int(not_yet_count) / int(total_count)) * 100)
    text += f"\nnot_yet：（{not_yet_count}, {not_yet_countl}%）"
    fs_text += f"\nnot_yet：（{not_yet_count}, {not_yet_countl}%）"

    pre_ship_countl = round2((int(pre_ship_count) / int(total_count)) * 100)
    text += f"\npre_ship：（{pre_ship_count}, {pre_ship_countl}%）"
    fs_text += f"\npre_ship：（{pre_ship_count}, {pre_ship_countl}%）"

    delivered_countl = round2((int(delivered_count) / int(total_count)) * 100)
    text += f"\ndelivered：（{delivered_count}, {delivered_countl}%）"
    fs_text += f"\ndelivered：（{delivered_count}, {delivered_countl}%）"

    unpaid_countl = round2((int(unpaid_count) / int(total_count)) * 100)
    text += f"\nunpaid：（{unpaid_count}, {unpaid_countl}%）"
    fs_text += f"\nunpaid：（{unpaid_count}, {unpaid_countl}%）"

    alert_countl = round2((int(alert_count) / int(total_count)) * 100)
    text += f"\nalert：（{alert_count}, {alert_countl}%）"
    fs_text += f"\nalert：（{alert_count}, {alert_countl}%）"

    unpaid_tracking_data = get_unpaid_tracking_data(xlsx_path)
    if (len(unpaid_tracking_data) > 0):
        text += f"\n-------unpaid详情-------"
        fs_text += f"\n-------unpaid详情-------"
        for key, value in unpaid_tracking_data.items():
            text += f"\n（单号：{key}, 快递单号：{value}）"
            fs_text += f"\n（单号：{key}, 快递单号：{value}）"

    alert_intercepted_tracking_data = get_unpaid_tracking_data(xlsx_path, key_value="alert")
    if (len(alert_intercepted_tracking_data) > 0):
        text += f"\n-------alert详情-------"
        fs_text += f"\n-------alert详情-------"
        for key, value in alert_intercepted_tracking_data.items():
            text += f"\n（单号：{key}, 快递单号：{value}）"
            fs_text += f"\n（单号：{key}, 快递单号：{value}）"

    print(text)

    sum_up_text = ""
    swl_flag = False
    qsl_flag = False
    bg = "#FFFFFF"

    # 上网率判断
    warning_levels = [
        (0, 30, "🧑‍🍳", "继续观察👀", "#FFFFFF"),
        (1, 30, "☁️注意", "未达30%！", "#F8F1D3"),
        (2, 70, "🌧️注意", "未达70%！", "#E3C49C"),
        (3, 97, "❄️异常", "未达97%！", "#F1C1BD"),
    ]

    actual_interval_time = interval_time - actual_interval
    # sum_up_text += f"\n间隔第{interval_time}{actual_interval}天"
    sum_up_text += f"\n间隔第{actual_interval_time}天"

    for days, threshold, icon, message, color in warning_levels:
        if actual_interval_time == days and swl < threshold:
            sum_up_text += f"\n{icon}：上网率为{swl}%，{message}"
            swl_flag = True
            if (actual_interval_time >= 2):
                bg = color
            break
    else:  # ✅ 只有 for 没有 break 时才会执行
        if (actual_interval_time >= 4):
            if (swl >= 99):
                sum_up_text += f"\n☀️上网率为{swl}%，优秀🌈"
            elif (swl >= 97 and swl < 99):
                sum_up_text += f"\n☀️上网率为{swl}%，达标✅"
            else:
                sum_up_text += f"\n⚡️异常：上网率为{swl}%，未达️97%"
                bg = "#F1C1BD"
                swl_flag = True
        else:
            sum_up_text += f"\n☀️上网率为{swl}%，达标✅"

    if (len(alert_intercepted_tracking_data) > 0):
        bg = "#FFF258"

    if (len(unpaid_tracking_data) > 0):
        bg = "#A684F0"

    tat = get_token()
    brief_sheet_value(tat, [fs_text], ck_time, gz_time, ClientConstants.md_flld)
    brief_sheet_bg(tat, ck_time, gz_time, ClientConstants.md_flld, bg)


def automatic(dir_path):
    is_morning = (datetime.now().hour) < 12

    pattern = r"^(出库时间|创建时间|打单时间)\d+_\d+\.xlsx$"

    # 获取所有文件（可选地限制为某种类型，如 .xlsx）
    files = [f for f in os.listdir(dir_path) if f.lower().endswith(('.xlsx', '.xls'))]

    # 按照自然顺序排序
    files.sort(key=natural_key)

    # 遍历排序后的文件
    for file in files:
        if re.match(pattern, file):
            xlsx_path = os.path.join(dir_path, file)

            go(xlsx_path)

            # check_and_add_courier_column(xlsx_path)
            #
            # total_count, no_track_count = count_pattern_state(xlsx_path, RowName.Courier, Pattern.no_track)
            # track_count = total_count - no_track_count
            # total_count2, delivered_count = count_pattern_state(xlsx_path, RowName.Courier, Pattern.delivered)
            # total_count3, unpaid_count = count_pattern_state(xlsx_path, RowName.Courier, Pattern.unpaid)
            # total_count4, not_yet_count = count_pattern_state(xlsx_path, RowName.Courier, r"not_yet")
            # total_count5, pre_ship_count = count_pattern_state(xlsx_path, RowName.Courier, r"pre_ship")
            # total_count6, alert_count = count_pattern_state(xlsx_path, RowName.Courier, Pattern.alert)
            #
            # ck_time = get_days_difference(xlsx_path)
            # gz_time = getYmd()
            # interval_time = (datetime.strptime(gz_time, "%Y/%m/%d") - datetime.strptime(ck_time, "%Y/%m/%d")).days
            #
            # swl = round2(100 - ((int(no_track_count) / int(total_count)) * 100))
            #
            # if (is_morning and interval_time == 1):  # 早上跑昨天的
            #     # go(xlsx_path)
            #     swl = round2(100 - ((int(no_track_count) / int(total_count)) * 100))
            #     print("11111", swl, xlsx_path)
            # else:
            #     if (swl < 99):
            #         # go(xlsx_path)
            #         print("2222", swl, xlsx_path)


def call():
    automatic("/Users/zkp/Desktop/B&Y/轨迹统计/flld/2025.5")


if __name__ == '__main__':

    select = "请选择功能："
    select += "\n1：🍺合并cvs文件为xlsx文件"
    select += "\n2：📊轨迹分析️"
    select += "\n"
    select_input = input(select)

    if select_input == "1":

        file_paths = []

        csv1 = input("请输入csv文件1的路径：").strip()
        csv2 = input("请输入csv文件2的路径：").strip()

        if csv1.endswith(".csv"):
            file_paths.append(csv1)

        if csv2.endswith(".csv"):
            file_paths.append(csv2)

        if len(file_paths):
            output_dir = '/Users/zkp/Desktop/B&Y/轨迹统计/flld/'
            merge_csv_files_to_excel(file_paths, output_dir)

    elif select_input == "2":
        call()
    else:
        print("🈚️此项功能！")
