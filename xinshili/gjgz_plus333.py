from datetime import datetime, date, timedelta
import os
import re
from openpyxl import load_workbook
import openpyxl
import pandas as pd
from collections import Counter, defaultdict
from dataclasses import dataclass
import concurrent.futures
import time

from xinshili.fs_utils_plus import get_token, brief_sheet_value, detail_sheet_value, ClientConstants, detail_sheet_bg, \
    brief_sheet_bg
from xinshili.pd_utils import remove_duplicates_by_column
from xinshili.usps_utils import track
from xinshili.utils import round2, getYmd, delete_file, is_us_weekend, get_weekday, get_american_holiday, \
    get_chinese_holiday

"""
zbw轨迹跟踪分析
"""


@dataclass(frozen=True)
class RowName:
    Tracking_No = 'Tracking No./物流跟踪号'
    Courier = 'Courier/快递'
    OutboundTime = "OutboundTime/出库时间"
    Warehouse = "Warehouse/仓库"
    Client = "Client/客户"
    CreationWaveTime = "Create wave time/生成波次时间"
    SKU = "SKU"
    ShippingService = "Shipping service/物流渠道"
    PossessionSfDate = "PossessionSfDate/揽收时间"
    LatestEventSfDate = "LatestEventSfDate/最新事件时间"
    SfDateInterval = "SfDateInterval/SF消息间隔"


@dataclass(frozen=True)
class CourierStateMapKey:
    tracking_map = 'tracking_map'
    irregular_number_map = 'irregular_number_map'
    no_tracking_map = 'no_tracking_map'
    unpaid_map = "unpaid_map"
    not_yet_map = "not_yet_map"
    pre_ship_map = "pre_ship_map"
    delivered_map = "delivered_map"
    possession_sf_date_map = "possession_sf_date_map"
    latest_event_sf_date_map = "latest_event_sf_date_map"
    sf_date_equality_map = "sf_date_equality_map"


class CourierStateMapValue:
    irregular_no_tracking = 'irregular_no_tracking'
    not_yet = 'not_yet'
    pre_ship = "pre_ship"
    no_tracking = "no_tracking"
    unpaid = "unpaid"
    delivered = "delivered"
    tracking = "tracking"


@dataclass(frozen=True)
class CellKey:
    Outbound_Time = "Outbound_Time"
    update_time = "update_time"
    order_count = "order_count"
    no_track_number = "no_track_number"
    track_percent = "track_percent"
    delivered_counts = "delivered_counts"
    delivered_percent = "delivered_percent"
    no_track_percent = "no_track_percent"
    warehouse_condition = "warehouse_condition"
    store_condition = "store_condition"
    sku_condition = "sku_condition"
    time_segment_condition = "time_segment_condition"
    sum_up = "sum_up"
    exception = "exception"
    shipping_service_condition = "shipping_service_condition"
    unpaid_count = "unpaid_count"
    special_information = "special_information"
    wl = "wl"


@dataclass(frozen=True)
class Pattern:
    no_track = r"not_yet|pre_ship|irregular_no_tracking|no_tracking"
    delivered = r"delivered"
    unpaid = r"unpaid"
    not_yet = r"not_yet"
    irregular_no_tracking = r"irregular_no_tracking"
    pre_ship = r"pre_ship"
    no_tracking = r"no_tracking"
    tracking = r"tracking"


def find_irregular_tracking_numbers(filepath, column_name=RowName.Tracking_No):
    """
    查找不规则的快递单号（不是纯数字或者不是9开头）
    :param filepath: Excel文件路径
    :return: 不规则快递单号字典
    """
    try:
        # 打开xlsx文件
        wb = openpyxl.load_workbook(filepath)
        sheet = wb.active  # 默认使用活动工作表

        # 获取 'Tracking No./物流跟踪号' 列索引
        tracking_no_col = None
        for col in range(1, sheet.max_column + 1):
            if sheet.cell(row=1, column=col).value == column_name:
                tracking_no_col = col
                break

        if tracking_no_col is None:
            print(f"找不到 {column_name} 列")
            return {}

        # 存储不规则快递单号的字典
        irregular_number_map = {}

        # 遍历所有行，从第二行开始（跳过表头）
        for row in range(2, sheet.max_row + 1):
            tracking_no = str(sheet.cell(row=row, column=tracking_no_col).value)  # 转换为字符串
            # 判断是否是纯数字并且以9开头
            if not tracking_no.isdigit() or not tracking_no.startswith('9'):
                irregular_number_map[tracking_no] = CourierStateMapValue.irregular_no_tracking

        return irregular_number_map

    except Exception as e:
        print(f"发生错误: {e}")
        return {}


def update_courier_status(filepath, maps_list, wl=RowName.Tracking_No, column_map=None):
    """
    批量更新多个状态，避免重复读取和写入文件，提高效率
    :param filepath: Excel 文件路径
    :param maps_list: 一个字典列表，包含多个 {tracking_no: status} 的映射
    :param wl: 物流跟踪号列名
    :param column_map: 需要更新的列 {状态映射: 对应的 Excel 列名}
    """
    # 1. 读取 Excel 文件
    wb = openpyxl.load_workbook(filepath)
    sheet = wb.active

    # 2. 获取列索引
    headers = [cell.value for cell in sheet[1]]
    tracking_no_col = headers.index(wl) + 1  # 物流单号列

    # 3. 获取所有需要更新的列索引
    column_indices = {key: headers.index(col_name) + 1 for key, col_name in column_map.items()}

    # 4. 读取 Excel 中的所有 tracking_no
    tracking_no_rows = {}
    for row in range(2, sheet.max_row + 1):  # 从第2行（跳过表头）开始
        tracking_no = sheet.cell(row=row, column=tracking_no_col).value
        if tracking_no:
            tracking_no_rows[tracking_no] = row

    # 5. 遍历所有需要更新的状态
    for state_map, col_name in column_map.items():
        col_index = column_indices[state_map]
        for tracking_no, status in maps_list.get(state_map, {}).items():
            if tracking_no in tracking_no_rows:  # 仅更新存在的 tracking_no
                row_index = tracking_no_rows[tracking_no]
                sheet.cell(row=row_index, column=col_index, value=status)

    # 6. 一次性保存 Excel
    wb.save(filepath)


# 预编译正则，提高性能
date_regex = re.compile(r"\d{4}-\d{2}-\d{2}")


# 解析日期的辅助函数
def parse_date(date_str):
    match = date_regex.search(str(date_str))
    return match.group() if match else ""


