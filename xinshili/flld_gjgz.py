import pandas as pd
import random
import time

from xinshili.usps_utils import track
from xinshili.utils import get_file_dir, get_filename_without_extension


def extract_and_process_data(filepath, column_name, group_size=35):
    """
    从 Excel 文件中提取指定列的数据，按组发送请求并统计满足条件的结果。

    参数:
    - filepath: str，Excel 文件路径
    - column_name: str，要提取的列名
    - group_size: int，每组的数据大小

    返回:
    - list，满足条件的结果数据
    """
    # 读取 Excel 文件
    data = pd.read_excel(filepath)

    # 检查列是否存在
    if column_name not in data.columns:
        raise ValueError(f"列 '{column_name}' 不存在于 Excel 文件中")

    # 获取指定列数据并去除空值
    items = data[column_name].dropna().tolist()

    # 按组划分数据
    grouped_items = [items[i:i + group_size] for i in range(0, len(items), group_size)]

    # 存储满足条件的结果
    tracking_results = []
    no_tracking_results = []
    unpaid_results = []
    not_yet_results = []
    pre_ship_results = []
    delivered_results = []

    text = "The package associated with this tracking number did not have proper postage applied and will not be delivered"
    text1 = "Delivered"

    # 请求每组数据
    for idx, group in enumerate(grouped_items, start=1):
        print(f"处理第 {idx} 组，共 {len(group)} 条数据")
        track1 = track(group)

        for package_id, info in track1['data'].items():
            if info.get('err'):
                if info.get('err_id') == '-2147219283':  # 无轨迹(Label Created, not yet in system)
                    no_tracking_results.append(package_id)
                    not_yet_results.append(package_id)
                elif info.get('err_id') == 'pre-ship':  # 无轨迹(pre-ship)
                    no_tracking_results.append(package_id)
                    pre_ship_results.append(package_id)
                else:
                    no_tracking_results.append(package_id)
            else:
                if info.get('statusLong') in text:
                    unpaid_results.append(package_id)
                if info.get('statusShort') in text1:
                    delivered_results.append(package_id)
                tracking_results.append(package_id)

        # 随机生成 5 到 10 秒之间的等待时间
        wait_time = random.uniform(5, 10)
        time.sleep(wait_time)

    print(f"没有轨迹数： {len(no_tracking_results)} 条，有轨迹数： {len(tracking_results)} 条")
    print(f"\nunpaid数： {len(unpaid_results)} 条")
    print(f"\nnot_yet数： {len(not_yet_results)} 条")
    print(f"\npre_ship数： {len(pre_ship_results)} 条")
    print(f"\ndelivered数： {len(delivered_results)} 条")

    output_file = get_file_dir(input_file) + "/" + get_filename_without_extension(
        input_file) + "_有轨迹" + f"{len(tracking_results)}单" + ".xlsx"

    # 从原始数据中删除无轨迹的行
    filtered_data = data[~data[column_name].isin(no_tracking_results)]
    # 保存为新的 Excel 文件
    filtered_data.to_excel(output_file, index=False)
    print(f"处理完成，新文件保存至: {output_file}")


# 示例调用
file_path = "/Users/zkp/Desktop/B&Y/轨迹统计/佛罗里达/佛罗里达117单回传.xlsx"  # 替换为你的输入文件路径
input_file = input("请输入源表文件的绝对路径：")
try:
    extract_and_process_data(file_path, "跟踪号", 35)
except Exception as e:
    print("错误:", e)
