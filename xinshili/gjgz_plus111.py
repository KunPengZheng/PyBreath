from datetime import datetime, date, timedelta
import os
import re
from openpyxl import load_workbook
import openpyxl
import pandas as pd
from collections import Counter, defaultdict
from dataclasses import dataclass

from xinshili.fs_utils_plus import get_token, brief_sheet_value, detail_sheet_value
from xinshili.usps_utils import track
from xinshili.utils import round2, getYmd
import random
import time

"""
zbw轨迹跟踪分析
"""


@dataclass(frozen=True)
class RowName:
    Tracking_No = 'Tracking No./物流跟踪号'
    Courier = 'Courier/快递'
    OutboundTime = "OutboundTime/出库时间"


@dataclass(frozen=True)
class CourierStateMapKey:
    tracking_results = 'tracking_results'
    no_tracking_results = 'no_tracking_results'
    unpaid_results = "unpaid_results"
    not_yet_results = "not_yet_results"
    pre_ship_results = "pre_ship_results"
    delivered_results = "delivered_results"
    out_of_delivery_results = "out_of_delivery_results"
    irregular_order_number_results = "irregular_order_number_results"
    returned_to_sender_results = "returned_to_sender_results"


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


def update_courier_status_for_results(filepath, maps):
    wb = openpyxl.load_workbook(filepath)
    sheet = wb.active  # 默认使用活动工作表

    data = pd.read_excel(filepath)
    # 获取 'Tracking No./物流跟踪号' 列和 'Courier/快递' 列的索引
    tracking_no_col = data.columns.get_loc(RowName.Tracking_No) + 1  # openpyxl索引从1开始
    courier_col = data.columns.get_loc(RowName.Courier) + 1  # openpyxl索引从1开始

    for tracking_no, status in maps.items():
        for row in range(2, sheet.max_row + 1):  # 从第二行开始（跳过表头）
            # 获取当前行的物流跟踪号
            current_tracking_no = sheet.cell(row=row, column=tracking_no_col).value
            # 如果找到匹配的物流跟踪号，更新 Courier/快递 列
            if current_tracking_no == tracking_no:
                sheet.cell(row=row, column=courier_col, value=status)
                break  # 找到后退出循环，避免重复更新同一行

    # 保存更新后的文件
    wb.save(filepath)


def extract_and_process_data(filepath, column_name, group_size):
    data = pd.read_excel(filepath)

    if column_name not in data.columns:
        raise ValueError(f"列 '{column_name}' 不存在于 Excel 文件中")

    # 存储结果的 map（字典）
    results_map = {
        CourierStateMapKey.tracking_results: {},
        CourierStateMapKey.no_tracking_results: {},
        CourierStateMapKey.unpaid_results: {},
        CourierStateMapKey.not_yet_results: {},
        CourierStateMapKey.pre_ship_results: {},
        CourierStateMapKey.delivered_results: {},
        CourierStateMapKey.out_of_delivery_results: {},
        CourierStateMapKey.irregular_order_number_results: {},
        CourierStateMapKey.returned_to_sender_results: {}
    }

    # 不规则的快递单号不需要跟踪
    for tracking_number in data[RowName.Tracking_No]:
        if not str(tracking_number).isdigit() or not str(tracking_number).startswith('9'):
            results_map[CourierStateMapKey.irregular_order_number_results][
                tracking_number] = CourierStateMapValue.irregular_no_tracking
    update_courier_status_for_results(filepath, results_map[CourierStateMapKey.irregular_order_number_results])

    data[column_name] = data[column_name].fillna('')

    filtered_data = data[
        data[column_name].apply(
            lambda x: str(x).strip().lower() in ['',
                                                 CourierStateMapValue.not_yet,
                                                 CourierStateMapValue.pre_ship,
                                                 CourierStateMapValue.no_tracking])]

    # 提取符合条件的 'Tracking No./物流跟踪号' 列数据
    items = filtered_data[RowName.Tracking_No].tolist()

    # 按组划分数据
    grouped_items = [items[i:i + group_size] for i in range(0, len(items), group_size)]

    # 请求每组数据
    for idx, group in enumerate(grouped_items, start=1):
        print(f"处理第 {idx} 组，共 {len(group)} 条数据")
        track1 = track(group)  # 假设track是查询API的函数

        for package_id, info in track1['data'].items():
            # 判断错误类型并分类
            if info.get('err'):
                if info.get('err_id') == '-2147219283':  # 无轨迹(Label Created, not yet in system)
                    results_map[CourierStateMapKey.not_yet_results][package_id] = CourierStateMapValue.not_yet
                elif info.get('err_id') == 'pre-ship':  # 无轨迹(pre-ship)
                    results_map[CourierStateMapKey.pre_ship_results][package_id] = CourierStateMapValue.pre_ship
                else:
                    results_map[CourierStateMapKey.no_tracking_results][package_id] = CourierStateMapValue.no_tracking
            else:
                if "The package associated with this tracking number did not have proper postage applied and will not be delivered" in \
                        info.get('statusLong'):
                    results_map[CourierStateMapKey.unpaid_results][package_id] = CourierStateMapValue.unpaid
                elif "Delivered" in info.get('statusCategory'):
                    results_map[CourierStateMapKey.delivered_results][package_id] = CourierStateMapValue.delivered
                elif "Delivered to Agent" in info.get('statusCategory'):
                    results_map[CourierStateMapKey.delivered_results][package_id] = CourierStateMapValue.delivered
                else:
                    results_map[CourierStateMapKey.tracking_results][package_id] = CourierStateMapValue.tracking

    # 输出结果统计
    # print(
    #     f"没有轨迹数： {len(results_map['no_tracking_results'])} 条，有轨迹数： {len(results_map['tracking_results'])} 条")
    # print(f"\nunpaid数： {len(results_map['unpaid_results'])} 条")
    # print(f"\nnot_yet数： {len(results_map['not_yet_results'])} 条")
    # print(f"\npre_ship数： {len(results_map['pre_ship_results'])} 条")
    # print(f"\ndelivered数： {len(results_map['delivered_results'])} 条")

    return results_map


