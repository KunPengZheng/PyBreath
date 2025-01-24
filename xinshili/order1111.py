import pandas as pd
import warnings

# 忽略 openpyxl 的样式警告
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


def analyze_data(file_path, order_column="Outbound Order No/出库单号",
                 time_column="OutboundTime/出库时间", warehouse_column="Warehouse/仓库"):
    """
    分析每天的出库记录及仓库占比。

    :param file_path: Excel 文件路径
    :param order_column: 出库单号列名
    :param time_column: 出库时间列名
    :param warehouse_column: 仓库列名
    :return: 按天的出库记录总数和仓库占比信息
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

        # 添加日期字段（仅保留日期部分）
        data['Date'] = data[time_column].dt.date

        # 按日期统计总数
        daily_counts = data.groupby('Date').size().reset_index(name='Total Records')

        # 按日期和仓库统计数量
        daily_warehouse_counts = data.groupby(['Date', warehouse_column]).size().reset_index(name='Count')

        # 计算每日仓库占比
        results = []
        for date, group in daily_warehouse_counts.groupby('Date'):
            total_records = daily_counts.loc[daily_counts['Date'] == date, 'Total Records'].values[0]
            group['Percentage'] = (group['Count'] / total_records * 100).round(2)
            results.append(group)

        # 合并结果
        final_results = pd.concat(results).reset_index(drop=True)
        return daily_counts, final_results

    except Exception as e:
        print(f"发生错误: {e}")
        return None, None


# 主程序
file_path = input("请输入Excel文件的路径：")

# 分析数据
daily_counts, final_results = analyze_data(file_path)

if daily_counts is not None and final_results is not None:
    print("\n每天的出库记录总数：")
    print(daily_counts)
    print("\n每天的仓库占比分析：")
    print(final_results)
