import requests
import json
import pandas as pd

from xinshili.utils import get_days_in_current_month, day_of_month

app_id = "cli_a71b49e8b4aad013"
app_secret = "7L9WNS6YWwQNVUN3iEtQKgb8BoQSJRzn"


def map_numbers_to_excel_columns(start, end):
    """
    将一个范围内的数字映射为 Excel 列名，从 B 开始。

    参数:
    - start: int，起始数值。
    - end: int，结束数值。

    返回:
    - dict，键为数字，值为对应的 Excel 列名。
    """
    # 从 B 开始偏移
    start_column_index = 2  # B 是第 2 列
    mapping = {}

    for number in range(start, end + 1):
        excel_column_index = start_column_index + number - 1
        column_name = ""

        while excel_column_index > 0:
            excel_column_index -= 1
            column_name = chr(excel_column_index % 26 + ord('A')) + column_name
            excel_column_index //= 26

        mapping[number] = column_name

    return mapping


def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    # 应用凭证里的 app id 和 app secret
    post_data = {"app_id": app_id, "app_secret": app_secret}
    r = requests.post(url, data=post_data)
    tat = r.json()["tenant_access_token"]  # token
    print(f"token:{tat}")
    return tat


def detail_sheet_value(tat, lists, ck_time, analyse_obj):
    """
    写入数据到 飞书 zbw轨迹跟踪2025.1 表的 详sheet
    """
    # values_prepend:它会在指定位置上方新增一行，而不是直接覆盖现有数据; values:若指定范围内已有数据，将被新写入的数据覆盖。
    # BGrnsxMFfhfoumtUDF8cXM8jnGg：表格地址中?前面的部分，表示该文档
    url = ""
    if analyse_obj == "zbw":
        url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/BGrnsxMFfhfoumtUDF8cXM8jnGg/values"
    elif analyse_obj == "sanrio":
        url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/TZQ8s1r1GhihRstNl5kco7xlnsf/values"
    else:
        raise ValueError(f"{analyse_obj} 未定义")
    header = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(tat)}  # 请求头
    # 因为首行是行头，所以表格中的出库时间所在行为：出库时间+1
    map_sheet_ck_time = str(int(ck_time) + 1)
    post_data = None
    if analyse_obj == "zbw":
        post_data = {"valueRange": {"range": f"JZrQj9!B{map_sheet_ck_time}:M{map_sheet_ck_time}", "values": [lists]}}
    elif analyse_obj == "sanrio":
        post_data = {"valueRange": {"range": f"wGMg6A!B{map_sheet_ck_time}:M{map_sheet_ck_time}", "values": [lists]}}
    else:
        raise ValueError(f"{analyse_obj} 未定义")
    # values_prepend 需要使用post请求方式，values需要使用put请求方式
    r2 = requests.put(url, data=json.dumps(post_data), headers=header)  # 请求写入
    print(r2.json())  # 输出来判断写入是否成功


def brief_sheet_value(tat, lists, ck_time, analyse_obj):
    # values_prepend:它会在指定位置上方新增一行，而不是直接覆盖现有数据; values:若指定范围内已有数据，将被新写入的数据覆盖。
    # BGrnsxMFfhfoumtUDF8cXM8jnGg：表格地址中?前面的部分，表示该文档
    url = ""
    if analyse_obj == "zbw":
        url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/BGrnsxMFfhfoumtUDF8cXM8jnGg/values"
    elif analyse_obj == "sanrio":
        url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/TZQ8s1r1GhihRstNl5kco7xlnsf/values"
    else:
        raise ValueError(f"{analyse_obj} 未定义")
    header = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(tat)}  # 请求头
    result = map_numbers_to_excel_columns(1, get_days_in_current_month())
    today = result[day_of_month()]  #
    # 因为首行是行头，所以表格中的出库时间所在行为：出库时间+1
    map_sheet_ck_time = str(int(ck_time) + 1)
    # JZrQj9：表格地址中 ?sheet= 后面的部分，表示表的名字
    post_data = None
    if analyse_obj == "zbw":
        post_data = {
            "valueRange": {"range": f"fa00e1!{today}{map_sheet_ck_time}:{today}{map_sheet_ck_time}", "values": [lists]}}
    elif analyse_obj == "sanrio":
        post_data = {
            "valueRange": {"range": f"48d357!{today}{map_sheet_ck_time}:{today}{map_sheet_ck_time}", "values": [lists]}}
    else:
        raise ValueError(f"{analyse_obj} 未定义")
    # values_prepend 需要使用post请求方式，values需要使用put请求方式
    r2 = requests.put(url, data=json.dumps(post_data), headers=header)  # 请求写入
    print(r2.json())  # 输出来判断写入是否成功


