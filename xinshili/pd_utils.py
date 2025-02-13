import pandas as pd
import os


def remove_duplicates_by_column(input_file, output_file, column_name):
    """
    删除指定列中重复的行，仅保留第一条，并覆盖源文件。

    参数：
    - input_file: str，输入文件路径
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
        df_deduplicated.to_excel(output_file, index=False)
    except Exception as e:
        print(f"处理文件时发生错误：{e}")


def filter_data(input_file, output_file, column_name, isinList):
    """
    将input_file1的指定列的内容 和 将input_file2的指定列的内容 进行匹配，匹配到了 则将input_file2指定列的内容 标记为红色
    :param input_file: 输入文件路径
    :param output_file: 结果文件路径
    :param column_name: 指定的列名
    :param isinList: 需要过滤出来的指定内容的集合
    """
    # 读取 Excel 文件
    df = pd.read_excel(input_file, engine='openpyxl')

    # 过滤数据，只保留符合条件的行
    filtered_df = df[df[column_name].isin(isinList)]

    # 将筛选结果保存到新的 Excel 文件
    filtered_df.to_excel(output_file, index=False, engine='openpyxl')

    print(f"筛选完成，结果已保存至 {output_file}")


def merge_xlsx_files(file_paths: list, output_path: str):
    """
    将多个文件合并为一个文件
    :param file_paths: 文件路径的数组
    :param output_path: 结果文件路径
    """
    # 用于存储合并后的所有数据
    combined_data = []

    for file_path in file_paths:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"文件 {file_path} 不存在，跳过")
            continue

        # 读取每个 Excel 文件的内容
        df = pd.read_excel(file_path)

        # 将每个文件的 DataFrame 加入到 combined_data 列表中
        combined_data.append(df)

    # 将所有 DataFrame 拼接在一起
    merged_df = pd.concat(combined_data, ignore_index=True)

    # 将合并后的数据保存到一个新的 Excel 文件
    merged_df.to_excel(output_path, index=False)

    print(f"所有文件已合并，结果保存为: {output_path}")