def extract_and_process_data(filepath: str, column_name: str, group_size: int, wl_name=RowName.Tracking_No,
                             request_interval: float = 2.0):
    data = pd.read_excel(filepath)

    if column_name not in data.columns:
        raise ValueError(f"列 '{column_name}' 不存在于 Excel 文件中")

    # 初始化结果 map
    results_map = {
        CourierStateMapKey.tracking_map: {},
        CourierStateMapKey.no_tracking_map: {},
        CourierStateMapKey.unpaid_map: {},
        CourierStateMapKey.not_yet_map: {},
        CourierStateMapKey.pre_ship_map: {},
        CourierStateMapKey.delivered_map: {},
        CourierStateMapKey.possession_sf_date_map: {},
        CourierStateMapKey.latest_event_sf_date_map: {},
        CourierStateMapKey.sf_date_equality_map: {},
    }

    # 填充空值，并使用 `isin()` 进行过滤
    data[column_name] = data[column_name].fillna('')
    valid_values = {"", CourierStateMapValue.not_yet, CourierStateMapValue.pre_ship,
                    CourierStateMapValue.tracking, CourierStateMapValue.no_tracking}
    filtered_data = data[data[column_name].isin(valid_values)]

    # 获取符合条件的物流单号列表
    items = filtered_data[wl_name].tolist()

    # 分批处理
    grouped_items = [items[i:i + group_size] for i in range(0, len(items), group_size)]

    last_request_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 直接存储索引，避免 .index() 操作
        futures = {executor.submit(track, group): (idx, group) for idx, group in enumerate(grouped_items)}

        for future in concurrent.futures.as_completed(futures):
            idx, group = futures[future]

            # 控制请求间隔
            elapsed_time = time.time() - last_request_time
            if elapsed_time < request_interval:
                time.sleep(request_interval - elapsed_time)
            last_request_time = time.time()

            try:
                track1 = future.result()
                print(f"处理第 {idx + 1} 组，共 {len(group)} 条数据")

                for package_id, info in track1['data'].items():
                    if info.get('err'):
                        err_id = info.get('err_id')
                        if err_id == '-2147219283':
                            results_map[CourierStateMapKey.not_yet_map][package_id] = CourierStateMapValue.not_yet
                        elif err_id == 'pre-ship':
                            results_map[CourierStateMapKey.pre_ship_map][package_id] = CourierStateMapValue.pre_ship
                        else:
                            results_map[CourierStateMapKey.no_tracking_map][
                                package_id] = CourierStateMapValue.no_tracking

                        results_map[CourierStateMapKey.possession_sf_date_map][package_id] = ""
                        results_map[CourierStateMapKey.latest_event_sf_date_map][package_id] = ""
                        results_map[CourierStateMapKey.sf_date_equality_map][package_id] = 0
                    else:
                        status_category = info.get('statusCategory')
                        status_long = info.get('statusLong')

                        if "postage" in status_long:
                            results_map[CourierStateMapKey.unpaid_map][package_id] = CourierStateMapValue.unpaid
                        elif "Delivered" in status_category or "Delivered to Agent" in status_category:
                            results_map[CourierStateMapKey.delivered_map][package_id] = CourierStateMapValue.delivered
                        else:
                            results_map[CourierStateMapKey.tracking_map][package_id] = CourierStateMapValue.tracking

                        # 解析日期
                        possession_date = parse_date(info.get("possessionSfDateTime"))
                        latest_event_date = parse_date(info.get("latestEventSfDateTime"))

                        if possession_date and latest_event_date:
                            days_diff = (datetime.strptime(latest_event_date, "%Y-%m-%d") -
                                         datetime.strptime(possession_date, "%Y-%m-%d")).days
                        else:
                            days_diff = 0

                        # 特殊情况
                        if days_diff == 0 and info.get("statusShort") == 'Arrived at USPS Regional Origin Facility':
                            days_diff = 99

                        results_map[CourierStateMapKey.possession_sf_date_map][package_id] = possession_date
                        results_map[CourierStateMapKey.latest_event_sf_date_map][package_id] = latest_event_date
                        results_map[CourierStateMapKey.sf_date_equality_map][package_id] = int(days_diff)

            except Exception as e:
                print(f"处理组 {idx + 1} 时发生错误: {e}")

    return results_map


def count_pattern_state(file_path, column_name, patternStr):
    """
    统计指定列指定内容的数量
    """
    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]
        if column_name not in headers:
            raise ValueError(f"列名 '{column_name}' 不存在！")
        column_index = headers.index(column_name) + 1
        pattern = re.compile(patternStr, re.IGNORECASE)
        total_count = 0
        no_track_count = 0
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            cell_value = row[column_index - 1]
            if cell_value is not None:
                total_count += 1
                if pattern.search(str(cell_value)):
                    no_track_count += 1
        return total_count, no_track_count
    except Exception as e:
        print(f"发生错误: {e}")
        return 0, 0


def count_tracking_with_sf_date_equality(file_path):
    """
    统计 "Courier/快递" 列内容为 'tracking' 且 "SfDateEquality" 列的内容为 0 的行数。

    :param file_path: Excel 文件路径
    :return: 符合条件的行数
    """
    try:
        # 加载 Excel 文件
        workbook = load_workbook(file_path, data_only=True)
        sheet = workbook.active  # 获取活动表

        # 读取表头
        headers = [cell.value for cell in sheet[1]]

        # 确保列名存在
        if RowName.Courier not in headers or RowName.SfDateInterval not in headers:
            raise ValueError(f"Excel 文件中未找到 '{RowName.Courier}' 或 '{RowName.SfDateInterval}' 列")

        # 获取列索引（Excel 列索引从 1 开始，转换为 Python 需要 -1）
        courier_index = headers.index(RowName.Courier)
        sf_date_equality_index = headers.index(RowName.SfDateInterval)

        count = 0  # 统计符合条件的行数

        # 遍历数据行（从第 2 行开始）
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            courier_value = row[courier_index]
            sf_date_equality_value = row[sf_date_equality_index]

            # 判断是否符合筛选条件
            if courier_value == CourierStateMapValue.tracking and sf_date_equality_value == 0:
                count += 1

        return count

    except Exception as e:
        print(f"发生错误: {e}")
        return 0


def count_distribution_and_no_track(file_path, key_column, courier_column=RowName.Courier):
    """
    通用函数，统计指定列的分布情况及其对应 "无轨迹" 的数量。
    :param file_path: Excel 文件路径
    :param key_column: 需要统计的列名
    :param courier_column: 快递列名
    :return: 各值的总数和 "无轨迹" 数量的 Counter 对象
    """
    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]
        if key_column not in headers or courier_column not in headers:
            raise ValueError(f"列名 '{key_column}' 或 '{courier_column}' 不存在！")
        key_index = headers.index(key_column) + 1
        courier_index = headers.index(courier_column) + 1
        pattern = re.compile(Pattern.no_track, re.IGNORECASE)
        key_counter = Counter()
        key_no_track_counter = Counter()
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            key_value = row[key_index - 1]
            courier_status = row[courier_index - 1]
            if key_value is not None:
                key_counter[key_value] += 1
                if courier_status is not None and pattern.search(str(courier_status)):
                    key_no_track_counter[key_value] += 1
        return key_counter, key_no_track_counter
    except Exception as e:
        print(f"发生错误: {e}")
        return Counter(), Counter()


def count_distribution_and_no_track1(file_path, key_column, courier_column=RowName.Courier,
                                     sf_date_column=RowName.SfDateInterval):
    """
    通用函数，统计指定列的分布情况及其对应 "无轨迹" 的数量。
    :param file_path: Excel 文件路径
    :param key_column: 需要统计的列名
    :param courier_column: 快递列名
    :return: 各值的总数和 "无轨迹" 数量的 Counter 对象
    """
    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]
        if key_column not in headers or courier_column not in headers or sf_date_column not in headers:
            raise ValueError(f"列名 '{key_column}' 或 '{courier_column}' 或 '{sf_date_column}' 不存在！")
        key_index = headers.index(key_column) + 1
        courier_index = headers.index(courier_column) + 1
        sf_date_index = headers.index(sf_date_column) + 1
        pattern = re.compile(Pattern.no_track, re.IGNORECASE)
        key_counter = Counter()
        key_no_track_counter = Counter()
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            key_value = row[key_index - 1]
            courier_status = row[courier_index - 1]
            sf_date_value = row[sf_date_index - 1]
            if key_value is not None:
                key_counter[key_value] += 1
                if courier_status is not None:
                    if (pattern.search(str(courier_status))):
                        key_no_track_counter[key_value] += 1
                    elif (courier_status == "tracking" and sf_date_value == 0):
                        key_no_track_counter[key_value] += 1
        return key_counter, key_no_track_counter
    except Exception as e:
        print(f"发生错误: {e}")
        return Counter(), Counter()


