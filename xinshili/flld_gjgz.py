import pandas as pd

from xinshili.usps_utils import track


def extract_and_process_data(filepath, column_name="跟踪号", group_size=35):
    """
    从 Excel 文件中提取指定列的数据，按组发送请求并统计满足条件的结果。

    参数:
    - filepath: str，Excel 文件路径
    - column_name: str，要提取的列名
    - group_size: int，每组的数据大小
    - api_url: str，接口地址
    - condition_key: str，接口响应中判断条件的键
    - condition_value: str，接口响应中判断条件的值

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
    results = []

    # 请求每组数据
    for idx, group in enumerate(grouped_items, start=1):
        print(f"处理第 {idx} 组，共 {len(group)} 条数据")
        group_results = []
        track1 = track(group)

        for package_id, info in track1['data'].items():
            print(f"Package ID: {package_id}")
            if info.get('err'):
                print(f"Error: {info['err_desc']}")  # 无轨迹
                group_results.append(package_id)
            else:
                print(f"Destination: {info['destinationCity']}, {info['destinationState']}")
                print(f"Status: {info['statusShort']}")
                print(f"Details: {info['statusLong']}")
                print(f"Last Updated: {info['latestEventSfDateTime']}")
            print("-" * 30)

        # 将满足条件的结果存入最终数组]
        print(f"处理第 {idx} 组，共 {len(group)} 条数据，共 {len(group_results)} 条数据无轨迹")
        results.extend(group_results)

    # 返回结果
    return results


# 示例调用
file_path = "/Users/zkp/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/aee968804ccf60699f2aada7c6e578a8/Message/MessageTemp/fd8511edf7e3e2cab96f63bd9b9d5f86/File/佛罗里达117单回传.xlsx"  # 替换为你的文件路径
column_name = "跟踪号"  # 替换为你的列名
group_size = 35

try:
    result_data = extract_and_process_data(file_path, column_name, group_size)
    print(f"处理完成，满足条件的数据共 {len(result_data)} 条")
    print("结果数据：", result_data)
except Exception as e:
    print("错误:", e)
