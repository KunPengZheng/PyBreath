import re
from datetime import datetime, timezone, timedelta

import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from xinshili.fs_utils_plus import get_token, dimension_range, FsConstants, value_range, ClientMapConstants, \
    ClientConstants
from xinshili.gjgz_plus333 import check_and_add_courier_column, extract_and_process_data, RowName, CourierStateMapKey, \
    update_courier_status, is_time_difference_exceed, process_tracking_no, CourierStateMapValue
from xinshili.utils import natural_key


def convert_china_to_utc(china_time: datetime) -> datetime:
    """
    将中国时间转换为零时区（UTC/Zulu Time），忽略夏令时
    :param china_time: 中国时间 datetime 对象（无 tzinfo 或本地时间）
    :return: UTC 时间 datetime（无 tzinfo）
    """
    if not isinstance(china_time, datetime):
        raise ValueError("china_time 必须是 datetime 类型")

    china_tz = timezone(timedelta(hours=8))  # 中国时区 UTC+8
    utc_tz = timezone.utc  # UTC 零时区

    # 设置中国时区 → 转为 UTC → 去除 tzinfo
    return china_time.replace(tzinfo=china_tz).astimezone(utc_tz).replace(tzinfo=None)


def process_tracking_time1(file_path):
    df = pd.read_excel(file_path)

    # 先排除状态为 unpaid、delivered、irregular_no_tracking 的行
    df_filtered = df[~df[RowName.Courier].str.lower().isin([CourierStateMapValue.unpaid,
                                                            CourierStateMapValue.delivered,
                                                            CourierStateMapValue.irregular_no_tracking])].copy()

    intervals = []
    states = []
    track_times = []

    # 当前中国时间转换为零时区时间，因为usps接口返回的时间是领时区的
    us_now = convert_china_to_utc(datetime.now())

    for idx, row in df_filtered.iterrows():
        try:
            outbound_time_str = str(row.get("发货时间", "")).strip()

            base_us_time = None
            if outbound_time_str and outbound_time_str.lower() != "nan":
                try:
                    creation_china_time = datetime.strptime(outbound_time_str, "%Y-%m-%d %H:%M:%S")
                    base_us_time = convert_china_to_utc(creation_china_time)
                except Exception:
                    base_us_time = None

            # if base_us_time:
            #     base_diff = us_now - base_us_time
            #     base_hours = round(base_diff.total_seconds() / 3600, 2)
            #
            #     if base_hours > 72:  # 如果 当前时间 - 发货时间 > 72 小时，默认不能再替换运单号。但是结果结果不一定卡死再72小时，而且不包含周末和节假日
            #         intervals.append(base_hours)
            #         states.append("无法替换")
            #         track_times.append(us_now)
            #         continue  # 跳过后续判断

            # 最新事件时间
            date_str = str(row.get(RowName.LatestEventSfDate, "")).strip()
            time_str = str(row.get(RowName.LatestEventSfTime, "")).strip()
            last_time_str = str(row.get(RowName.LastEventSfTime, "")).strip()

            date_flag = date_str and date_str.lower() != "nan"
            time_flag = time_str and time_str.lower() != "nan"
            last_flag = last_time_str and last_time_str.lower() != "nan"
            outbound_time_flag = outbound_time_str and outbound_time_str.lower() != "nan"

            latest_date_time_str = ""
            diff = None

            if date_flag:  # 存在最新事件日期
                if time_flag:  # 存在最新事件时间
                    latest_date_time_str = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                else:  # 不存在最新事件时间
                    latest_date_time_str = datetime.strptime(f"{date_str}", "%Y-%m-%d")
                # if last_flag:  # 存在上一条事件时间
                #     diff = latest_date_time_str - datetime.strptime(f"{last_time_str}", "%Y-%m-%d %H:%M")
                # else:  # 不存在上一条事件时间
                diff = us_now - latest_date_time_str
            else:
                if outbound_time_flag:
                    creation_time = datetime.strptime(outbound_time_str, "%Y-%m-%d %H:%M:%S")
                    diff = us_now - convert_china_to_utc(creation_time)
                else:
                    diff = None

            if diff is not None:
                hours = round(diff.total_seconds() / 3600, 2)

                total_seconds = int(diff.total_seconds())
                hours_part = total_seconds // 3600
                minutes_part = (total_seconds % 3600) // 60
                interval_str = f"{hours_part:02}:{minutes_part:02}"
                intervals.append(interval_str)

                if hours >= 72:
                    states.append("无法替换")
                elif hours >= 48:
                    states.append("阳单替换")
                elif hours >= 24:
                    states.append("预备阳单")
                else:
                    states.append("轨迹正常")
            else:
                intervals.append(None)
                states.append("")

            track_times.append(us_now)

        except Exception as e:
            print(f"⚠️ 第 {idx} 行处理失败: {e}")
            intervals.append(None)
            states.append("")
            track_times.append(us_now)

    # 写入结果列
    df_filtered[RowName.TrackTimeInterval] = intervals
    df_filtered[RowName.TrackTimeIntervalState] = states
    df_filtered[RowName.Tacking_Time] = [t.strftime("%Y-%m-%d %H:%M:%S") if isinstance(t, datetime) else "" for t in
                                         track_times]

    # 用处理后数据更新原始表
    df.update(df_filtered)
    df.to_excel(file_path, index=False)
    print(f"✅ 已处理并保存至：{file_path}")