def count_distribution_and_no_track2(file_path, key_column, courier_column=RowName.Courier):
    """
    通用函数，统计指定列的分布情况及其对应 "无轨迹"、"delivered"、"unpaid" 的数量。
    :param file_path: Excel 文件路径
    :param key_column: 需要统计的列名
    :param courier_column: 快递列名
    :return: 各值的总数和各个状态的数量的 Counter 对象
    """
    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]

        if key_column not in headers or courier_column not in headers:
            raise ValueError(f"列名 '{key_column}' 或 '{courier_column}' 不存在！")

        key_index = headers.index(key_column) + 1
        courier_index = headers.index(courier_column) + 1

        # 正则表达式匹配无轨迹、已送达、未支付状态
        pattern_no_track = re.compile(Pattern.no_track, re.IGNORECASE)
        pattern_no_tracking = re.compile(r"no_tracking", re.IGNORECASE)
        pattern_pre_ship = re.compile(r"pre_ship", re.IGNORECASE)
        pattern_not_yet = re.compile(r"not_yet", re.IGNORECASE)

        pattern_delivered = re.compile(r"delivered", re.IGNORECASE)
        pattern_unpaid = re.compile(r"unpaid", re.IGNORECASE)

        # 计数器
        key_counter = Counter()  # 统计每个key的总数
        key_no_track_counter = Counter()
        key_no_tracking_counter = Counter()
        key_pre_ship_counter = Counter()
        key_not_yet_counter = Counter()

        key_delivered_counter = Counter()
        key_unpaid_counter = Counter()

        # 遍历每一行，统计各个状态的数量
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            key_value = row[key_index - 1]
            courier_status = row[courier_index - 1]

            if key_value is not None:
                key_counter[key_value] += 1  # 统计总数

                if courier_status is not None and pattern_no_track.search(str(courier_status)):
                    key_no_track_counter[key_value] += 1

                if courier_status is not None and pattern_no_tracking.search(str(courier_status)):
                    key_no_tracking_counter[key_value] += 1

                if courier_status is not None and pattern_pre_ship.search(str(courier_status)):
                    key_pre_ship_counter[key_value] += 1

                if courier_status is not None and pattern_not_yet.search(str(courier_status)):
                    key_not_yet_counter[key_value] += 1

                if courier_status is not None and pattern_delivered.search(str(courier_status)):
                    key_delivered_counter[key_value] += 1

                if courier_status is not None and pattern_unpaid.search(str(courier_status)):
                    key_unpaid_counter[key_value] += 1

        return key_counter, key_no_track_counter, key_no_tracking_counter, key_pre_ship_counter, key_not_yet_counter, key_delivered_counter, key_unpaid_counter

    except Exception as e:
        print(f"发生错误: {e}")
        return Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter()


def count_distribution_and_no_track3(file_path, key_column, courier_column=RowName.Courier,
                                     sf_date_column=RowName.SfDateInterval):
    """
    通用函数，统计指定列的分布情况及其对应 "无轨迹"、"delivered"、"unpaid" 及 "tracking 且 SfDateEquality 为 0" 的数量。

    :param file_path: Excel 文件路径
    :param key_column: 需要统计的列名
    :param courier_column: 快递列名
    :param sf_date_column: SfDateEquality 列名
    :return: 各值的总数和各个状态的数量的 Counter 对象
    """
    try:
        workbook = load_workbook(file_path, data_only=True)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]

        # 确保列名存在
        if key_column not in headers or courier_column not in headers or sf_date_column not in headers:
            raise ValueError(f"列名 '{key_column}'、'{courier_column}' 或 '{sf_date_column}' 不存在！")

        key_index = headers.index(key_column)
        courier_index = headers.index(courier_column)
        sf_date_index = headers.index(sf_date_column)

        # 正则表达式匹配无轨迹、已送达、未支付状态
        pattern_no_track = re.compile(Pattern.no_track, re.IGNORECASE)
        pattern_no_tracking = re.compile(r"no_tracking", re.IGNORECASE)
        pattern_pre_ship = re.compile(r"pre_ship", re.IGNORECASE)
        pattern_not_yet = re.compile(r"not_yet", re.IGNORECASE)

        pattern_delivered = re.compile(r"delivered", re.IGNORECASE)
        pattern_unpaid = re.compile(r"unpaid", re.IGNORECASE)

        # 计数器
        key_counter = Counter()  # 统计每个key的总数
        key_no_track_counter = Counter()
        key_no_tracking_counter = Counter()
        key_pre_ship_counter = Counter()
        key_not_yet_counter = Counter()

        key_delivered_counter = Counter()
        key_unpaid_counter = Counter()
        key_tracking_sf_zero_counter = Counter()  # 统计 "Courier/快递" 为 tracking 且 "SfDateEquality" 为 0 的数量

        # 遍历数据行
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            key_value = row[key_index]
            courier_status = row[courier_index]
            sf_date_value = row[sf_date_index]

            if key_value is not None:
                key_counter[key_value] += 1  # 统计总数

                if courier_status is not None and pattern_no_track.search(str(courier_status)):
                    key_no_track_counter[key_value] += 1

                if courier_status is not None and pattern_no_tracking.search(str(courier_status)):
                    key_no_tracking_counter[key_value] += 1

                if courier_status is not None and pattern_pre_ship.search(str(courier_status)):
                    key_pre_ship_counter[key_value] += 1

                if courier_status is not None and pattern_not_yet.search(str(courier_status)):
                    key_not_yet_counter[key_value] += 1

                if courier_status is not None and pattern_delivered.search(str(courier_status)):
                    key_delivered_counter[key_value] += 1

                if courier_status is not None and pattern_unpaid.search(str(courier_status)):
                    key_unpaid_counter[key_value] += 1

                # 判断 "Courier/快递" 为 "tracking" 且 "SfDateEquality" 为 0
                if courier_status == "tracking" and sf_date_value == 0:
                    key_tracking_sf_zero_counter[key_value] += 1

        return key_counter, key_no_track_counter, key_no_tracking_counter, key_pre_ship_counter, key_not_yet_counter, key_delivered_counter, key_unpaid_counter, key_tracking_sf_zero_counter

    except Exception as e:
        print(f"发生错误: {e}")
        return Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter()