def count_delivered(file_path, column_name):
    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]
        if column_name not in headers:
            raise ValueError(f"列名 '{column_name}' 不存在！")
        column_index = headers.index(column_name) + 1
        pattern = re.compile(r"delivered", re.IGNORECASE)
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


def count_no_track(file_path, column_name):
    """统计 '快递' 列中所有行数和内容为 '无轨迹' 的数量"""
    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]
        if column_name not in headers:
            raise ValueError(f"列名 '{column_name}' 不存在！")
        column_index = headers.index(column_name) + 1
        pattern = re.compile(r"not_yet|pre_ship|irregular_no_tracking|no_tracking", re.IGNORECASE)
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
        pattern = re.compile(r"not_yet|pre_ship|irregular_no_tracking|no_tracking", re.IGNORECASE)
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


def analyze_time_segments(file_path, time_column, courier_column):
    """
    按时间段（每3分钟为一段，忽略秒进行判断）统计总数和 "无轨迹" 的数量。
    输出时包括秒显示。
    """
    try:
        # 加载 Excel 文件
        workbook = load_workbook(file_path)
        sheet = workbook.active

        # 获取表头
        headers = [cell.value for cell in sheet[1]]
        if time_column not in headers or courier_column not in headers:
            raise ValueError(f"列名 '{time_column}' 或 '{courier_column}' 不存在！")

        # 获取列索引
        time_index = headers.index(time_column) + 1
        courier_index = headers.index(courier_column) + 1

        # 正则表达式匹配 "无轨迹"
        pattern = re.compile(r"not_yet|pre_ship|irregular_no_tracking|no_tracking", re.IGNORECASE)

        # 读取并解析数据
        data = []
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            order_time = row[time_index - 1]
            courier_status = row[courier_index - 1]
            if order_time is not None and isinstance(order_time, str):
                try:
                    # 解析时间格式为 "2025-01-22 23:11:43"
                    order_time = datetime.strptime(order_time, "%Y-%m-%d %H:%M:%S")
                    order_time_without_seconds = order_time.replace(second=0)
                    data.append((order_time, order_time_without_seconds, courier_status))
                except ValueError:
                    continue

        # 按时间段归类
        data.sort(key=lambda x: x[1])  # 按无秒时间排序
        time_segments = defaultdict(list)
        if data:
            base_time = data[0][1]  # 使用无秒时间作为基准
            current_segment = []
            for full_time, order_time_without_seconds, courier_status in data:
                if (order_time_without_seconds - base_time).total_seconds() <= 180:  # 3分钟内
                    current_segment.append((full_time, courier_status))
                else:
                    time_segments[base_time].extend(current_segment)
                    base_time = order_time_without_seconds
                    current_segment = [(full_time, courier_status)]
            if current_segment:
                time_segments[base_time].extend(current_segment)

        # 统计每个时间段的总数和无轨迹数量
        segment_statistics = {}
        for segment_start, entries in time_segments.items():
            total_count = len(entries)
            no_track_count = sum(
                1 for _, courier_status in entries if courier_status is not None and pattern.match(str(courier_status)))
            segment_statistics[segment_start] = {
                "total_count": total_count,
                "no_track_count": no_track_count,
                "entries": entries,
            }

        return segment_statistics

    except Exception as e:
        print(f"发生错误: {e}")
        return {}


