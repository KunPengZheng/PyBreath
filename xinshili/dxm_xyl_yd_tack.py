import re
from datetime import datetime, timezone, timedelta

import pandas as pd
import os
from zoneinfo import ZoneInfo
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from xinshili.fs_utils_plus import get_token, dimension_range, FsConstants, value_range, ClientMapConstants, \
    ClientConstants
from xinshili.gjgz_plus333 import check_and_add_courier_column, extract_and_process_data, RowName, CourierStateMapKey, \
    update_courier_status, is_time_difference_exceed, process_tracking_no, CourierStateMapValue, \
    find_irregular_tracking_numbers, update_courier_status1
from xinshili.utils import natural_key
from xinshili.yd_to_dxm import clean_order_id


def convert_china_to_utc0(china_time: datetime) -> datetime:
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
    df = pd.read_excel(file_path, dtype=str)

    # 先排除状态为 unpaid、delivered、irregular_no_tracking 的行
    df_filtered = df[~df[RowName.Courier].str.lower().isin([
        # CourierStateMapValue.unpaid,
        # CourierStateMapValue.delivered,
        CourierStateMapValue.irregular_no_tracking])].copy()

    intervals = []
    states = []
    track_times = []

    # 当前中国时间转换为零时区时间，因为usps接口返回的时间是领时区的
    utc0_now = convert_china_to_utc0(datetime.now())

    for idx, row in df_filtered.iterrows():
        try:
            courier = str(row.get(RowName.Courier, "")).strip().lower()
            yd_number = str(row.get(RowName.YD_Number, "")).strip()

            # 优先判断是否已交付或已换阳单
            if courier == CourierStateMapValue.delivered:
                intervals.append("")
                states.append("已经交付")
                track_times.append(utc0_now)
                continue

            # 原来的运单号不能是unpaid，如果是unpaid要接着往下执行，进行补发提示
            if yd_number and yd_number.lower() != "nan" and courier != CourierStateMapValue.unpaid:
                intervals.append("")
                states.append("已换阳单")
                track_times.append(utc0_now)
                continue

            # 如果没有触发上面两个判断，则进入常规时间判断逻辑
            ship_time_str = str(row.get("发货时间", "")).strip()
            date_str = str(row.get(RowName.LatestEventSfDate, "")).strip()
            time_str = str(row.get(RowName.LatestEventSfTime, "")).strip()

            date_flag = date_str and date_str.lower() != "nan"
            time_flag = time_str and time_str.lower() != "nan"
            outbound_time_flag = ship_time_str and ship_time_str.lower() != "nan"

            diff = None
            if date_flag:
                if time_flag:
                    latest_date_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                else:
                    latest_date_time = datetime.strptime(f"{date_str}", "%Y-%m-%d")
                diff = utc0_now - latest_date_time
            elif outbound_time_flag:
                creation_time = datetime.strptime(ship_time_str, "%Y-%m-%d %H:%M:%S")
                diff = utc0_now - convert_china_to_utc0(creation_time)

            if diff is not None:
                hours = round(diff.total_seconds() / 3600, 2)
                total_seconds = int(diff.total_seconds())
                hours_part = total_seconds // 3600
                minutes_part = (total_seconds % 3600) // 60
                interval_str = f"{hours_part:02}:{minutes_part:02}"
                intervals.append(interval_str)

                # 默认无法替换判断时间为 72 小时
                delay_hours = 72

                # ✅ 判断付款时间是否为美国周五、六、日，如果是则延迟 48 小时
                pay_time_str = str(row.get("付款时间", "")).strip()
                if pay_time_str and pay_time_str.lower() != "nan":
                    try:
                        pay_time_china = datetime.strptime(pay_time_str, "%Y-%m-%d %H:%M:%S")
                        pay_time_utc0 = convert_china_to_utc0(pay_time_china)
                        # 转为美国东部时间（或你实际使用的 USPS 时区）
                        pay_time_us = pay_time_utc0.replace(tzinfo=timezone.utc).astimezone(
                            ZoneInfo("America/New_York"))
                        if pay_time_us.weekday() in [4, 5, 6]:  # 星期五、六、日
                            delay_hours += 48
                    except Exception as e:
                        print(f"⚠️ 第 {idx} 行付款时间解析失败: {e}")

                # 优先判断是否unpaid
                if courier == CourierStateMapValue.unpaid:
                    if hours <= 192:  # <=8天
                        states.append("邮资未付<=8天")
                    else:
                        states.append("邮资未付>8天")
                    track_times.append(utc0_now)
                    continue

                if hours >= delay_hours:
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

            track_times.append(utc0_now)

        except Exception as e:
            print(f"⚠️ 第 {idx} 行处理失败: {e}")
            intervals.append(None)
            states.append("")
            track_times.append(utc0_now)

    df_filtered[RowName.TrackTimeInterval] = intervals
    df_filtered[RowName.TrackTimeIntervalState] = states
    df_filtered[RowName.Tacking_Time] = [
        t.strftime("%Y-%m-%d %H:%M:%S") if isinstance(t, datetime) else "" for t in track_times
    ]

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
    df = pd.read_excel(source_file, dtype=str)

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