def analyze_time_segments(file_path, time_column, courier_column, sf_date_column):
    """
    按时间段（每3分钟为一段，忽略秒进行判断）统计总数和 "无轨迹" 的数量。
    额外统计：如果 "Courier/快递" 列内容为 "tracking" 且 "SfDateEquality" 列的内容为 0，"无轨迹" 计数也 +1。

    :param file_path: Excel 文件路径
    :param time_column: 时间列名（格式："2025-01-22 23:11:43"）
    :param courier_column: 快递状态列名
    :param sf_date_column: SfDateEquality 列名
    :return: 以 3 分钟为一段的统计数据
    """
    try:
        # 加载 Excel 文件
        workbook = load_workbook(file_path, data_only=True)
        sheet = workbook.active

        # 获取表头
        headers = [cell.value for cell in sheet[1]]
        if time_column not in headers or courier_column not in headers or sf_date_column not in headers:
            raise ValueError(f"列名 '{time_column}'、'{courier_column}' 或 '{sf_date_column}' 不存在！")

        # 获取列索引
        time_index = headers.index(time_column)
        courier_index = headers.index(courier_column)
        sf_date_index = headers.index(sf_date_column)

        # 正则表达式匹配 "无轨迹"
        pattern_no_track = re.compile(r"(no_tracking|pre_ship|not_yet)", re.IGNORECASE)

        # 读取并解析数据
        data = []
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            order_time = row[time_index]
            courier_status = row[courier_index]
            sf_date_value = row[sf_date_index]

            if order_time is not None and isinstance(order_time, str):
                try:
                    # 解析时间格式为 "2025-01-22 23:11:43"
                    order_time = datetime.strptime(order_time, "%Y-%m-%d %H:%M:%S")
                    order_time_without_seconds = order_time.replace(second=0)
                    data.append((order_time, order_time_without_seconds, courier_status, sf_date_value))
                except ValueError:
                    continue

        # 按时间段归类
        data.sort(key=lambda x: x[1])  # 按无秒时间排序
        time_segments = defaultdict(list)
        if data:
            base_time = data[0][1]  # 使用无秒时间作为基准
            current_segment = []
            for full_time, order_time_without_seconds, courier_status, sf_date_value in data:
                if (order_time_without_seconds - base_time).total_seconds() <= 180:  # 3分钟内
                    current_segment.append((full_time, courier_status, sf_date_value))
                else:
                    time_segments[base_time].extend(current_segment)
                    base_time = order_time_without_seconds
                    current_segment = [(full_time, courier_status, sf_date_value)]
            if current_segment:
                time_segments[base_time].extend(current_segment)

        # 统计每个时间段的总数和无轨迹数量
        segment_statistics = {}
        for segment_start, entries in time_segments.items():
            total_count = len(entries)
            no_track_count = sum(
                1 for _, courier_status, sf_date_value in entries
                if (courier_status is not None and pattern_no_track.match(str(courier_status))) or
                (courier_status == "tracking" and sf_date_value == 0)  # 新增 tracking & SfDateEquality=0 的判断
            )
            segment_statistics[segment_start] = {
                "total_count": total_count,
                "no_track_count": no_track_count,
                "entries": entries,  # 记录每条数据
            }

        return segment_statistics

    except Exception as e:
        print(f"发生错误: {e}")
        return {}


def check_and_add_courier_column(file_path):
    """
    检查 Excel 文件是否存在 '快递' 列，如果没有，则在最后一列添加该列。

    :param file_path: Excel 文件路径
    :param courier_column: 快递列名，默认为 'Courier/快递'
    :return: None
    """
    try:
        # 加载 Excel 文件
        data = pd.read_excel(file_path, engine='openpyxl')
        # 判断是否存在 '快递' 列
        if RowName.Courier not in data.columns:
            # 如果没有 '快递' 列，则在最后一列添加该列
            data[RowName.Courier] = ""  # 默认为空值，可以根据需求填充其他默认值
        if RowName.PossessionSfDate not in data.columns:
            data[RowName.PossessionSfDate] = ""
        if RowName.LatestEventSfDate not in data.columns:
            data[RowName.LatestEventSfDate] = ""
        if RowName.SfDateInterval not in data.columns:
            data[RowName.SfDateInterval] = ""
        # 保存修改后的文件
        data.to_excel(file_path, index=False, engine='openpyxl')
    except Exception as e:
        print(f"发生错误: {e}")


def get_days_difference(file_path, column_name=RowName.OutboundTime):
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
        # 解析日期
        outbound_time = datetime.strptime(first_row_value, "%Y-%m-%d %H:%M:%S")
        # 格式化为 "%Y/%m/%d" 格式
        formatted_date = outbound_time.strftime("%Y/%m/%d")
        return formatted_date
    except Exception as e:
        print(f"发生错误: {e}")
        return None


def get_unpaid_platform_tracking_map(file_path):
    """
    获取 Courier/快递 列内容为 'unpaid' 对应的 Platform Number/平台单号 和
    Tracking No./物流跟踪号的内容，并存放到字典中。

    :param file_path: Excel 文件路径
    :return: 字典，key 为 Platform Number/平台单号，value 为 Tracking No./物流跟踪号
    """
    # 读取 Excel 文件
    data = pd.read_excel(file_path)

    # 确保 "Courier/快递"、"Platform Number/平台单号" 和 "Tracking No./物流跟踪号" 列存在
    if 'Courier/快递' not in data.columns or 'Platform Number/平台单号' not in data.columns or 'Tracking No./物流跟踪号' not in data.columns:
        raise ValueError("文件中缺少所需的列，请检查文件结构")

    # 筛选出 "Courier/快递" 列内容为 "unpaid" 的行
    unpaid_data = data[data['Courier/快递'] == 'unpaid']

    # 创建一个字典，key 为 Platform Number/平台单号，value 为 Tracking No./物流跟踪号
    platform_tracking_map = {}

    # 遍历筛选出的数据并填充字典
    for _, row in unpaid_data.iterrows():
        platform_number = row['Platform Number/平台单号']
        tracking_number = row['Tracking No./物流跟踪号']
        shipping_service = row['Shipping service/物流渠道']
        recipient = row['Recipient/收件人']
        kj_ = (shipping_service == '上传物流面单(Upload_Shipping_Label)' and recipient == 'KJ') or \
              (shipping_service != '上传物流面单(Upload_Shipping_Label)')
        platform_tracking_map[platform_number] = {"tracking_number": tracking_number, "kj": kj_}

    # 返回结果字典
    return platform_tracking_map


def convert_inch_to_cm(value_in_inch):
    """
    将英寸转换为厘米
    :param value_in_inch: 英寸数
    :return: 转换后的厘米数
    """
    return round2(value_in_inch * 2.54)


def get_in(file_path, sku_to_match):
    # 读取 Excel 文件
    data = pd.read_excel(file_path)

    # 确保相关列存在
    required_columns = ['SKU', 'Length/长', 'Width/宽', 'Height/高', 'Unit/单位']
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"文件中缺少所需的列，请检查文件结构")

    # 查找匹配的第一个 SKU
    matched_row = data[data['SKU'] == sku_to_match].iloc[0]  # 获取第一个匹配的行

    # 提取数据
    length = matched_row['Length/长']
    width = matched_row['Width/宽']
    height = matched_row['Height/高']
    unit = matched_row['Unit/单位']

    # 如果单位是英寸，进行转换
    if unit == 'in':
        length = convert_inch_to_cm(length)
        width = convert_inch_to_cm(width)
        height = convert_inch_to_cm(height)
        unit = 'cm'  # 转换后的单位为厘米

    # 返回一个字典，包含转换后的数据
    result = {
        'SKU': sku_to_match,
        'Length': length,
        'Width': width,
        'Height': height,
        'Unit': unit
    }

    return result


