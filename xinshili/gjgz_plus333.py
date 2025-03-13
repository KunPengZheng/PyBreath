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
    OutboundTime = "Creation time/创建时间"
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
    warehouse_condition = "warehouse_condition"
    store_condition = "store_condition"
    sku_condition = "sku_condition"
    time_segment_condition = "time_segment_condition"
    sum_up = "sum_up"
    exception = "exception"
    shipping_service_condition = "shipping_service_condition"
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
    查找不规则的快递单号（不是纯数字、不是9开头、或者包含下划线）
    :param filepath: Excel文件路径
    :param column_name: 需要检查的列名，默认为 'Tracking No./物流跟踪号'
    :return: 不规则快递单号字典
    """
    try:
        # 打开xlsx文件
        wb = openpyxl.load_workbook(filepath, data_only=True)
        sheet = wb.active  # 默认使用活动工作表

        # 获取 'Tracking No./物流跟踪号' 列索引
        tracking_no_col = next(
            (col for col in range(1, sheet.max_column + 1) if sheet.cell(row=1, column=col).value == column_name),
            None
        )

        if tracking_no_col is None:
            print(f"找不到 {column_name} 列")
            return {}

        # 存储不规则快递单号的字典
        irregular_number_map = {}

        # 遍历所有行，从第二行开始（跳过表头）
        for row in range(2, sheet.max_row + 1):
            tracking_no = str(sheet.cell(row=row, column=tracking_no_col).value).strip()  # 转换为字符串并去除前后空格
            # 判断是否为不合规单号
            if not tracking_no.isdigit() or not tracking_no.startswith(("92", "93", "94")) or "_" in tracking_no:
                irregular_number_map[tracking_no] = CourierStateMapValue.irregular_no_tracking

        print("find_irregular_tracking_numbers 方法执行完成")
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
    wb = openpyxl.load_workbook(filepath, data_only=True)
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
    print("update_courier_status 方法执行完成")


# 预编译正则，提高性能
date_regex = re.compile(r"\d{4}-\d{2}-\d{2}")


# 解析日期的辅助函数
def parse_date(date_str):
    match = date_regex.search(str(date_str))
    return match.group() if match else ""


def extract_and_process_data(filepath: str, column_name: str, group_size: int, wl_name=RowName.Tracking_No,
                             request_interval: float = 2.0):
    print("extract_and_process_data 方法执行开始")

    # **优化1：仅读取必要的列，减少内存占用**
    data = pd.read_excel(filepath, usecols=[column_name, wl_name], dtype=str)

    if column_name not in data.columns:
        raise ValueError(f"列 '{column_name}' 不存在于 Excel 文件中")

    # 初始化结果字典
    results_map = {
        "tracking_map": {},
        "no_tracking_map": {},
        "unpaid_map": {},
        "not_yet_map": {},
        "pre_ship_map": {},
        "delivered_map": {},
        "possession_sf_date_map": {},
        "latest_event_sf_date_map": {},
        "sf_date_equality_map": {},
    }

    # **优化2：过滤空值，减少计算量**
    data[column_name] = data[column_name].fillna('')
    valid_values = {"", "not_yet", "pre_ship", "tracking", "no_tracking"}
    filtered_data = data[data[column_name].isin(valid_values)]

    # **优化3：转换为列表，减少 Pandas 操作，提高性能**
    items = filtered_data[wl_name].dropna().tolist()

    # **优化4：使用列表推导式减少循环开销**
    grouped_items = [items[i:i + group_size] for i in range(0, len(items), group_size)]

    last_request_time = time.time()
    print(f"提取到 {len(items)} 条数据，分成 {len(grouped_items)} 组")

    # **优化5：限制最大线程数，防止 CPU 过载**
    max_threads = min(5, len(grouped_items))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(track, group): (idx, group) for idx, group in enumerate(grouped_items)}

        for future in concurrent.futures.as_completed(futures):
            idx, group = futures[future]

            # **优化6：控制请求频率，减少 API 压力**
            elapsed_time = time.time() - last_request_time
            if elapsed_time < request_interval:
                time.sleep(request_interval - elapsed_time)
            last_request_time = time.time()

            try:
                track1 = future.result()  # **优化7：及时释放 future 结果，减少内存占用**
                print(f"处理第 {idx + 1} 组，共 {len(group)} 条数据")

                for package_id, info in track1['data'].items():
                    if info.get('err'):
                        err_id = info.get('err_id')
                        if err_id == '-2147219283':
                            results_map["not_yet_map"][package_id] = "not_yet"
                        elif err_id == 'pre-ship':
                            results_map["pre_ship_map"][package_id] = "pre_ship"
                        else:
                            results_map["no_tracking_map"][package_id] = "no_tracking"

                        # **优化8：避免存储空字符串**
                        results_map["possession_sf_date_map"][package_id] = None
                        results_map["latest_event_sf_date_map"][package_id] = None
                        results_map["sf_date_equality_map"][package_id] = 0
                    else:
                        status_category = info.get('statusCategory', '')
                        status_long = info.get('statusLong', '')

                        if "postage" in status_long:
                            results_map["unpaid_map"][package_id] = "unpaid"
                        elif "Delivered" in status_category or "Delivered to Agent" in status_category:
                            results_map["delivered_map"][package_id] = "delivered"
                        else:
                            results_map["tracking_map"][package_id] = "tracking"

                        # **优化9：解析日期并计算时间差**
                        possession_date = parse_date(info.get("possessionSfDateTime"))
                        latest_event_date = parse_date(info.get("latestEventSfDateTime"))

                        if possession_date and latest_event_date:
                            days_diff = (datetime.strptime(latest_event_date, "%Y-%m-%d") -
                                         datetime.strptime(possession_date, "%Y-%m-%d")).days
                        else:
                            days_diff = 0

                        # **优化10：特殊处理 USPS 物流**
                        if days_diff == 0 and info.get("statusShort") == 'Arrived at USPS Regional Origin Facility':
                            days_diff = 99

                        results_map["possession_sf_date_map"][package_id] = possession_date
                        results_map["latest_event_sf_date_map"][package_id] = latest_event_date
                        results_map["sf_date_equality_map"][package_id] = int(days_diff)

            except Exception as e:
                print(f"处理组 {idx + 1} 时发生错误: {e}")

    print("extract_and_process_data 方法执行完成")
    return results_map


def count_pattern_and_tracking_with_sf_date(file_path, column_name, sfDateInterval_name, patterns):
    """
    统计指定列中多个正则表达式匹配内容的数量，并统计 "Courier/快递" 列内容为 'tracking' 且 "SfDateEquality" 列的内容为 0 的行数。

    :param file_path: Excel 文件路径
    :param column_name: 需要统计的列名
    :param patterns: 正则表达式字典，key 为模式名称，value 为模式字符串
    :return: 包含每个模式匹配计数和符合 'tracking' 且 'SfDateEquality' 为 0 的行数的字典
    """
    try:
        workbook = load_workbook(file_path, data_only=True)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]

        # 检查列名是否存在
        if column_name not in headers or sfDateInterval_name not in headers:
            raise ValueError(f"Excel 文件中未找到 '{column_name}' 或 '{sfDateInterval_name}'列 找不到")

        # 获取列索引
        column_index = headers.index(column_name)
        sfDateInterval_index = headers.index(sfDateInterval_name)

        # 编译所有正则表达式
        compiled_patterns = {key: re.compile(pattern, re.IGNORECASE) for key, pattern in patterns.items()}

        # 初始化计数器
        count_dict = {**{key: 0 for key in patterns}, "sfDateInterval": 0}  # 显式初始化
        tracking_sf_date_equality_count = 0

        # 遍历每一行数据
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            courier_value = row[column_index]
            sfDateInterval_value = row[sfDateInterval_index]

            # 判断是否符合 'tracking' 且 'SfDateEquality' 为 0 的条件
            if courier_value == "tracking" and sfDateInterval_value == 0:
                tracking_sf_date_equality_count += 1

            # 判断正则表达式匹配
            if courier_value is not None:
                cell_value_str = str(courier_value)
                for key, pattern in compiled_patterns.items():
                    if pattern.search(cell_value_str):
                        count_dict[key] += 1

        # 将 'tracking' 且 'SfDateEquality' 为 0 的计数添加到字典中
        count_dict["sfDateInterval"] = tracking_sf_date_equality_count

        return count_dict

    except Exception as e:
        print(f"发生错误: {e}")
        # 返回一个包含所有模式及 'tracking_sf_date_equality' 键的字典
        return {key: 0 for key in patterns} | {"sfDateInterval": 0}  # 合并字典


def count_distribution_and_no_track(file_path, key_column, courier_column=RowName.Courier):
    """
    通用函数，统计指定列的分布情况及其对应 "无轨迹" 的数量。
    :param file_path: Excel 文件路径
    :param key_column: 需要统计的列名
    :param courier_column: 快递列名
    :return: 各值的总数和 "无轨迹" 数量的 Counter 对象
    """
    try:
        workbook = load_workbook(file_path, data_only=True)
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


def dimension_distribution(file_path, key_column, courier_column=RowName.Courier,
                           sf_date_column=RowName.SfDateInterval):
    """
    通用函数，统计指定列的分布情况及其对应 "无轨迹" 的数量。
    :param file_path: Excel 文件路径
    :param key_column: 需要统计的列名
    :param courier_column: 快递列名
    :return: 各值的总数和 "无轨迹" 数量的 Counter 对象
    """
    try:
        workbook = load_workbook(file_path, data_only=True)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]
        if key_column not in headers or courier_column not in headers or sf_date_column not in headers:
            raise ValueError(f"列名 '{key_column}' 或 '{courier_column}' 或 '{sf_date_column}' 不存在！")

        # 获取列索引（加 1 是因为 Excel 索引从 1 开始）
        key_index = headers.index(key_column) + 1
        courier_index = headers.index(courier_column) + 1
        sf_date_index = headers.index(sf_date_column) + 1

        # 初始化计数器
        key_counter = Counter()
        key_no_track_counter = Counter()

        # 正则表达式和条件
        pattern = re.compile(Pattern.no_track, re.IGNORECASE)

        # 遍历每一行
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            key_value = row[key_index - 1]
            courier_status = row[courier_index - 1]
            sf_date_value = row[sf_date_index - 1]

            if key_value is not None:
                key_counter[key_value] += 1
                if courier_status is not None:
                    # 判断是否是 "无轨迹"
                    if pattern.search(str(courier_status)) or (courier_status == "tracking" and sf_date_value == 0):
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
        workbook = load_workbook(file_path, data_only=True)
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


def analyze_time_segments(file_path, data_map, time_column, courier_column, sf_date_column):
    """
    统计按 3 分钟为间隔的时间段数据，计算每个时间段的总数、无轨迹数，并找到最低上网率的时间段。
    """
    try:
        workbook = load_workbook(file_path, data_only=True)
        sheet = workbook.active

        # 获取表头
        headers = [cell.value for cell in sheet[1]]
        if time_column not in headers or courier_column not in headers or sf_date_column not in headers:
            raise ValueError(f"列名 '{time_column}'、'{courier_column}' 或 '{sf_date_column}' 不存在！")

        # 获取列索引
        time_index, courier_index, sf_date_index = (
            headers.index(time_column), headers.index(courier_column), headers.index(sf_date_column)
        )

        pattern_no_track = re.compile(r"(no_tracking|pre_ship|not_yet)", re.IGNORECASE)

        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            order_time, courier_status, sf_date_value = row[time_index], row[courier_index], row[sf_date_index]
            if isinstance(order_time, str):
                try:
                    order_time = datetime.strptime(order_time, "%Y-%m-%d %H:%M:%S").replace(second=0)
                    data.append((order_time, courier_status, sf_date_value))
                except ValueError:
                    continue

        data.sort(key=lambda x: x[0])  # 按时间排序
        time_segments = defaultdict(list)

        if data:
            base_time = data[0][0]  # 作为时间段起点
            for order_time, courier_status, sf_date_value in data:
                if (order_time - base_time).total_seconds() <= 180:
                    time_segments[base_time].append((order_time, courier_status, sf_date_value))
                else:
                    base_time = order_time
                    time_segments[base_time].append((order_time, courier_status, sf_date_value))

        segment_statistics = {}
        lowest_segment, lowest_swl = "", 101  # 记录最低上网率的时间段

        for segment_start, entries in time_segments.items():
            total_count = len(entries)
            no_track_count = sum(
                1 for _, courier_status, sf_date_value in entries
                if pattern_no_track.match(str(courier_status or "")) or (
                        courier_status == "tracking" and sf_date_value == 0)
            )
            segmentswl = round(100 - ((no_track_count / total_count) * 100), 2) if total_count else 0

            segment_info = f"\n{segment_start.strftime('%y-%m-%d %H:%M')} - {(segment_start + timedelta(minutes=3)).strftime('%y-%m-%d %H:%M')}：（{total_count}, {no_track_count}, {segmentswl}%）"
            segment_statistics[segment_start] = {
                "total_count": total_count,
                "no_track_count": no_track_count,
                "swl": segmentswl,
                "segment_info": segment_info
            }

            if segmentswl < lowest_swl:
                lowest_swl, lowest_segment = segmentswl, segment_info

        time_segment_text = "".join(
            stats["segment_info"] for stats in segment_statistics.values()
        )

        data_map[CellKey.time_segment_condition] = time_segment_text

        return time_segment_text, lowest_segment

    except Exception as e:
        print(f"发生错误: {e}")
        return "", ""


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
        print("check_and_add_courier_column 方法执行完成")
    except Exception as e:
        print(f"发生错误: {e}")


def get_days_difference(file_path, column_name=RowName.OutboundTime):
    try:
        workbook = load_workbook(file_path, data_only=True)
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
    report_text = []
    lowest_swl = 101  # 初始化为一个比 100 大的值，用于比较
    lowest_entity = ""  # 保存最低上网率的实体信息

    # 遍历分布数据
    for entity, count in distribution.items():
        no_track_count = no_track_distribution.get(entity, 0)
        swl = round2(100 - ((no_track_count / count) * 100))  # 计算上网率
        # 使用 f-string 格式化输出文本
        report_text.append(f"\n{entity}：({count},{swl}%)")

        # 判断是否是最低的上网率
        if swl < lowest_swl:
            lowest_swl = swl
            lowest_entity = f"\n{entity}：（{count}, {no_track_count}, {swl}%）"

    # 将结果存储到 data_map 中
    data_map[data_map_key] = "".join(report_text)  # 使用 join 合并字符串，减少内存消耗
    return "".join(report_text), lowest_entity


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
    total_count = remove_duplicates_by_column(xlsx_path, output_file, RowName.Tracking_No)

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

    count_dict = count_pattern_and_tracking_with_sf_date(output_file, RowName.Courier, RowName.SfDateInterval, patterns)

    no_track_count = count_dict["no_track"]
    delivered_count = count_dict["delivered"]
    unpaid_count = count_dict["unpaid"]
    not_yet_count = count_dict["not_yet"]
    pre_ship_count = count_dict["pre_ship"]
    irregular_no_tracking_count = count_dict["irregular_no_tracking"]
    no_tracking_count = count_dict["no_tracking"]
    tracking_count = count_dict["tracking"]
    tracking_zero_count = count_dict["sfDateInterval"]

    # 先进行一次计算，并缓存结果
    total_count_int = int(total_count)
    no_track_count_int = int(no_track_count)
    tracking_zero_count_int = int(tracking_zero_count)
    delivered_count_int = int(delivered_count)
    unpaid_count_int = int(unpaid_count)
    not_yet_count_int = int(not_yet_count)
    pre_ship_count_int = int(pre_ship_count)
    irregular_no_tracking_count_int = int(irregular_no_tracking_count)
    no_tracking_count_int = int(no_tracking_count)
    tracking_count_int = int(tracking_count)

    # 计算百分比
    swl = round2(100 - ((no_track_count_int + tracking_zero_count_int) / total_count_int * 100))
    wswl = round2(100 - swl)
    qsl = round2((delivered_count_int / total_count_int) * 100)
    unpaidl = round2((unpaid_count_int / total_count_int) * 100)
    not_yetl = round2((not_yet_count_int / total_count_int) * 100)
    pre_shipl = round2((pre_ship_count_int / total_count_int) * 100)
    irregular_no_trackingl = round2((irregular_no_tracking_count_int / total_count_int) * 100)
    no_tracking_countl = round2((no_tracking_count_int / total_count_int) * 100)
    tracking_countl = round2(((tracking_count_int - tracking_zero_count_int) / total_count_int) * 100)
    tracking_zero_countl = round2((tracking_zero_count_int / total_count_int) * 100)

    kj_counts = kj_count(output_file)

    # 构建字符串
    wl = (
        f"\n订单总数：{total_count_int}"
        f"\nKJ订单总数：{kj_counts}"
        f"\n"
        f"\n上网：（{tracking_count_int - tracking_zero_count_int}, {swl}%）"
        f"\n未上网：（{no_track_count_int + tracking_zero_count_int}, {wswl}%）"
        f"\n"
        f"\ndelivered：（{delivered_count_int}, {qsl}%）"
        f"\nunpaid：（{unpaid_count_int}, {unpaidl}%）"
        f"\ntracking：（{tracking_count_int - tracking_zero_count_int}, {tracking_countl}%）"
        f"\ntracking_zero：（{tracking_zero_count_int}, {tracking_zero_countl}%）"
        f"\nno_tracking：（{no_tracking_count_int}, {no_tracking_countl}%）"
        f"\nnot_yet：（{not_yet_count_int}, {not_yetl}%）"
        f"\npre_ship：（{pre_ship_count_int}, {pre_shipl}%）"
        f"\nirregular_no_tracking：（{irregular_no_tracking_count_int}, {irregular_no_trackingl}%）"
        f"\n{irregular_number_text + unpaid_text}"
    )
    data_map[CellKey.wl] = wl

    text += "\n----------------------轨迹概览----------------------"
    text += wl

    # 避免重复读取 Excel 文件
    warehouse_count, warehouse_no_track_count = dimension_distribution(output_file, key_column=RowName.Warehouse)
    warehouse_text, lowest_warehouse = generate_distribution_report(warehouse_count, warehouse_no_track_count,
                                                                    data_map, CellKey.warehouse_condition)
    text += "\n----------------------仓库分布----------------------" + warehouse_text

    store_count, store_no_track_count = dimension_distribution(output_file, key_column=RowName.Client)
    store_text, lowest_store = generate_distribution_report(store_count, store_no_track_count,
                                                            data_map, CellKey.store_condition)
    text += "\n----------------------店铺分布----------------------" + store_text

    shipping_service_count, shipping_service_no_track_count = dimension_distribution(output_file,
                                                                                     key_column=RowName.ShippingService)
    shipping_service_text, lowest_shipping_service = generate_distribution_report(shipping_service_count,
                                                                                  shipping_service_no_track_count,
                                                                                  data_map,
                                                                                  CellKey.shipping_service_condition)
    text += "\n----------------------物流渠道分布----------------------" + shipping_service_text

    time_segment_text, lowest_segment = analyze_time_segments(output_file, data_map,
                                                              time_column=RowName.CreationWaveTime,
                                                              courier_column=RowName.Courier,
                                                              sf_date_column=RowName.SfDateInterval)

    text += "\n----------------------时间段分布----------------------" + time_segment_text

    lowest_txt = "\n"
    if lowest_sku:
        lowest_txt += "\n最低上网率的 SKU：" + "".join(lowest_sku)
    lowest_txt += f"""
    最低上网率的 仓库：{lowest_warehouse}
    最低上网率的 商店：{lowest_store}
    最低上网率的 时间段：{lowest_segment}
    最低上网率的 物流渠道：{lowest_shipping_service}
    """

    sum_up_text = ""
    actual_interval = ""
    if is_usweekend == 6:  # 6是中国周日，美国周六
        sum_up_text = "美国时间：周六（和中国相差13-16个小时）\n"
        actual_interval = "（-2）"
    elif is_usweekend == 0:  # 0是中国周一，美国周日
        sum_up_text = "美国时间：周日（相差13-16个小时）\n"
        actual_interval = "（-1）"

    # if (len(irregular_number_list) > 0):
    #     sum_up_text += f"存在不规则单号：{irregular_number_list}"
    #     sum_up_text += f"\n"

    swl_flag = False
    qsl_flag = False
    bg = "#ffffff"

    # 上网率判断
    warning_levels = [
        (0, 30, "☁️注意", "未达30%，建议跟进！", "#F8F1D3"),
        (1, 70, "🌧️异常", "未达75%，建议分析数据尝试定位问题！", "#E3C49C"),
        (3, 97, "❄️⛈️🌀⚠️🚨警报", "未达97%，分析数据反馈问题！", "#F1C1BD"),
    ]

    sum_up_text += f"\n间隔第{interval_time}{actual_interval}天，上网率为{swl}%"

    for days, threshold, icon, message, color in warning_levels:
        if interval_time == days and swl < threshold:
            sum_up_text += f"\n{icon} {message}"
            swl_flag = True
            bg = color
            break
    else:
        sum_up_text += "，上网率优秀"

    # 签收率判断
    qsl_warnings = [
        (1, 3, 0, "🚨警报", "签收率为0%，异常状态！"),
        (3, 5, 20, "🚨警报", "签收率未达20%，异常状态！"),
        (5, 7, 50, "🚨警报", "签收率未达50%，异常状态！"),
        (7, 9, 80, "🚨警报", "签收率未达80%，异常状态！"),
    ]

    for start, end, threshold, icon, message in qsl_warnings:
        if start <= interval_time <= end and qsl <= threshold:
            sum_up_text += f"\n{icon} {message}"
            qsl_flag = True
            break
    else:
        sum_up_text += f"\n☀️间隔第{interval_time}{actual_interval}天，签收率为{qsl}%，继续跟进！"

    if interval_time > 9 and qsl >= 98:
        sum_up_text += f"\n☀️间隔第{interval_time}{actual_interval}天，签收率为{qsl}%，签收率优秀！"

    text += "\n----------------------总结&建议----------------------"
    if swl < 100:
        sum_up_text += lowest_txt
    text += f"\n{sum_up_text}"
    data_map[CellKey.sum_up] = sum_up_text

    # 异常状态记录
    if swl_flag or qsl_flag:
        if swl_flag and qsl_flag:
            data_map[CellKey.exception] = "上网率&签收率 异常\n（签收率目前无法量化，只为提醒⏰）"
        elif swl_flag:
            data_map[CellKey.exception] = "上网率异常"
        elif qsl_flag:
            data_map[CellKey.exception] = "签收率异常\n（签收率目前无法量化，只为提醒⏰）"
    else:
        data_map[CellKey.exception] = ""

    # 删除去重文件
    delete_file(output_file)
    print(text)

    # 写入飞书在线文档
    # tat = get_token()
    # if analyse_obj == ClientConstants.zbw or analyse_obj == ClientConstants.sanrio or analyse_obj == ClientConstants.xyl:
    #     lists = f"({total_count},{swl}%)"
    #     lists += f"\n{warehouse_text}"
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
        pattern = r"^创建时间\d+_\d+\.xlsx$"  # 正则表达式
        for ele in files:
            if re.match(pattern, ele):
                xlsx_path = f"{root}/{ele}"
                print(f"匹配的文件: {xlsx_path}")
                try:
                    # total_count, no_track_count = count_pattern_state(xlsx_path, RowName.Courier, Pattern.no_track)
                    # tracking_zero_count = count_tracking_with_sf_date_equality(xlsx_path)
                    # total_count2, delivered_count = count_pattern_state(xlsx_path, RowName.Courier, Pattern.delivered)
                    #
                    # if total_count == 0:
                    #     swl = 0
                    # else:
                    #     swl = round2(100 - ((int(no_track_count + tracking_zero_count) / int(total_count)) * 100))
                    #
                    # if total_count == 0:
                    #     qsl = 0
                    # else:
                    #     qsl = round2((int(delivered_count) / int(total_count)) * 100)
                    #
                    # if swl < 99 or qsl < 98:
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
    go(ClientConstants.zbw, "/Users/zkp/Desktop/B&Y/轨迹统计/zbw/2025.3/创建时间1_846.xlsx")
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
