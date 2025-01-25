import pandas as pd
import warnings

from xinshili.fs_utils import get_token, order_sheet_value
import pandas as pd
import warnings

from xinshili.utils import round2

# 忽略 openpyxl 的样式警告
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

mx = "donggu(美西东谷)"
mz = "baoTX01(美中休斯敦)"
md = "feicheng(费城)"


def analyze_data(file_path, order_column="Outbound Order No/出库单号",
                 time_column="OutboundTime/出库时间", warehouse_column="Warehouse/仓库"):
    """
    分析每天的出库记录及仓库分布，并为每一天计算 position = 日期的 day + 1。

    :param file_path: Excel 文件路径
    :param order_column: 出库单号列名
    :param time_column: 出库时间列名
    :param warehouse_column: 仓库列名
    :return: 数据对象列表，每个对象包含每天的订单统计信息
    """
    try:
        # 加载 Excel 文件
        data = pd.read_excel(file_path, engine='openpyxl')

        # 检查列是否存在
        for col in [order_column, time_column, warehouse_column]:
            if col not in data.columns:
                raise ValueError(f"列 '{col}' 不存在！")

        # 去重操作，以出库单号为基准
        data = data.drop_duplicates(subset=[order_column])

        # 确保出库时间列为日期时间格式
        data[time_column] = pd.to_datetime(data[time_column], errors='coerce')

        # 检查是否存在无法解析的时间值
        if data[time_column].isna().any():
            print(f"警告: 出库时间列中存在无法解析的值！这些值将被忽略。")

        # 添加日期字段（仅保留日期部分）
        data['Date'] = data[time_column].dt.date

        # 初始化结果列表
        result_list = []

        # 仓库排序规则，注意⚠️仓库名字发生改变的时候要进行修改！！！！！！
        warehouse_order = [mx, mz, md]

        # 按日期分组
        grouped = data.groupby('Date', sort=True)

        for date, group in grouped:
            total_orders = len(group)  # 当天的订单总数

            # 获取各仓库的订单数
            warehouse_counts = group[warehouse_column].value_counts().to_dict()

            # 检查当天的仓库计数
            # print(f"调试: 日期 {date} 的仓库计数 {warehouse_counts}")

            # 根据指定顺序排序
            sorted_counts = {w: warehouse_counts.get(w, 0) for w in warehouse_order}

            # 检查排序后计数
            # print(f"调试: 日期 {date} 的排序后仓库计数 {sorted_counts}")

            # 计算占比，并乘以100保留两位小数
            sorted_ratios = {w: round2((sorted_counts[w] / total_orders) * 100) if total_orders > 0 else 0
                             for w in warehouse_order}

            # 检查占比计算
            # print(f"调试: 日期 {date} 的排序后仓库占比 {sorted_ratios}")

            # 计算 position = 日期的 day + 1
            position = date.day + 1

            # 创建对象存储数据
            daily_data = {
                "position": position,
                "date": date,
                "total_orders": total_orders,
                "warehouse_counts": sorted_counts,
                "warehouse_ratios": sorted_ratios,
            }
            result_list.append(daily_data)

        return result_list

    except Exception as e:
        print(f"发生错误: {e}")
        return None


file_path = input("请输入Excel文件的路径：")
result = analyze_data(file_path)
tat = get_token()
if result:
    print("\n每天的订单统计：")
    for daily_data in result:
        print(f"Position: {daily_data['position']}")
        print(f"日期: {daily_data['date']}")
        print(f"总订单数: {daily_data['total_orders']}")
        print(f"仓库订单数: {daily_data['warehouse_counts']}")
        print(f"仓库占比: {daily_data['warehouse_ratios']}")
        print("-" * 40)
        warehouse_counts_map = daily_data['warehouse_counts']
        warehouse_ratios_map = daily_data['warehouse_ratios']
        order_sheet_value(tat, [
            daily_data['total_orders'],
            str(warehouse_counts_map[mx]) + "（" + str(warehouse_ratios_map[mx]) + "%）",
            str(warehouse_counts_map[mz]) + "（" + str(warehouse_ratios_map[mz]) + "%）",
            str(warehouse_counts_map[md]) + "（" + str(warehouse_ratios_map[md]) + "%）",
        ], daily_data['position'])