def sku_kj_count(file_path, sku_value, sku_column='SKU', shipping_service_column='Shipping service/物流渠道',
                 recipient_column='Recipient/收件人'):
    # 读取 Excel 文件
    data = pd.read_excel(file_path)

    # 确保必要的列存在
    if sku_column not in data.columns or shipping_service_column not in data.columns or recipient_column not in data.columns:
        raise ValueError(f"文件中缺少必要的列，请检查列名是否正确")

    # 筛选出 SKU 列为指定内容，且满足以下两种情况之一：
    # 1. 'Shipping service/物流渠道' 为 '上传物流面单(Upload_Shipping_Label)' 且 'Recipient/收件人' 为 'KJ'
    # 2. 'Shipping service/物流渠道' 不为 '上传物流面单(Upload_Shipping_Label)'
    filtered_data = data[
        (data[sku_column] == sku_value) &  # 筛选 SKU 列为指定值
        (
                ((data[shipping_service_column] == '上传物流面单(Upload_Shipping_Label)') & (
                        data[recipient_column] == 'KJ')) |  # 满足第一个条件
                (data[shipping_service_column] != '上传物流面单(Upload_Shipping_Label)')  # 满足第二个条件
        )
        ]

    # 返回符合条件的行数
    return len(filtered_data)


def kj_count(file_path, shipping_service_column='Shipping service/物流渠道', recipient_column='Recipient/收件人'):
    # 读取 Excel 文件
    data = pd.read_excel(file_path)

    # 确保必要的列存在
    if shipping_service_column not in data.columns or recipient_column not in data.columns:
        raise ValueError(f"文件中缺少必要的列，请检查列名是否正确")

    # 条件1：'Shipping service/物流渠道' 不为 '上传物流面单(Upload_Shipping_Label)' 的行
    condition1 = (data[shipping_service_column] != '上传物流面单(Upload_Shipping_Label)')

    # 条件2：'Shipping service/物流渠道' 为 '上传物流面单(Upload_Shipping_Label)' 且 'Recipient/收件人' 为 'KJ' 的行
    condition2 = (data[shipping_service_column] == '上传物流面单(Upload_Shipping_Label)') & (
            data[recipient_column] == 'KJ')

    # 综合筛选符合任一条件的行
    filtered_data = data[condition1 | condition2]

    # 返回符合条件的行数
    return len(filtered_data)


def generate_distribution_report(distribution, no_track_distribution, data_map, data_map_key):
    """
    通用的分布报告生成函数
    :param distribution: 订单分布字典
    :param no_track_distribution: 无轨迹分布字典
    :param data_map:
    :param data_map_key: 用于存储到 `data_map` 的 key（例如 `CellKey.warehouse_condition` 或 `CellKey.store_condition`）
    :return: 生成的分布报告文本
    """
    report_text = ""
    report_text2 = ""
    lowest_swl = 101  # 初始化为一个比 100 大的值，用于比较
    lowest_entity = ""  # 保存最低上网率的实体信息

    # 遍历分布数据
    for entity, count in distribution.items():
        no_track_count = no_track_distribution.get(entity, 0)
        swl = round2(100 - ((int(no_track_count) / int(count)) * 100))
        # strs = f"\n{entity}： 订单总数：{count}；无轨迹数：{no_track_count}；上网率：{swl}%"
        strs = f"\n{entity}：（{count}, {no_track_count}, {swl}%）"
        strs2 = f"\n{entity}：({count},{swl}%)"
        report_text += strs
        report_text2 += strs2

        # 判断是否是最低的上网率
        if swl < lowest_swl:
            lowest_swl = swl
            lowest_entity = strs

    data_map[data_map_key] = report_text  # 将结果存储到 data_map 中
    return report_text, lowest_entity, report_text2


def generate_distribution_report2(distribution, no_track_distribution, sku_no_tracking_distribution,
                                  sku_pre_ship_distribution, sku_not_yet_distribution, sku_delivered_distribution,
                                  sku_unpaid_distribution, tracking_sf_zero_distribution,
                                  data_map, data_map_key, interval_time, xlsx_path):
    """
    通用的分布报告生成函数，统计订单分布、无轨迹订单、计算上网率，并找出最低上网率的所有实体
    :param distribution: 订单分布字典
    :param no_track_distribution: 无轨迹分布字典
    :param data_map:
    :param data_map_key: 用于存储到 `data_map` 的 key（例如 `CellKey.warehouse_condition` 或 `CellKey.store_condition`）
    :return: 生成的分布报告文本, 最低上网率的所有实体信息, 精简版报告文本
    """
    report_text = ""
    report_text2 = ""
    lowest_swl = 101  # 初始化为比100大的值
    lowest_entities = {}  # 存储多个最低上网率的实体信息

    # 遍历分布数据
    for entity, count in distribution.items():
        no_track_count = no_track_distribution.get(entity, 0)
        no_tracking_count = sku_no_tracking_distribution.get(entity, 0)
        pre_ship_count = sku_pre_ship_distribution.get(entity, 0)
        not_yet_count = sku_not_yet_distribution.get(entity, 0)
        delivered_count = sku_delivered_distribution.get(entity, 0)
        unpaid_count = sku_unpaid_distribution.get(entity, 0)
        tracking_sf_zero_count = tracking_sf_zero_distribution.get(entity, 0)

        swl = round2(100 - ((int(no_track_count + tracking_sf_zero_count) / int(count)) * 100))  # 计算上网率
        in_data = get_in(xlsx_path, entity)
        length_ = in_data['Length']
        width_ = in_data['Width']
        height_ = in_data['Height']
        unit_ = in_data['Unit']
        kjCount = sku_kj_count(xlsx_path, entity)

        strs = ""
        # 生成报告内容
        if (swl != 100.0):
            # strs = f"\n{entity}： 订单总数：{count}；无轨迹数：{no_track_count}；上网率：{swl}%"
            strs = f"\n{entity}：（{count}, {no_track_count + tracking_sf_zero_count}, {swl}%）,（{no_tracking_count}, {pre_ship_count}, " \
                   f"{not_yet_count}, {tracking_sf_zero_count}, {delivered_count}, {unpaid_count}）,（{kjCount}, {length_}*{width_}*{height_}*{unit_}）"
            strs2 = f"\n{entity}：({count},{swl}%)"
            report_text += strs
            report_text2 += strs2

        # 更新最低上网率的实体
        if swl < lowest_swl:
            lowest_swl = swl
            lowest_entities.clear()  # 清空数据
            lowest_entities[entity] = {"entity": entity, "count": count,
                                       "no_track_count": (no_track_count + tracking_sf_zero_count), "swl": swl,
                                       "strs": strs}
        elif swl == lowest_swl:
            lowest_entities[entity] = {"entity": entity, "count": count,
                                       "no_track_count": (no_track_count + tracking_sf_zero_count), "swl": swl,
                                       "strs": strs}

    resultList = []
    for key, value in lowest_entities.items():
        no_track_counts = value["no_track_count"]
        strss = value["strs"]
        if (interval_time >= 3):
            resultList.append(strss)
        else:
            if (no_track_counts >= 4):
                resultList.append(strss)

    data_map[data_map_key] = report_text  # 将结果存储到 data_map
    return report_text, resultList, report_text2