def create_fs_xlsx_file(file_path):
    # 定义表头
    columns = [
        RowName.Pay_Time, RowName.Ship_Time, RowName.Order_Num, RowName.Track_Num,
        RowName.Track_State, RowName.Analyse_State,
        # RowName.Last_Track_Time,
        RowName.Latest_Track_Site, RowName.Latest_Track_Time, RowName.Interval_Time, RowName.Process_Time,
        RowName.YD_Number2, RowName.YD_State2
    ]

    # 创建空的 DataFrame 并写入文件（覆盖或新建）
    df = pd.DataFrame(columns=columns)
    df.to_excel(file_path, index=False)
    print(f"✅ 文件已{'创建' if not os.path.exists(file_path) else '清空并重建'}：{file_path}")


def export_yd_data(source_file, target_file):
    # 读取源文件
    df = pd.read_excel(source_file)

    def safe_concat_time(row):
        date_part = str(row.get(RowName.LatestEventSfDate, "")).strip()
        time_part = str(row.get(RowName.LatestEventSfTime, "")).strip()
        if date_part.lower() not in ["", "nan"]:
            if time_part.lower() not in ["", "nan"]:
                return f"{date_part} {time_part}"
            else:
                return date_part
        else:
            return ""

    df[RowName.Latest_Track_Time] = df.apply(safe_concat_time, axis=1)

    # 构造目标列的数据（强制转换为字符串以防止科学计数法）
    export_df = pd.DataFrame({
        RowName.Pay_Time: df[RowName.Pay_Time],
        RowName.Ship_Time: df[RowName.Ship_Time],
        RowName.Order_Num: df[RowName.Order_Num].astype(str),
        RowName.Track_Num: df[RowName.Track_Num].astype(str),
        RowName.Track_State: df[RowName.Courier],
        RowName.Analyse_State: df[RowName.Tacking_Time],
        # RowName.Last_Track_Time: df[RowName.LastEventSfTime],
        RowName.Latest_Track_Site: df[RowName.LatestEventSfSite],
        RowName.Latest_Track_Time: df[RowName.Latest_Track_Time],
        RowName.Interval_Time: df[RowName.TrackTimeInterval],
        RowName.Process_Time: df[RowName.TrackTimeIntervalState],
        RowName.YD_Number2: df[RowName.YD_Number],
        RowName.YD_State2: df[RowName.YD_State],
    })

    # 文件已存在 → 打开并追加
    wb = load_workbook(target_file)
    ws = wb.active
    start_row = ws.max_row + 1

    for i, row in enumerate(dataframe_to_rows(export_df, index=False, header=False)):
        for j, value in enumerate(row, 1):
            cell = ws.cell(row=start_row + i, column=j, value=value)

            # 设置为文本格式以防止科学计数法
            header = ws.cell(row=1, column=j).value
            if header in [RowName.Order_Num, RowName.Track_Num]:
                cell.number_format = "@"
                cell.value = str(value)  # 强制转为字符串

    wb.save(target_file)
    print(f"✅ 已追加导出 YD 数据至：{target_file}")
    return len(export_df)


