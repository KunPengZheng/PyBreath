import pandas as pd
import warnings

from xinshili.fs_utils_plus import order_sheet_value, get_token
from xinshili.utils import round2

# 忽略 openpyxl 的样式警告
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# 仓库和客户定义
mx = "donggu(美西东谷)"
mz = "baoTX01(美中休斯敦)"
md = "feicheng(费城)"

client_RSN3001 = "RSN3001(东谷ZBW)"
client_RSN3002 = "RSN3002(东谷ZYL)"
client_RSN3003 = "RSN3003(东谷AY)"
client_RSN3004 = "RSN3004(东谷ZHQW)"
client_RSN3005 = "RSN3005(东谷BB-ZSSJ)"
client_RSN3006 = "RSN3006(作废3)"
client_RSN3007 = "RSN3007(东谷BB-DXL)"
client_RSN3008 = "RSN3008(东谷sanrio)"
client_RSN3009 = "RSN3009(东谷QUN)"
client_RSN30010 = "RSN3010(东谷JIANWEI)"
client_RSN30011 = "RSN3011(东谷BB-ZSSJZG)"
client_RSN30012 = "RSN3012(作废1)"
client_RSN30013 = "RSN3013(美中BBMZ-CCY)"
client_RSN30014 = "RSN3014(作废2)"
client_RSN30015 = "RSN3015(美中QUN)"
client_RSN30016 = "RSN3016(美中JianWei)"
client_RSN30017 = "RSN3017(美中XYL)"
client_RSN30018 = "RSN3018(美中BBMZ-ALVIN)"
client_RSN30019 = "RSN309(费城新引力)"
client_RSN30020 = "RSN3020(美中BBMZ-YJG)"
client_RSN30021 = "RSN3021(美中BBMZ-XDM)"
client_RSN30022 = "RSN3022(美中BBMZ-BBJY)"
client_RSN30023 = "RSN3023(东谷新引力)"
client_RSN30024 = "RSN3024(美中BBMZ-KLKJ)"
client_RSN30025 = "RSN3025(美中BBMZ-ZBW)"
client_RSN30026 = "RSN3026(美中BBMZ-ZYL)"
client_RSN30027 = "RSN3027(美中BBMZ-ZQW)"
client_RSN30028 = "RSN3028(美中BBMZ-AY)"
client_RSN30029 = "RSN3029(美中BBMZ-XLWX)"
client_RSN30030 = "RSN3030(美中BBMZ-XZMY)"
client_RSN30031 = "RSN3031(美中BBMZ-HAIOU)"
client_RSN30032 = "RSN3032(美中BBMZ-LTM)"
client_RSN30033 = "RSN3033(美中BBMZ-QWDZ)"

# 仓库排序规则
warehouse_order = [mx, mz, md]

# 客户集合
clients = [
    client_RSN3001, client_RSN3002, client_RSN3003, client_RSN3004, client_RSN3005, client_RSN3006,
    client_RSN3007, client_RSN3008, client_RSN3009, client_RSN30010, client_RSN30011, client_RSN30012,
    client_RSN30013, client_RSN30014, client_RSN30015, client_RSN30016, client_RSN30017, client_RSN30018,
    client_RSN30019, client_RSN30020, client_RSN30021, client_RSN30022, client_RSN30023, client_RSN30024,
    client_RSN30025, client_RSN30026, client_RSN30027, client_RSN30028, client_RSN30029, client_RSN30030,
    client_RSN30031, client_RSN30032, client_RSN30033
]


def analyze_data(file_path, order_column="Outbound Order No/出库单号",
                 time_column="OutboundTime/出库时间", warehouse_column="Warehouse/仓库",
                 client_column="Client/客户"):
    """
    分析每天的出库记录、仓库分布和客户订单信息，并为每一天计算 position = 日期的 day + 1。

    :param file_path: Excel 文件路径
    :param order_column: 出库单号列名
    :param time_column: 出库时间列名
    :param warehouse_column: 仓库列名
    :param client_column: 客户列名
    :return: 数据对象列表，每个对象包含每天的订单统计信息
    """
    try:
        # 加载 Excel 文件
        data = pd.read_excel(file_path, engine='openpyxl')

        # 检查列是否存在
        for col in [order_column, time_column, warehouse_column, client_column]:
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

        # 按日期分组
        grouped = data.groupby('Date', sort=True)

        for date, group in grouped:
            total_orders = len(group)  # 当天的订单总数

            # 获取各仓库的订单数
            warehouse_counts = group[warehouse_column].value_counts().to_dict()

            # 获取各客户的订单数
            client_counts = group[client_column].value_counts().to_dict()

            # 根据指定顺序排序仓库和客户
            sorted_warehouse_counts = {w: warehouse_counts.get(w, 0) for w in warehouse_order}
            sorted_client_counts = {c: client_counts.get(c, 0) for c in clients}

            # 计算仓库占比，并乘以100保留两位小数
            sorted_warehouse_ratios = {
                w: round2((sorted_warehouse_counts[w] / total_orders) * 100) if total_orders > 0 else 0
                for w in warehouse_order}

            # 计算客户占比，并乘以100保留两位小数
            sorted_client_ratios = {
                c: round2((sorted_client_counts[c] / total_orders) * 100) if total_orders > 0 else 0
                for c in clients}

            # 计算 position = 日期的 day + 1
            position = date.day + 1

            # 创建对象存储数据
            daily_data = {
                "position": position,
                "date": date,
                "total_orders": total_orders,
                "warehouse_counts": sorted_warehouse_counts,
                "warehouse_ratios": sorted_warehouse_ratios,
                "client_counts": sorted_client_counts,
                "client_ratios": sorted_client_ratios
            }
            result_list.append(daily_data)

        return result_list

    except Exception as e:
        print(f"发生错误: {e}")
        return None