def check_and_add_courier_column(file_path, courier_column=RowName.Courier):
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
        if courier_column not in data.columns:
            # 如果没有 '快递' 列，则在最后一列添加该列
            data[courier_column] = ""  # 默认为空值，可以根据需求填充其他默认值
            # 保存修改后的文件
            data.to_excel(file_path, index=False, engine='openpyxl')
            print(f"列 '{courier_column}' 已添加到文件中，并保存。")
        else:
            print(f"列 '{courier_column}' 已存在，无需添加。")
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


def remove_duplicates_by_column(input_file, output_file, column_name):
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
        df_deduplicated.to_excel(output_file, index=False)
    except Exception as e:
        print(f"处理文件时发生错误：{e}")


analyse_obj = input("请输跟踪对象（zbw/sanrio）：")
xlsx_path = input("请输入文件的绝对路径：")
check_and_add_courier_column(xlsx_path)
results = extract_and_process_data(xlsx_path, RowName.Courier, 100)

update_courier_status_for_results(xlsx_path, results[CourierStateMapKey.not_yet_results])
update_courier_status_for_results(xlsx_path, results[CourierStateMapKey.pre_ship_results])
update_courier_status_for_results(xlsx_path, results[CourierStateMapKey.unpaid_results])
update_courier_status_for_results(xlsx_path, results[CourierStateMapKey.delivered_results])
update_courier_status_for_results(xlsx_path, results[CourierStateMapKey.no_tracking_results])
update_courier_status_for_results(xlsx_path, results[CourierStateMapKey.tracking_results])

ck_time = get_days_difference(xlsx_path)
gz_time = getYmd()
interval_time = (datetime.strptime(gz_time, "%Y/%m/%d") - datetime.strptime(ck_time, "%Y/%m/%d")).days

# 数据map
data_map = {}

text = ""

text += "\n----------------------sku分布----------------------"
sku_distribution, sku_no_track_distribution = count_distribution_and_no_track(
    xlsx_path, key_column="SKU"
)
# print("\nSKU 分布及对应的 '无轨迹' 情况：")
sku_text = ""
lowest_sku = ""
lowest_swl = 101  # 初始化为比 100 大的值
for sku, count in sku_distribution.items():
    no_track_count = sku_no_track_distribution[sku]
    skuswl = round2(100 - ((int(no_track_count) / int(count)) * 100))
    # print(f"{sku}: 总数 {count} 条，其中 '无轨迹' {no_track_count} 条，上网率为：{skuswl}%")
    text += f"\n{sku}： 订单总数：{count}；无轨迹数：{no_track_count}；上网率：{skuswl}%"
    sku_text += f"\n{sku}： 订单总数：{count}；无轨迹数：{no_track_count}；上网率：{skuswl}%"
    # 判断是否是最低的上网率
    if skuswl < lowest_swl:
        lowest_swl = skuswl
        lowest_sku = f"{sku}： 订单总数：{count}；无轨迹数：{no_track_count}；上网率：{skuswl}%"
# 将 sku_text 保存到 data_map
data_map[CellKey.sku_condition] = sku_text

output_file = os.path.splitext(xlsx_path)[0] + "_去重.xlsx"
# 需要去重复
remove_duplicates_by_column(xlsx_path, output_file, "Tracking No./物流跟踪号")

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
text += "\n----------------------时间----------------------"
text += f"\n更新时间: {current_time}"
data_map[CellKey.update_time] = current_time

text += f"\n出库日期：{ck_time}"
text += f"\n跟踪日期：{gz_time}"
text += f"\n间隔时间：{interval_time}"

total_count, no_track_count = count_no_track(output_file, column_name="Courier/快递")
total_count2, delivered_count = count_delivered(output_file, column_name="Courier/快递")

qsl = round2((int(delivered_count) / int(total_count)) * 100)
swl = round2(100 - ((int(no_track_count) / int(total_count)) * 100))
# print(f"总条数（除列头）：{total_count}，内容为 '无轨迹' 的总数：{no_track_count}，上网率为：{swl}%")
text += "\n----------------------概览----------------------"
text += f"\n订单总数：{total_count}"
text += f"\n签收数：{delivered_count}"
text += f"\n签收率：{qsl}%"
text += f"\n未上网数：{no_track_count}"
text += f"\n上网率：{swl}%"
text += f"\n未上网率：{100 - swl}%"

