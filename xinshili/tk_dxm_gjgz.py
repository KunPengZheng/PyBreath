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
    find_irregular_tracking_numbers, update_courier_status1, get_days_difference
from xinshili.pd_utils import remove_duplicates_by_column
from xinshili.utils import natural_key, delete_file
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


def get_target_files(date_str, folder_a, folder_b):
    target_date = datetime.strptime(date_str, "%Y/%m/%d")
    # 仅 target_date 起算往后 3 天（含当天）：D, D+1, D+2
    date_list = [(target_date + timedelta(days=i)).date() for i in range(0, 3)]

    # 按月汇总：month_folder -> 该月需要匹配的“日”（两位补零）
    month_days = {}
    for d in date_list:
        key = f"{d.year}.{d.month}"
        month_days.setdefault(key, set()).add(str(d.day))

    # 文件名模板：^(创建时间|打单时间)<day>_....xlsx
    # 注意：每个“月目录”只用它自己的 days 来拼接正则，避免跨月误匹配
    result_files = []

    for base in (folder_a, folder_b):
        for month_folder, days in month_days.items():
            folder_path = os.path.join(base, month_folder)
            if not os.path.isdir(folder_path):
                continue

            # 例如 (?:30|01|02)
            day_alt = "|".join(sorted(days, key=int))  # 排序按数字，不然 '10' 会排在 '2' 前
            pattern = re.compile(rf"^(创建时间|打单时间)(?:{day_alt})_.*\.xlsx$")

            for fname in os.listdir(folder_path):
                if pattern.match(fname):
                    result_files.append(os.path.join(folder_path, fname))

    return date_list, result_files


def update_from_A_to_B(A_path, B_path):
    # 读取
    A_df = pd.read_excel(A_path, dtype=str).fillna("")
    A_df.columns = A_df.columns.str.strip()

    B_df = pd.read_excel(B_path, dtype=str).fillna("")
    B_df.columns = B_df.columns.str.strip()

    # 判断匹配列
    if "打单时间" in os.path.basename(A_path):
        merge_key_A = "快递单号"
        merge_key_B = "运单号"
    elif "创建时间" in os.path.basename(A_path):
        merge_key_A = "Tracking No./物流跟踪号"
        merge_key_B = "运单号"
    else:
        print(f"⚠️ A 文件名不包含 '打单时间' 或 '创建时间'，跳过：{A_path}")
        return

    # 需要复制的列
    col_map = {
        "Courier/快递": "Courier/快递",
        "PossessionSfDate/揽收时间": "PossessionSfDate/揽收时间",
        "LatestEventSfDate/最新事件时间": "LatestEventSfDate/最新事件时间",
        "LatestEventSfSite/最新事件地点": "LatestEventSfSite/最新事件地点",
    }

    # 检查必要列
    if merge_key_A not in A_df.columns:
        print(f"❌ 源文件缺少匹配列 '{merge_key_A}'，文件：{A_path}")
        return
    if merge_key_B not in B_df.columns:
        print(f"❌ 目标文件缺少匹配列 '{merge_key_B}'，文件：{B_path}")
        return
    for col in col_map.keys():
        if col not in A_df.columns:
            print(f"❌ 源文件缺少列 '{col}'，文件：{A_path}")
            return

    # 合并
    merged_df = B_df.merge(
        A_df[[merge_key_A] + list(col_map.keys())],
        how="left",
        left_on=merge_key_B,
        right_on=merge_key_A,
        suffixes=("", "_src")
    )

    # 覆盖目标列
    for src_col, tgt_col in col_map.items():
        src_col_merged = f"{src_col}_src"
        if src_col_merged in merged_df.columns:
            merged_df[tgt_col] = merged_df[src_col_merged].where(
                merged_df[src_col_merged].notna(),
                merged_df[tgt_col]
            )

    # 删除多余列
    merged_df = merged_df[B_df.columns]

    # 保存
    merged_df.to_excel(B_path, index=False)
    # print(f"✅ 已更新 {B_path}  ←  来源 {A_path}")


def copy_track_state(ck_time, xlsx_path):
    folder_xyl = "/Users/zkp/Desktop/B&Y/轨迹统计/xyl"
    folder_flld = "/Users/zkp/Desktop/B&Y/轨迹统计/flld"  # 这里换成实际路径
    dates, files = get_target_files(ck_time, folder_xyl, folder_flld)
    for f in files:
        update_from_A_to_B(f, xlsx_path)


def go(xlsx_path):
    output_file = os.path.splitext(xlsx_path)[0] + "_去重0.xlsx"
    all_total_count = remove_duplicates_by_column(xlsx_path, output_file, RowName.Track_Num)  # 无筛选订单总数
    delete_file(output_file)

    check_and_add_courier_column(xlsx_path)
    process_tracking_no(xlsx_path, RowName.Track_Num)

    irregular_number_map = find_irregular_tracking_numbers(xlsx_path, RowName.Track_Num)
    if irregular_number_map:
        update_courier_status1(xlsx_path, irregular_number_map, RowName.Track_Num)

    ck_time = get_days_difference(xlsx_path, "发货时间")
    copy_track_state(ck_time, xlsx_path)

    # usps_track(xlsx_path, RowName.Courier, RowName.Track_Num)

    process_tracking_time1(xlsx_path)


def auto(root_dir):
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
                    go(xlsx_path)
                    # if exceed <= 7:
                    #     print(f"正在处理文件: {xlsx_path}")
                    #     go(xlsx_path)


if __name__ == '__main__':
    auto("/Users/zkp/Desktop/B&Y/轨迹统计/tkkj")
