import pandas as pd
import warnings

# 忽略 openpyxl 的样式警告
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


def analyze_warehouse_distribution(file_path, order_column="Outbound Order No/出库单号",
                                   warehouse_column="Warehouse/仓库"):
    """
    订单数据分析：
    删除 `Outbound Order No/出库单号` 列的重复值（同一单有多个sku会生成多条数据），然后计算订单总数; 分析各个仓库的订单数量；
    """
    try:
        # 加载 Excel 文件
        data = pd.read_excel(file_path, engine='openpyxl')

        # 检查列是否存在
        if order_column not in data.columns or warehouse_column not in data.columns:
            raise ValueError(f"列 '{order_column}' 或 '{warehouse_column}' 不存在！")

        # 根据出库单号去重
        deduplicated_data = data.drop_duplicates(subset=order_column)

        # 计算仓库分布占比
        warehouse_counts = deduplicated_data[warehouse_column].value_counts()
        total_count = warehouse_counts.sum()
        warehouse_percentages = (warehouse_counts / total_count) * 100

        # 打印分析结果
        print(f"去重后总记录数：{total_count}\n")
        print(f"{warehouse_column} 分布占比分析：")
        for warehouse, count in warehouse_counts.items():
            percentage = warehouse_percentages[warehouse]
            print(f"{warehouse}: {count} 条，占比 {percentage:.2f}%")

        # 返回分析结果
        return total_count, warehouse_counts.to_dict(), warehouse_percentages.to_dict()

    except Exception as e:
        print(f"发生错误: {e}")
        return None, None, None


input_file = input("请输入文件的绝对路径：")
total_count, warehouse_counts, warehouse_percentages = analyze_warehouse_distribution(
    input_file,
    order_column="Outbound Order No/出库单号",
    warehouse_column="Warehouse/仓库"
)