def go(xlsx_path, dxm_xyl_track_merger, yd_flag=True):
    check_and_add_courier_column(xlsx_path)

    process_tracking_no(xlsx_path, RowName.Track_Num)
    if yd_flag:
        process_tracking_no(xlsx_path, RowName.YD_Number)

    irregular_number_map = find_irregular_tracking_numbers(xlsx_path, RowName.Track_Num)
    if irregular_number_map:
        update_courier_status1(xlsx_path, irregular_number_map, RowName.Track_Num)

    if yd_flag:
        usps_track(xlsx_path, RowName.Courier, RowName.Track_Num)
        usps_track(xlsx_path, RowName.YD_State, RowName.YD_Number)

    process_tracking_time1(xlsx_path)
    if yd_flag:
        export_yd_data(xlsx_path, dxm_xyl_track_merger)


def auto(root_dir, yd_flag=True):
    dxm_xyl_track_merger = "/Users/zkp/Desktop/B&Y/轨迹统计/dxm_xyl_track/dxm_xyl_track_merger.xlsx"
    if yd_flag:
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
                    if yd_flag:
                        track_day = 7
                    else:
                        track_day = 5
                    if exceed <= track_day:
                        print(f"正在处理文件: {xlsx_path}")
                        go(xlsx_path, dxm_xyl_track_merger, False)

    if yd_flag:
        result = get_xlsx_data_len(dxm_xyl_track_merger)
        token = get_token()
        # dimension_range(token, FsConstants.gjgz_token,  ClientMapConstants[ClientConstants.dxm_xyl_yd], 1, 12, majorDimension=FsConstants.COLUMNS)
        value_range(token, FsConstants.gjgz_token, ClientMapConstants[ClientConstants.dxm_xyl_yd], f"A1:L{len(result)}",
                    result)


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
    mapping = dict(zip(df_valid["订单编号"].apply(clean_order_id), df_valid["平台回传单号"].str.strip()))

    # 遍历文件夹中的所有 xlsx 文件
    for dirpath, dirnames, filenames in os.walk(folder_path):
        dirnames.sort(key=natural_key)
        for dirname in dirnames:
            sun_dir_path = os.path.join(dirpath, dirname)
            files = [f for f in os.listdir(sun_dir_path) if f.lower().endswith(('.xlsx', '.xls'))]
            files.sort(key=natural_key)
            for file in files:
                file_path = os.path.join(sun_dir_path, file)
                try:
                    df = pd.read_excel(file_path, dtype=str)
                    df.fillna('', inplace=True)

                    if RowName.Order_Num in df.columns:
                        if RowName.YD_Number not in df.columns:
                            df[RowName.YD_Number] = ""

                        match_count = 0
                        for i, order_id in df[RowName.Order_Num].items():
                            order_id = str(order_id).strip()
                            if order_id in mapping:
                                yd_number = mapping[order_id]
                                df.at[i, RowName.YD_Number] = yd_number
                                print(f"✅ 匹配成功：文件：{file_path}，订单编号：{order_id}，平台回传单号：{yd_number}")
                                match_count += 1

                        if match_count > 0:
                            df.to_excel(file_path, index=False)
                            print(f"📊 文件 {file_path} 共匹配成功 {match_count} 条记录")
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
        update_yd_number(sun_path, "/Users/zkp/Desktop/B&Y/轨迹统计/dxm_xyl_track/")
    elif select_input == "2":
        auto("/Users/zkp/Desktop/B&Y/轨迹统计/dxm_xyl_track")
    else:
        print("🈚️此项功能！")
