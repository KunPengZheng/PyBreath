import os

import pandas as pd
import utils


# 以出库单号为判断条件，出现重复只保留第一条，其余都删除
def remove_duplicates_in_column(file_path, sheet_name, column_name, output_path):
    """
    删除 Excel 文件中某一列的重复值，只保留一个。

    :param file_path: 输入的 Excel 文件路径。
    :param sheet_name: 需要操作的工作表名称。
    :param column_name: 需要处理的列名称。
    :param output_path: 输出的 Excel 文件路径。
    """
    try:
        # 读取 Excel 文件
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # 删除某一列的重复值，只保留第一个
        df = df.drop_duplicates(subset=[column_name])

        # 保存处理后的数据到新的 Excel 文件
        df.to_excel(output_path, index=False)
        print(f"处理完成，结果已保存至: {output_path}")
    except Exception as e:
        print(f"处理过程中发生错误: {e}")


input_file = input("请输入源表文件的绝对路径：")  # 输入 Excel 文件路径
file_name_no_ext = os.path.splitext(input_file)[0]
output_file = "/Users/zkp/Desktop/B&Y/删除重复/" + file_name_no_ext + "_temp.xlsx"

sheet = "Sheet1"  # 需要处理的工作表
column = "Outbound Order No/出库单号"  # 需要去重的列名称

remove_duplicates_in_column(input_file, sheet, column, output_file)

utils.open_dir(output_file)