def go(analyse_obj, xlsx_path):
    if analyse_obj is None:
        analyse_obj = input("请输跟踪对象（zbw/sanrio/xyl/mz_xsd/md_fc/mx_dg）：")

    if analyse_obj != ClientConstants.zbw \
            and analyse_obj != ClientConstants.sanrio \
            and analyse_obj != ClientConstants.xyl \
            and analyse_obj != ClientConstants.mz_xsd \
            and analyse_obj != ClientConstants.md_fc \
            and analyse_obj != ClientConstants.mx_dg:
        raise ValueError(f"{analyse_obj} 未定义")

    if xlsx_path is None:
        xlsx_path = input("请输入文件的绝对路径：")

    check_and_add_courier_column(xlsx_path)

    irregular_number_map = find_irregular_tracking_numbers(xlsx_path)
    irregular_number_list = []
    if irregular_number_map:
        irregular_number_list = list(irregular_number_map.keys())
        print(f"存在无效的物流跟踪号：{irregular_number_list}")
        update_courier_status(xlsx_path, {CourierStateMapKey.irregular_number_map: irregular_number_map})

    results = extract_and_process_data(xlsx_path, RowName.Courier, 100)

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
    }

    update_courier_status(xlsx_path, all_maps, wl=RowName.Tracking_No, column_map=column_mapping)

    # 数据map
    data_map = {}

    text = ""

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ck_time = get_days_difference(xlsx_path)
    gz_time = getYmd()
    interval_time = (datetime.strptime(gz_time, "%Y/%m/%d") - datetime.strptime(ck_time, "%Y/%m/%d")).days
    is_usweekend = is_us_weekend(ck_time)
    date_obj = datetime.strptime(ck_time, "%Y/%m/%d").date()
    previous_day = date_obj - timedelta(days=1)

    Outbound_Time = ""
    Outbound_Time += ck_time
    Outbound_Time += f"\n{get_weekday(ck_time)}"
    us_holiday = get_american_holiday(previous_day)
    if us_holiday:
        Outbound_Time += f"\n美国节日: {us_holiday}"
    cn_holiday = get_chinese_holiday(date_obj)
    if cn_holiday:
        Outbound_Time += f"\n中国节日: {cn_holiday}"

    date_obj1 = datetime.strptime(gz_time, "%Y/%m/%d").date()
    previous_day1 = date_obj1 - timedelta(days=1)
    Update_Time = ""
    Update_Time += current_time
    Update_Time += f"\n{get_weekday(gz_time)}"
    us_holiday1 = get_american_holiday(previous_day1)
    if us_holiday1:
        Update_Time += f"\n美国节日: {us_holiday1}"
    cn_holiday1 = get_chinese_holiday(date_obj1)
    if cn_holiday1:
        Update_Time += f"\n中国节日: {cn_holiday1}"

    text += "\n----------------------时间----------------------"
    text += f"\n更新时间: {Update_Time}"
    text += f"\n出库日期：{Outbound_Time}"
    text += f"\n跟踪日期：{gz_time}"
    text += f"\n间隔时间：{interval_time}"
    data_map[CellKey.Outbound_Time] = Outbound_Time
    data_map[CellKey.update_time] = Update_Time

    text += "\n----------------------非usps物流跟踪号----------------------"
    irregular_number_text = ""
    if (len(irregular_number_list) > 0):
        irregular_number_text = "\n非usps物流跟踪号："
        for ele in irregular_number_list:
            irregular_number_text += f"\n"
            irregular_number_text += ele
    text += irregular_number_text

    text += "\n----------------------unpaid详情----------------------"
    unpaid_text = ""
    result_map = get_unpaid_platform_tracking_map(xlsx_path)
    if (len(result_map) > 0):
        unpaid_text = "\nunpaid详情："
        for key, value in result_map.items():
            value1 = value["tracking_number"]
            value2 = value["kj"]
            if (analyse_obj == ClientConstants.sanrio):
                unpaid_text += f"\n平台单号：{key}, 物流跟踪号：{value1}, 是否kj：{value2}"
            else:
                unpaid_text += f"\n物流跟踪号：{value1}, 是否kj：{value2}"
            unpaid_text += f"\n"
    text += unpaid_text

    data_map[CellKey.special_information] = irregular_number_text + unpaid_text

    text += "\n----------------------SKU分布----------------------"
    sku_distribution, sku_no_track_distribution, sku_no_tracking_distribution, sku_pre_ship_distribution, \
        sku_not_yet_distribution, sku_delivered_distribution, sku_unpaid_distribution, key_tracking_sf_zero_counter = count_distribution_and_no_track3(
        xlsx_path, key_column=RowName.SKU)
    sku_text, lowest_sku, sku_text2 = generate_distribution_report2(
        sku_distribution, sku_no_track_distribution, sku_no_tracking_distribution, sku_pre_ship_distribution,
        sku_not_yet_distribution, sku_delivered_distribution, sku_unpaid_distribution, key_tracking_sf_zero_counter,
        data_map, CellKey.sku_condition,
        interval_time, xlsx_path
    )
    text += sku_text

    output_file = os.path.splitext(xlsx_path)[0] + "_去重.xlsx"
    # 同一单会有多个sku，多个sku会生成多行数据，分析sku的时候不能去重，其它的需要去重
    remove_duplicates_by_column(xlsx_path, output_file, RowName.Tracking_No)

    total_count, no_track_count = count_pattern_state(output_file, RowName.Courier, Pattern.no_track)
    track_count = total_count - no_track_count
    total_count2, delivered_count = count_pattern_state(output_file, RowName.Courier, Pattern.delivered)
    total_count3, unpaid_count = count_pattern_state(output_file, RowName.Courier, Pattern.unpaid)
    total_count4, not_yet_count = count_pattern_state(output_file, RowName.Courier, Pattern.not_yet)
    total_count5, pre_ship_count = count_pattern_state(output_file, RowName.Courier, Pattern.pre_ship)
    total_count6, irregular_no_tracking_count = count_pattern_state(output_file, RowName.Courier,
                                                                    Pattern.irregular_no_tracking)
    total_count7, no_tracking_count = count_pattern_state(output_file, RowName.Courier, Pattern.no_tracking)
    total_count8, tracking_count = count_pattern_state(output_file, RowName.Courier, Pattern.tracking)
    tracking_zero_count = count_tracking_with_sf_date_equality(output_file)

    swl = round2(100 - ((int(no_track_count + tracking_zero_count) / int(total_count)) * 100))
    wswl = round2(100 - swl)
    qsl = round2((int(delivered_count) / int(total_count)) * 100)
    unpaidl = round2((int(unpaid_count) / int(total_count)) * 100)
    not_yetl = round2((int(not_yet_count) / int(total_count)) * 100)
    pre_shipl = round2((int(pre_ship_count) / int(total_count)) * 100)
    irregular_no_trackingl = round2((int(irregular_no_tracking_count) / int(total_count)) * 100)
    no_tracking_countl = round2((int(no_tracking_count) / int(total_count)) * 100)
    tracking_countl = round2((int(tracking_count - tracking_zero_count) / int(total_count)) * 100)
    tracking_zero_countl = round2((int(tracking_zero_count) / int(total_count)) * 100)

    kj_counts = kj_count(output_file)

    wl = ""
    wl += f"\n订单总数：{total_count}"
    wl += f"\nKJ订单总数：{kj_counts}"
    wl += f"\n"
    wl += f"\n上网：（{track_count - tracking_zero_count}, {swl}%）"
    wl += f"\n未上网：（{no_track_count + tracking_zero_count}, {wswl}%）"
    wl += f"\n"
    wl += f"\ndelivered：（{delivered_count}, {qsl}%）"
    wl += f"\nunpaid：（{unpaid_count}, {unpaidl}%）"
    wl += f"\ntracking：（{tracking_count - tracking_zero_count}, {tracking_countl}%）"
    wl += f"\ntracking_zero：（{tracking_zero_count}, {tracking_zero_countl}%）"

    wl += f"\nno_tracking：（{no_tracking_count}, {no_tracking_countl}%）"
    wl += f"\nnot_yet：（{not_yet_count}, {not_yetl}%）"
    wl += f"\npre_ship：（{pre_ship_count}, {pre_shipl}%）"
    wl += f"\nirregular_no_tracking：（{irregular_no_tracking_count}, {irregular_no_trackingl}%）"

    wl += f"\n"
    wl += irregular_number_text + unpaid_text

    text += "\n----------------------轨迹概览----------------------"
    text += wl
    data_map[CellKey.wl] = wl

    text += "\n----------------------仓库分布----------------------"
    warehouse_distribution, warehouse_no_track = count_distribution_and_no_track1(
        output_file, key_column=RowName.Warehouse)
    warehouse_text, lowest_warehouse, warehouse_text2 = generate_distribution_report(
        warehouse_distribution, warehouse_no_track, data_map, CellKey.warehouse_condition
    )
    text += warehouse_text

    text += "\n----------------------店铺分布----------------------"
    store_distribution, store_no_track_distribution = count_distribution_and_no_track1(
        output_file, key_column=RowName.Client)
    store_text, lowest_store, store_text2 = generate_distribution_report(
        store_distribution, store_no_track_distribution, data_map, CellKey.store_condition
    )
    text += store_text

    text += "\n----------------------物流渠道分布----------------------"
    shipping_service_distribution, shipping_service_no_track_distribution = count_distribution_and_no_track1(
        output_file, key_column=RowName.ShippingService)
    shipping_service_text, lowest_shipping_service, shipping_service_text2 = generate_distribution_report(
        shipping_service_distribution, shipping_service_no_track_distribution, data_map,
        CellKey.shipping_service_condition
    )
    text += shipping_service_text

    text += "\n----------------------时间段分布----------------------"
    time_segment_analysis = analyze_time_segments(
        output_file, time_column=RowName.CreationWaveTime, courier_column=RowName.Courier,
        sf_date_column=RowName.SfDateInterval)
    time_segment_text = ""
    lowest_segment = ""  # 保存上网率最低的时间段
    lowest_swl = 101  # 初始化为比 100 大的值
    for segment_start, stats in time_segment_analysis.items():
        segment_end = segment_start + timedelta(minutes=3)
        total_count_temp = stats["total_count"]
        no_track_count = stats["no_track_count"]
        segmentswl = round2(100 - ((int(no_track_count) / int(total_count_temp)) * 100))
        # strs = f"\n{segment_start.strftime('%y-%m-%d %H:%M')} - {segment_end.strftime('%y-%m-%d %H:%M')}： 订单总数：{total_count_temp}；无轨迹数：{no_track_count}；上网率：{segmentswl}%"
        strs = f"\n{segment_start.strftime('%y-%m-%d %H:%M')} - {segment_end.strftime('%y-%m-%d %H:%M')}：（{total_count_temp}, {no_track_count}, {segmentswl}%）"
        text += strs
        time_segment_text += strs
        # 判断是否是最低的上网率
        if segmentswl < lowest_swl:
            lowest_swl = segmentswl
            lowest_segment = strs
    data_map[CellKey.time_segment_condition] = time_segment_text

    lowest_txt = ""
    lowest_txt += f"\n"
    if (len(lowest_sku) > 0):
        lowest_txt += f"\n最低上网率的 SKU："
        for item in lowest_sku:
            lowest_txt += item
    lowest_txt += f"\n最低上网率的 仓库：{lowest_warehouse}"
    lowest_txt += f"\n最低上网率的 商店：{lowest_store}"
    lowest_txt += f"\n最低上网率的 时间段：{lowest_segment}"
    lowest_txt += f"\n最低上网率的 物流渠道：{lowest_shipping_service}"

    sum_up_text = ""

    actual_interval = ""
    if (is_usweekend == 6):  # 6是中国周日，美国周六
        sum_up_text += f"美国时间：周六（和中国相差13-16个小时）"
        sum_up_text += f"\n"
        actual_interval = "（-2）"
    elif (is_usweekend == 0):  # 0是中国周一，美国周日
        sum_up_text += f"美国时间：周日（相差13-16个小时）"
        sum_up_text += f"\n"
        actual_interval = "（-1）"
    else:
        actual_interval = ""

    # if (len(irregular_number_list) > 0):
    #     sum_up_text += f"存在不规则单号：{irregular_number_list}"
    #     sum_up_text += f"\n"

    swl_flag = False
    qsl_flag = False
    bg = "#ffffff"

    # 如果三天后的上网率没有99%以上，那么就严重有问题；隔天应该要 》= 三分之一，隔两天应该要有》=75
    if (interval_time == 0):
        sum_up_text += f"\n间隔第{interval_time}{actual_interval}天，上网率为{swl}%，继续观察👀！"
    elif (interval_time == 1):
        if (swl < 30):
            sum_up_text += f"\n☁️注意：间隔第{interval_time}{actual_interval}天，上网率为{swl}%，未达30%，建议跟进！"
            swl_flag = True
            bg = "#F8F1D3"
        else:
            sum_up_text += f"\n☀️间隔第{interval_time}{actual_interval}天，上网率为{swl}%，上网率优秀"
    elif (interval_time == 2):
        if (swl < 70):
            sum_up_text += f"\n🌧️异常：间隔第{interval_time}{actual_interval}天，上网率为{swl}%，未达75%，建议分析数据尝试定位问题！"
            swl_flag = True
            bg = "#E3C49C"
        else:
            sum_up_text += f"\n☀️间隔第{interval_time}{actual_interval}天，上网率为{swl}%，上网率优秀"
    else:  # 间隔时间 >= 3天
        if (swl < 97):
            sum_up_text += f"\n❄️⛈️🌀⚠️🚨警报：间隔第{interval_time}{actual_interval}天，上网率为{swl}%，未达97%，分析数据反馈问题！"
            swl_flag = True
            bg = "#F1C1BD"
        else:
            sum_up_text += f"\n☀️间隔第{interval_time}{actual_interval}天，上网率为{swl}%，上网率优秀"

    # 要持续监控一个星期才行，从出库开始计算，三天内没有签收的不正常，五天内签收没达到50%也不正常，7天内没到90也不正常
    if (interval_time >= 1 and interval_time <= 3):
        if (interval_time >= 2 and qsl == 0):
            sum_up_text += f"\n🚨警报：间隔第{interval_time}{actual_interval}天，签收率为0%，异常状态！"
            qsl_flag = True
        else:
            sum_up_text += f"\n☀️间隔第{interval_time}{actual_interval}天，签收率为{qsl}%，继续跟进！"
    elif (interval_time > 3 and interval_time <= 5):
        if (qsl <= 20):
            sum_up_text += f"\n🚨警报：间隔第{interval_time}{actual_interval}天，签收率为{qsl}%，异常状态！"
            qsl_flag = True
        else:
            sum_up_text += f"\n☀️间隔第{interval_time}{actual_interval}天，签收率为{qsl}%，继续跟进！"
    elif (interval_time > 5 and interval_time <= 7):
        if (qsl <= 50):
            sum_up_text += f"\n🚨警报：间隔第{interval_time}{actual_interval}天，签收率为{qsl}%，异常状态！"
            qsl_flag = True
        else:
            sum_up_text += f"\n☀️间隔第{interval_time}{actual_interval}天，签收率为{qsl}%，继续跟进！"
    elif (interval_time > 7 and interval_time <= 9):
        if (qsl <= 80):
            sum_up_text += f"\n🚨警报：间隔第{interval_time}{actual_interval}天，签收率为{qsl}%，异常状态！"
            qsl_flag = True
        else:
            sum_up_text += f"\n☀️间隔第{interval_time}{actual_interval}天，签收率为{qsl}%，继续跟进！"
    else:
        if (qsl >= 98):
            sum_up_text += f"\n☀️间隔第{interval_time}{actual_interval}天，签收率为{qsl}%，签收率优秀！"
        else:
            sum_up_text += f"\n☀️间隔第{interval_time}{actual_interval}天，签收率为{qsl}%，继续跟进！"

    text += "\n----------------------总结&建议----------------------"
    if (swl < 100):
        sum_up_text += lowest_txt
    text += f"\n{sum_up_text}"
    data_map[CellKey.sum_up] = sum_up_text

    if (swl_flag or qsl_flag):
        if (swl_flag and qsl_flag):
            data_map[CellKey.exception] = "上网率&签收率 异常\n（签收率目前无法量化，只为提醒⏰）"
        elif (swl_flag):
            data_map[CellKey.exception] = "上网率异常"
        elif (qsl_flag):
            data_map[CellKey.exception] = "签收率异常\n（签收率目前无法量化，只为提醒⏰）"
    else:
        data_map[CellKey.exception] = ""

    # 删除去重文件
    delete_file(output_file)
    # 数据打印
    # print(data_map)
    print(text)

    # 写入飞书在线文档
    # tat = get_token()
    # if analyse_obj == ClientConstants.zbw or analyse_obj == ClientConstants.sanrio or analyse_obj == ClientConstants.xyl:
    #     lists = f"({total_count},{swl}%)"
    #     lists += f"\n{warehouse_text2}"
    #     brief_sheet_value(tat, [lists], ck_time, gz_time, analyse_obj)
    #     if (swl_flag):
    #         brief_sheet_bg(tat, ck_time, gz_time, analyse_obj, bg)
    # else:
    #     lists = f"({total_count},{swl}%)"
    #     brief_sheet_value(tat, [lists], ck_time, gz_time, analyse_obj)
    #     if (swl_flag):
    #         brief_sheet_bg(tat, ck_time, gz_time, analyse_obj, bg)
    #
    # if analyse_obj == ClientConstants.mz_xsd or \
    #         analyse_obj == ClientConstants.mx_dg or \
    #         analyse_obj == ClientConstants.md_fc:
    #     detail_sheet_value(tat, [
    #         data_map[CellKey.Outbound_Time],
    #         data_map[CellKey.update_time],
    #         data_map[CellKey.wl],
    #         data_map[CellKey.store_condition],
    #         data_map[CellKey.time_segment_condition],
    #         data_map[CellKey.shipping_service_condition],
    #         data_map[CellKey.sum_up],
    #         data_map[CellKey.exception],
    #     ], ck_time, analyse_obj)
    #
    #     if (swl_flag):
    #         detail_sheet_bg(tat, ck_time, analyse_obj, bg)
    # else:
    #     detail_sheet_value(tat, [
    #         data_map[CellKey.Outbound_Time],
    #         data_map[CellKey.update_time],
    #         data_map[CellKey.wl],
    #         data_map[CellKey.warehouse_condition],
    #         data_map[CellKey.store_condition],
    #         data_map[CellKey.time_segment_condition],
    #         data_map[CellKey.shipping_service_condition],
    #         data_map[CellKey.sku_condition],
    #         data_map[CellKey.sum_up],
    #         data_map[CellKey.exception],
    #     ], ck_time, analyse_obj)
    #
    #     if (swl_flag):
    #         detail_sheet_bg(tat, ck_time, analyse_obj, bg)