def get_xlsx_data_len(file_path):
    # 读取 Excel 文件，保留空值为 ""，禁用自动类型转换
    df = pd.read_excel(file_path, dtype=object).fillna("")
    # 获取列名作为第一行
    header = list(df.columns)
    # 获取数据行
    data_rows = df.values.tolist()
    # 将列头插入到数据最前面
    nested_list = [header] + data_rows
    return nested_list


def extract_order_ids_as_str(file_path: str, column_name=RowName.Order_Num) -> list[str]:
    """
    读取 Excel 中的“订单号”列，确保其以字符串形式提取出来。
    """
    df = pd.read_excel(file_path, dtype={column_name: str})
    return df[column_name].fillna("").astype(str).tolist()


def force_write_order_ids_to_excel(file_path: str, order_ids: list[str], column_name=RowName.Order_Num):
    """
    强制将订单号列写成字符串格式，避免 Excel 自动转为科学计数法。
    """
    wb = load_workbook(file_path)
    ws = wb.active

    # 找出列索引
    header = [cell.value for cell in ws[1]]
    if column_name not in header:
        raise ValueError(f"列名“{column_name}”未在 Excel 表头中找到")

    col_index = header.index(column_name) + 1
    col_letter = get_column_letter(col_index)

    for i, value in enumerate(order_ids, start=2):  # 从第2行开始写入
        cell = ws[f"{col_letter}{i}"]
        cell.value = str(value)
        cell.number_format = '@'  # '@' 表示文本格式

    wb.save(file_path)


