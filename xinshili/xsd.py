import pandas as pd
import os

def remove_duplicates_by_column(input_file, output_file, column_name):
    """
    删除指定列中重复的行，仅保留第一条，并保存为新的文件。

    参数：
    - input_file: str，输入文件路径
    - output_file: str，输出文件路径
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

        # 保存为新的文件
        df_deduplicated.to_excel(output_file, index=False)
        print(f"已生成去重后的文件：{output_file}")

    except Exception as e:
        print(f"处理文件时发生错误：{e}")

# 示例使用
input_file = input("请输入源文件路径：")
output_file = os.path.splitext(input_file)[0] + "_去重.xlsx"
column_name = "Tracking No./物流跟踪号"  # 要检查重复的列名

remove_duplicates_by_column(input_file, output_file, column_name)