data_map[CellKey.order_count] = total_count
data_map[CellKey.no_track_number] = no_track_count
data_map[CellKey.track_percent] = swl
data_map[CellKey.no_track_percent] = 100 - swl
data_map[CellKey.delivered_counts] = delivered_count
data_map[CellKey.delivered_percent] = qsl

text += "\n----------------------仓库分布----------------------"
warehouse_distribution, warehouse_no_track = count_distribution_and_no_track(
    output_file, key_column="Warehouse/仓库"
)
# print("\n发货仓库分布情况：")
warehouse_text = ""
lowest_swl = 101  # 初始化为比 100 大的值
lowest_warehouse = ""  # 保存最低上网率的仓库信息
for warehouse, count in warehouse_distribution.items():
    no_track_count = warehouse_no_track[warehouse]
    warehouseswl = round2(100 - ((int(no_track_count) / int(count)) * 100))
    # print(f"{warehouse}: 总数 {count} 条，其中 '无轨迹' {no_track_count} 条，上网率为：{warehouseswl}%")
    text += f"\n{warehouse}： 订单总数：{count}；无轨迹数：{no_track_count}；上网率：{warehouseswl}%"
    warehouse_text += f"\n{warehouse}： 订单总数：{count}；无轨迹数：{no_track_count}；上网率：{warehouseswl}%"
    # 判断是否是最低的上网率
    if warehouseswl < lowest_swl:
        lowest_swl = warehouseswl
        lowest_warehouse = f"{warehouse}： 订单总数：{count}；无轨迹数：{no_track_count}；上网率：{warehouseswl}%"
data_map[CellKey.warehouse_condition] = warehouse_text

text += "\n----------------------店铺分布----------------------"
store_distribution, store_no_track_distribution = count_distribution_and_no_track(
    output_file, key_column="Client/客户"
)
# print("\n店铺分布及对应的 '无轨迹' 情况：")
store_text = ""
lowest_store = ""
lowest_swl = 101  # 初始化为一个比 100 大的值，用于比较
for store, count in store_distribution.items():
    no_track_count = store_no_track_distribution[store]
    storeswl = round2(100 - ((int(no_track_count) / int(count)) * 100))
    # print(f"{store}: 总数 {count} 条，其中 '无轨迹' {no_track_count} 条，上网率为：{storeswl}%")
    text += f"\n{store}： 订单总数：{count}；无轨迹数：{no_track_count}；上网率：{storeswl}%"
    store_text += f"\n{store}： 订单总数：{count}；无轨迹数：{no_track_count}；上网率：{storeswl}%"
    # 判断是否是最低的上网率
    if storeswl < lowest_swl:
        lowest_swl = storeswl
        lowest_store = f"{store}： 订单总数：{count}；无轨迹数：{no_track_count}；上网率：{storeswl}%"
data_map[CellKey.store_condition] = store_text

# 分析时间段
text += "\n----------------------时间段分布----------------------"
time_segment_analysis = analyze_time_segments(
    output_file, time_column="Creation time/创建时间", courier_column="Courier/快递"
)
# print("\n按时间段统计结果：")
time_segment_text = ""
lowest_segment = ""  # 保存上网率最低的时间段
lowest_swl = 101  # 初始化为比 100 大的值
for segment_start, stats in time_segment_analysis.items():
    segment_end = segment_start + timedelta(minutes=3)
    total_count = stats["total_count"]
    no_track_count = stats["no_track_count"]
    segmentswl = round2(100 - ((int(no_track_count) / int(total_count)) * 100))
    # print(f"时间段 {segment_start.strftime('%m-%d %H:%M:%S')} - {segment_end.strftime('%m-%d %H:%M:%S')}:")
    # print(f"  总数: {total_count} 条, 其中 '无轨迹': {no_track_count} 条，上网率为：{segmentswl}%")

    text += f"\n{segment_start.strftime('%y-%m-%d %H:%M')} - {segment_end.strftime('%y-%m-%d %H:%M')}： 订单总数：{total_count}；无轨迹数：{no_track_count}；上网率：{segmentswl}%"
    time_segment_text += f"\n{segment_start.strftime('%y-%m-%d %H:%M')} - {segment_end.strftime('%y-%m-%d %H:%M')}： 订单总数：{total_count}；无轨迹数：{no_track_count}；上网率：{segmentswl}%"
    # 判断是否是最低的上网率
    if segmentswl < lowest_swl:
        lowest_swl = segmentswl
        lowest_segment = f"{segment_start.strftime('%y-%m-%d %H:%M')} - {segment_end.strftime('%y-%m-%d %H:%M')}： 订单总数：{total_count}；无轨迹数：{no_track_count}；上网率：{segmentswl}%"