def usps_track(xlsx_path, column_name, wl_name):
    results = extract_and_process_data(xlsx_path, column_name, 100, wl_name=wl_name, dxm_xyl_yd_flag=True)
    all_maps = {}
    column_mapping = {}
    if wl_name == RowName.Track_Num:
        all_maps = {
            CourierStateMapKey.not_yet_map: results[CourierStateMapKey.not_yet_map],
            CourierStateMapKey.pre_ship_map: results[CourierStateMapKey.pre_ship_map],
            CourierStateMapKey.unpaid_map: results[CourierStateMapKey.unpaid_map],
            CourierStateMapKey.delivered_map: results[CourierStateMapKey.delivered_map],
            CourierStateMapKey.no_tracking_map: results[CourierStateMapKey.no_tracking_map],
            CourierStateMapKey.tracking_map: results[CourierStateMapKey.tracking_map],
            CourierStateMapKey.possession_sf_date_map: results[CourierStateMapKey.possession_sf_date_map],
            CourierStateMapKey.latest_event_sf_date_map: results[CourierStateMapKey.latest_event_sf_date_map],
            CourierStateMapKey.sf_date_equality_map: results[CourierStateMapKey.sf_date_equality_map],
            CourierStateMapKey.latest_event_sf_time_map: results[CourierStateMapKey.latest_event_sf_time_map],
            CourierStateMapKey.latest_event_sf_site_map: results[CourierStateMapKey.latest_event_sf_site_map],
            CourierStateMapKey.alert_map: results[CourierStateMapKey.alert_map],
        }
        column_mapping = {
            CourierStateMapKey.not_yet_map: RowName.Courier,
            CourierStateMapKey.pre_ship_map: RowName.Courier,
            CourierStateMapKey.unpaid_map: RowName.Courier,
            CourierStateMapKey.delivered_map: RowName.Courier,
            CourierStateMapKey.no_tracking_map: RowName.Courier,
            CourierStateMapKey.tracking_map: RowName.Courier,
            CourierStateMapKey.possession_sf_date_map: RowName.PossessionSfDate,
            CourierStateMapKey.latest_event_sf_date_map: RowName.LatestEventSfDate,
            CourierStateMapKey.sf_date_equality_map: RowName.SfDateInterval,
            CourierStateMapKey.latest_event_sf_time_map: RowName.LatestEventSfTime,
            CourierStateMapKey.latest_event_sf_site_map: RowName.LatestEventSfSite,
            CourierStateMapKey.alert_map: RowName.Courier,
        }
    else:
        all_maps = {
            CourierStateMapKey.not_yet_map: results[CourierStateMapKey.not_yet_map],
            CourierStateMapKey.pre_ship_map: results[CourierStateMapKey.pre_ship_map],
            CourierStateMapKey.unpaid_map: results[CourierStateMapKey.unpaid_map],
            CourierStateMapKey.delivered_map: results[CourierStateMapKey.delivered_map],
            CourierStateMapKey.no_tracking_map: results[CourierStateMapKey.no_tracking_map],
            CourierStateMapKey.tracking_map: results[CourierStateMapKey.tracking_map],
            # CourierStateMapKey.possession_sf_date_map: results[CourierStateMapKey.possession_sf_date_map],
            # CourierStateMapKey.latest_event_sf_date_map: results[CourierStateMapKey.latest_event_sf_date_map],
            # CourierStateMapKey.sf_date_equality_map: results[CourierStateMapKey.sf_date_equality_map],
            # CourierStateMapKey.latest_event_sf_time_map: results[CourierStateMapKey.latest_event_sf_time_map],
            # CourierStateMapKey.latest_event_sf_site_map: results[CourierStateMapKey.latest_event_sf_site_map],
            CourierStateMapKey.alert_map: results[CourierStateMapKey.alert_map],
        }
        column_mapping = {
            CourierStateMapKey.not_yet_map: RowName.YD_State,
            CourierStateMapKey.pre_ship_map: RowName.YD_State,
            CourierStateMapKey.unpaid_map: RowName.YD_State,
            CourierStateMapKey.delivered_map: RowName.YD_State,
            CourierStateMapKey.no_tracking_map: RowName.YD_State,
            CourierStateMapKey.tracking_map: RowName.YD_State,
            # CourierStateMapKey.possession_sf_date_map: RowName.PossessionSfDate,
            # CourierStateMapKey.latest_event_sf_date_map: RowName.LatestEventSfDate,
            # CourierStateMapKey.sf_date_equality_map: RowName.SfDateInterval,
            # CourierStateMapKey.latest_event_sf_time_map: RowName.LatestEventSfTime,
            # CourierStateMapKey.latest_event_sf_site_map: RowName.LatestEventSfSite,
            CourierStateMapKey.alert_map: RowName.YD_State,
        }

    update_courier_status(xlsx_path, all_maps, wl=wl_name, column_map=column_mapping)


def go(xlsx_path, dxm_xyl_track_merger):
    # order_ids = extract_order_ids_as_str(xlsx_path)
    #
    # check_and_add_courier_column(xlsx_path)
    #
    # process_tracking_no(xlsx_path, RowName.Track_Num)
    # process_tracking_no(xlsx_path, RowName.YD_Number)
    #
    # usps_track(xlsx_path, RowName.Courier, RowName.Track_Num)
    # usps_track(xlsx_path, RowName.YD_State, RowName.YD_Number)

    process_tracking_time1(xlsx_path)
    # force_write_order_ids_to_excel(xlsx_path, order_ids)
    # export_yd_data(xlsx_path, dxm_xyl_track_merger)