def automatic(dir_path, analyse_obj):
    for root, dirs, files in os.walk(dir_path):
        """
        root: 当前文件夹路径
        dirs: 当前文件夹下的子文件夹列表
        files: 当前文件夹下的文件列表
        """
        # print(f"当前文件夹: {root}")
        # print(f"子文件夹: {dirs}")
        # print(f"文件: {files}")
        # print("--------")
        pattern = r"^出库时间\d+_\d+\.xlsx$"  # 正则表达式
        for ele in files:
            if re.match(pattern, ele):
                xlsx_path = f"{root}/{ele}"
                print(f"匹配的文件: {xlsx_path}")
                try:
                    total_count, no_track_count = count_pattern_state(xlsx_path, RowName.Courier, Pattern.no_track)
                    tracking_zero_count = count_tracking_with_sf_date_equality(xlsx_path)
                    total_count2, delivered_count = count_pattern_state(xlsx_path, RowName.Courier, Pattern.delivered)

                    if total_count == 0:
                        swl = 0
                    else:
                        swl = round2(100 - ((int(no_track_count + tracking_zero_count) / int(total_count)) * 100))

                    if total_count == 0:
                        qsl = 0
                    else:
                        qsl = round2((int(delivered_count) / int(total_count)) * 100)

                    if swl < 99 or qsl < 98:
                        go(analyse_obj, xlsx_path)
                except ZeroDivisionError:
                    print(f"警告：{xlsx_path} 的 total_count 为 0，跳过计算。")
                    go(analyse_obj, xlsx_path)  # 仍然执行 go 但避免除零错误
                except Exception as e:
                    print(f"处理 {xlsx_path} 时发生错误: {e}")
                    go(analyse_obj, xlsx_path)