# 主程序
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
        print(f"客户订单数: {daily_data['client_counts']}")
        print(f"客户占比: {daily_data['client_ratios']}")
        print("-" * 40)

        warehouse_counts_map = daily_data['warehouse_counts']
        warehouse_ratios_map = daily_data['warehouse_ratios']
        client_counts_map = daily_data['client_counts']
        client_ratios_map = daily_data['client_ratios']

        # 传递数据到表单（示例）
        order_sheet_value(tat, [
            daily_data['total_orders'],

            str(warehouse_counts_map[mx]) + "（" + str(warehouse_ratios_map[mx]) + "%）",
            str(warehouse_counts_map[mz]) + "（" + str(warehouse_ratios_map[mz]) + "%）",
            str(warehouse_counts_map[md]) + "（" + str(warehouse_ratios_map[md]) + "%）",

            str(client_counts_map[client_RSN3001]) + "（" + str(client_ratios_map[client_RSN3001]) + "%）",
            str(client_counts_map[client_RSN3002]) + "（" + str(client_ratios_map[client_RSN3002]) + "%）",
            str(client_counts_map[client_RSN3003]) + "（" + str(client_ratios_map[client_RSN3003]) + "%）",
            str(client_counts_map[client_RSN3004]) + "（" + str(client_ratios_map[client_RSN3004]) + "%）",
            str(client_counts_map[client_RSN3005]) + "（" + str(client_ratios_map[client_RSN3005]) + "%）",
            str(client_counts_map[client_RSN3006]) + "（" + str(client_ratios_map[client_RSN3006]) + "%）",
            str(client_counts_map[client_RSN3007]) + "（" + str(client_ratios_map[client_RSN3007]) + "%）",
            str(client_counts_map[client_RSN3008]) + "（" + str(client_ratios_map[client_RSN3008]) + "%）",
            str(client_counts_map[client_RSN3009]) + "（" + str(client_ratios_map[client_RSN3009]) + "%）",
            str(client_counts_map[client_RSN30010]) + "（" + str(client_ratios_map[client_RSN30010]) + "%）",
            str(client_counts_map[client_RSN30011]) + "（" + str(client_ratios_map[client_RSN30011]) + "%）",
            str(client_counts_map[client_RSN30012]) + "（" + str(client_ratios_map[client_RSN30012]) + "%）",
            str(client_counts_map[client_RSN30013]) + "（" + str(client_ratios_map[client_RSN30013]) + "%）",
            str(client_counts_map[client_RSN30014]) + "（" + str(client_ratios_map[client_RSN30014]) + "%）",
            str(client_counts_map[client_RSN30015]) + "（" + str(client_ratios_map[client_RSN30015]) + "%）",
            str(client_counts_map[client_RSN30016]) + "（" + str(client_ratios_map[client_RSN30016]) + "%）",
            str(client_counts_map[client_RSN30017]) + "（" + str(client_ratios_map[client_RSN30017]) + "%）",
            str(client_counts_map[client_RSN30018]) + "（" + str(client_ratios_map[client_RSN30018]) + "%）",
            str(client_counts_map[client_RSN30019]) + "（" + str(client_ratios_map[client_RSN30019]) + "%）",
            str(client_counts_map[client_RSN30020]) + "（" + str(client_ratios_map[client_RSN30020]) + "%）",
            str(client_counts_map[client_RSN30021]) + "（" + str(client_ratios_map[client_RSN30021]) + "%）",
            str(client_counts_map[client_RSN30022]) + "（" + str(client_ratios_map[client_RSN30022]) + "%）",
            str(client_counts_map[client_RSN30023]) + "（" + str(client_ratios_map[client_RSN30023]) + "%）",
            str(client_counts_map[client_RSN30024]) + "（" + str(client_ratios_map[client_RSN30024]) + "%）",
            str(client_counts_map[client_RSN30025]) + "（" + str(client_ratios_map[client_RSN30025]) + "%）",
            str(client_counts_map[client_RSN30026]) + "（" + str(client_ratios_map[client_RSN30026]) + "%）",
            str(client_counts_map[client_RSN30027]) + "（" + str(client_ratios_map[client_RSN30027]) + "%）",
            str(client_counts_map[client_RSN30028]) + "（" + str(client_ratios_map[client_RSN30028]) + "%）",
            str(client_counts_map[client_RSN30029]) + "（" + str(client_ratios_map[client_RSN30029]) + "%）",
            str(client_counts_map[client_RSN30030]) + "（" + str(client_ratios_map[client_RSN30030]) + "%）",
            str(client_counts_map[client_RSN30031]) + "（" + str(client_ratios_map[client_RSN30031]) + "%）",
            str(client_counts_map[client_RSN30032]) + "（" + str(client_ratios_map[client_RSN30032]) + "%）",
            str(client_counts_map[client_RSN30033]) + "（" + str(client_ratios_map[client_RSN30033]) + "%）",
        ], daily_data['position'], daily_data['date'])