data_map[CellKey.time_segment_condition] = time_segment_text

lowest_txt = ""
lowest_txt += f"\n最低上网率的 仓库：{lowest_warehouse}"
lowest_txt += f"\n最低上网率的 SKU：{lowest_sku}"
lowest_txt += f"\n最低上网率的 商店：{lowest_store}"
lowest_txt += f"\n最低上网率的 时间段：{lowest_segment}"

sum_up_text = ""
# 如果三天后的上网率没有99%以上，那么就严重有问题；隔天应该要 》= 三分之一，隔两天应该要有》=75
if (interval_time == 1):
    if (swl < 30):
        sum_up_text += f"☁️注意：间隔第1天，上网率为{swl}，未达30%，建议跟进！"
        sum_up_text += lowest_txt
    else:
        if (swl >= 50):
            sum_up_text += f"☀️间隔第1天，上网率为{swl}，上网率优秀"
        else:
            sum_up_text += f"☀️间隔第1天，上网率为{swl}，上网率良好"
elif (interval_time == 2):
    if (swl < 70):
        sum_up_text += f"🌧️异常：间隔第2天，上网率为{swl}，未达75%，建议分析数据尝试定位问题！"
        sum_up_text += lowest_txt
    else:
        if (swl >= 85):
            sum_up_text += f"☀️间隔第2天，上网率为{swl}，上网率优秀"
        else:
            sum_up_text += f"☀️间隔第2天，上网率为{swl}，上网率良好"
else:
    if (swl < 95):
        sum_up_text += f"❄️⛈️🌀⚠️🚨警报：间隔第{interval_time}天，上网率为{swl}，未达95%，分析数据反馈问题！"
        sum_up_text += lowest_txt
    else:
        if (swl >= 99):
            sum_up_text += f"☀️间隔第{interval_time}天，上网率为{swl}，上网率优秀"
        else:
            sum_up_text += f"☀️间隔第{interval_time}天，上网率为{swl}，上网率良好"

# 要持续监控一个星期才行，从出库开始计算，三天内没有签收的不正常，五天内签收没达到50%也不正常，7天内没到90也不正常
if (interval_time == 3):
    if (qsl == 0):
        sum_up_text += f"\n🚨警报：间隔第{interval_time}天，签收率为0%，异常状态！"
    else:
        sum_up_text += f"\n间隔第{interval_time}天，签收率为{qsl}%，继续跟进！"
elif (interval_time == 5):
    if (qsl < 50):
        sum_up_text += f"\n🚨警报：间隔第{interval_time}天，签收率为{qsl}%，异常状态！"
    else:
        sum_up_text += f"\n间隔第{interval_time}天，签收率为{qsl}%，继续跟进！"
elif (interval_time == 7):
    if (qsl < 90):
        sum_up_text += f"\n🚨警报：间隔第{interval_time}天，签收率为{qsl}%，异常状态！"
    else:
        sum_up_text += f"\n间隔第{interval_time}天，签收率为{qsl}%，继续跟进！"
else:
    sum_up_text += f"\n间隔第{interval_time}天，签收率为{qsl}%，继续跟进！"

data_map[CellKey.sum_up] = sum_up_text
text += "\n----------------------总结&建议----------------------"
text += f"\n{sum_up_text}"

# 数据打印
# print(data_map)
print(text)

# 写入飞书在线文档
# tat = get_token()
# brief_sheet_value(tat, [swl], ck_time, gz_time, analyse_obj)
# detail_sheet_value(tat, [
#     data_map[CellKey.update_time],
#     data_map[CellKey.order_count],
#     data_map[CellKey.delivered_counts],
#     data_map[CellKey.delivered_percent],
#     data_map[CellKey.no_track_number],
#     data_map[CellKey.track_percent],
#     data_map[CellKey.no_track_percent],
#     data_map[CellKey.warehouse_condition],
#     data_map[CellKey.store_condition],
#     data_map[CellKey.sku_condition],
#     data_map[CellKey.time_segment_condition],
#     data_map[CellKey.sum_up],
# ], ck_time, analyse_obj)