if __name__ == '__main__':
    # # 手动
    # go(None, None)
    go(ClientConstants.zbw, "/Users/zkp/Desktop/B&Y/轨迹统计/zbw/2025.3/出库时间5_144.xlsx")
    # # 自动
    # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/zbw", ClientConstants.zbw)
    # # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/zbw/2025.1", ClientConstants.zbw)
    # # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/zbw/2025.2", ClientConstants.zbw)
    # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/zbw/2025.3", ClientConstants.zbw)
    # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/sanrio", ClientConstants.sanrio)
    # # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/sanrio/2025.1", ClientConstants.sanrio)
    # # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/sanrio/2025.2", ClientConstants.sanrio)
    # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/sanrio/2025.3", ClientConstants.sanrio)
    # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/xyl", ClientConstants.xyl)
    # # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/xyl/2025.2", ClientConstants.xyl)
    # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/xyl/2025.3", ClientConstants.xyl)
    # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/mzxsd", ClientConstants.mz_xsd)
    # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/mxdg", ClientConstants.mx_dg)
    # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/mdfc", ClientConstants.md_fc)
    # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/mzxsd/2025.3", ClientConstants.mz_xsd)
    # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/mxdg/2025.3", ClientConstants.mx_dg)
    # automatic("/Users/zkp/Desktop/B&Y/轨迹统计/mdfc/2025.3", ClientConstants.md_fc)