def auto(root_dir):
    dxm_xyl_track_merger = "/Users/zkp/Desktop/B&Y/轨迹统计/dxm_xyl_track/dxm_xyl_track_merger.xlsx"
    create_fs_xlsx_file(dxm_xyl_track_merger)

    today = datetime.now()
    current_year = today.year
    current_month = today.month
    current_day = today.day
    current_time = f"{current_year}-{current_month}-{current_day}"

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames.sort(key=natural_key)
        for dirname in dirnames:
            sun_dir_path = os.path.join(dirpath, dirname)
            parts = dirname.split(".")
            year, month = parts[0], parts[1]
            files = [f for f in os.listdir(sun_dir_path) if f.lower().endswith(('.xlsx', '.xls'))]
            files.sort(key=natural_key)
            for file in files:
                xlsx_path = os.path.join(sun_dir_path, file)
                match = re.search(r"发货时间(\d+)_", file)
                if match:
                    day = match.group(1)
                    current_times = f"{year}-{month}-{day}"
                    exceed = is_time_difference_exceed(current_time, current_times)
                    if exceed <= 7:
                        print(f"正在处理文件: {xlsx_path}")
                        go(xlsx_path, dxm_xyl_track_merger)

    # result = get_xlsx_data_len(dxm_xyl_track_merger)
    # token = get_token()
    # # dimension_range(token, FsConstants.gjgz_token,  ClientMapConstants[ClientConstants.dxm_xyl_yd], 1, 12, majorDimension=FsConstants.COLUMNS)
    # value_range(token, FsConstants.gjgz_token, ClientMapConstants[ClientConstants.dxm_xyl_yd], f"A1:L{len(result)}",
    #             result)


def update_yd_number(source_file, folder_path):
    # 读取源文件（文件1）
    df_source = pd.read_excel(source_file, dtype=str)
    df_source.fillna('', inplace=True)

    if "订单编号" not in df_source.columns or "平台回传单号" not in df_source.columns:
        print("❌ 文件1中缺少必要列：订单编号 或 平台回传单号")
        return

    # ✅ 仅保留“订单编号”和“平台回传单号”都不为空的有效记录
    df_valid = df_source[
        (df_source["订单编号"].str.strip() != "") &
        (df_source["平台回传单号"].str.strip() != "")
        ]

    print(f"📋 阳单源文件中有效记录数：{len(df_valid)} 条")

    # 构建映射：订单编号 → 平台回传单号
    mapping = dict(zip(df_valid["订单编号"].str.strip(), df_valid["平台回传单号"].str.strip()))

    # 遍历文件夹中的所有 xlsx 文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_path, filename)
            try:
                df = pd.read_excel(file_path, dtype=str)
                df.fillna('', inplace=True)

                if "订单号" in df.columns:
                    if "YD_Number/阳单号" not in df.columns:
                        df["YD_Number/阳单号"] = ""

                    match_count = 0
                    for i, order_id in df["订单号"].items():
                        order_id = str(order_id).strip()
                        if order_id in mapping:
                            yd_number = mapping[order_id]
                            df.at[i, "YD_Number/阳单号"] = yd_number
                            print(f"✅ 匹配成功：文件：{file_path}，订单编号：{order_id}，平台回传单号：{yd_number}")
                            match_count += 1

                    if match_count > 0:
                        df.to_excel(file_path, index=False)
                        print(f"📊 文件 {filename} 共匹配成功 {match_count} 条记录")
                else:
                    print(f"⚠️ 文件 {file_path} 缺少“订单号”列，跳过")

            except Exception as e:
                print(f"❌ 文件 {file_path} 处理失败: {e}")


if __name__ == '__main__':
    select = "请选择功能："
    select += "\n1：☀️写入阳单号"
    select += "\n2：📊轨迹分析️"
    select += "\n"
    select_input = input(select)
    if select_input == "1":
        sun_path = input("请输入阳单号文件的路径:")
        update_yd_number(sun_path, "/Users/zkp/Desktop/B&Y/轨迹统计/dxm_xyl_track/2025.6")
    elif select_input == "2":
        auto("/Users/zkp/Desktop/B&Y/轨迹统计/dxm_xyl_track")
    else:
        print("🈚️此项功能！")
