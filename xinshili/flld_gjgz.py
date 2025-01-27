import pandas as pd

from xinshili.usps_utils import track


def extract_and_process_data(filepath, output_filepath, column_name="\u8ddf\u8e2a\u53f7", group_size=35):
    """
    从 Excel 文件中提取指定列的数据，按组发送请求并统计满足条件的结果。

    参数:
    - filepath: str，Excel 文件路径
    - output_filepath: str，处理后保存的新文件路径
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
    no_tracking_results = []

    # 请求每组数据
    for idx, group in enumerate(grouped_items, start=1):
        print(f"处理第 {idx} 组，共 {len(group)} 条数据")
        track1 = track(group)

        for package_id, info in track1['data'].items():
            if info.get('err'):
                print(f"Package ID: {package_id} - 无轨迹")
                no_tracking_results.append(package_id)
            else:
                print(f"Package ID: {package_id} - 有轨迹")

    print(f"无轨迹数据共 {len(no_tracking_results)} 条")

    # 从原始数据中删除无轨迹的行
    filtered_data = data[~data[column_name].isin(no_tracking_results)]

    # 保存为新的 Excel 文件
    filtered_data.to_excel(output_filepath, index=False)
    print(f"处理完成，新文件保存至: {output_filepath}")

    return no_tracking_results


# 示例调用
file_path = "/Users/zkp/Desktop/B&Y/轨迹统计/佛罗里达/佛罗里达117单回传.xlsx"  # 替换为你的输入文件路径
output_file_path = "/Users/zkp/Desktop/B&Y/轨迹统计/佛罗里达/佛罗里达117单回传_temp.xlsx"  # 替换为你的输出文件路径
column_name = "跟踪号"  # 替换为你的列名
group_size = 35

try:
    result_data = extract_and_process_data(file_path, output_file_path, column_name, group_size)
    print(f"处理完成，满足条件的数据共 {len(result_data)} 条")
except Exception as e:
    print("错误:", e)