def order_sheet_value(tat, lists, position):
    """
    写入数据到 飞书 2025订单数据分析（以出库时间为筛选条件） 表的 1月sheet
    """
    # values_prepend:它会在指定位置上方新增一行，而不是直接覆盖现有数据; values:若指定范围内已有数据，将被新写入的数据覆盖。
    # BGrnsxMFfhfoumtUDF8cXM8jnGg：表格地址中?前面的部分，表示该文档
    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/QeR8sB3Pkhieswtac5kcTxHkngc/values"
    header = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(tat)}  # 请求头
    # JZrQj9：表格地址中 ?sheet= 后面的部分，表示表的名字
    post_data = {
        "valueRange": {"range": f"6a545c!B{position}:AL{position}", "values": [lists]}}
    # values_prepend 需要使用post请求方式，values需要使用put请求方式
    r2 = requests.put(url, data=json.dumps(post_data), headers=header)  # 请求写入
    print(r2.json())  # 输出来判断写入是否成功


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

def get_column_for_specific_date(target_date, start_date="2025/1/1", start_column="B"):
    """
    根据目标日期（例如：2025年1月1日），自动查找目标日期对应的列，起始日期为指定列。

    参数：
    - target_date: str, 目标日期（格式：YYYY/MM/DD）
    - start_date: str, 起始日期（默认为2025年1月1日，格式：YYYY/MM/DD）
    - start_column: str, 起始日期对应的列名（默认为"B"）

    返回：
    - 对应日期的列名


    示例使用：
    target_date = '2025/4/30'  # 目标日期，格式：YYYY/MM/DD
    column = get_column_for_specific_date(target_date)

    if column:
        print(f"目标日期 {target_date} 对应的列是：{column}")
    else:
        print(f"没有找到目标日期 {target_date} 对应的列")

    """
    # 将字符串日期转换为 datetime 对象
    start_date = pd.to_datetime(start_date)
    target_date = pd.to_datetime(target_date)

    # 计算目标日期与起始日期之间的天数差
    days_diff = (target_date - start_date).days

    if days_diff < 0:
        print(f"目标日期 {target_date} 小于起始日期 {start_date}")
        return None

    # 将起始列转换为列的索引（B列为1，C列为2，依此类推）
    start_column_index = ord(start_column) - ord('A') + 1

    # 计算目标列的索引
    column_index = start_column_index + days_diff - 1  # 从B列开始，所以减去1

    # 将列索引转为Excel风格的列名（支持AA, AB...）
    column_name = ''
    while column_index >= 0:
        column_name = chr(column_index % 26 + 65) + column_name
        column_index = column_index // 26 - 1

    return column_name


def get_row_for_specific_date(target_date, start_date="2025/1/1", start_row=2):
    """
    根据目标日期（例如：2025年1月1日），自动查找目标日期对应的行号，起始日期为指定行号。

    参数：
    - target_date: str, 目标日期（格式：YYYY/MM/DD）
    - start_date: str, 起始日期（默认为2025年1月1日，格式：YYYY/MM/DD）
    - start_row: int, 起始日期对应的行号（默认为2）

    返回：
    - 对应日期的行号

    示例使用：
    target_date = '2025/3/5'  # 目标日期，格式：YYYY/MM/DD
    row_number = get_row_for_specific_date(target_date)

    if row_number:
        print(f"目标日期 {target_date} 对应的行号是：{row_number}")
    else:
        print(f"没有找到目标日期 {target_date} 对应的行号")
    """
    # 将字符串日期转换为 datetime 对象
    start_date = pd.to_datetime(start_date)
    target_date = pd.to_datetime(target_date)

    # 计算目标日期与起始日期之间的天数差
    days_diff = (target_date - start_date).days

    if days_diff < 0:
        print(f"目标日期 {target_date} 小于起始日期 {start_date}")
        return None

    # 计算目标行号
    target_row = start_row + days_diff
    return target_row
