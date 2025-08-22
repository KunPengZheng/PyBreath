import pandas as pd
import os
from datetime import datetime

from xinshili.utils import ensure_directory_exists


def remove_duplicates_by_column(input_file, output_file, column_name):
    """
    去重：删除指定列中重复的行，仅保留第一条，并覆盖源文件，同时返回去重后的行数。

    参数：
    - input_file: str，输入文件路径
    - column_name: str，要检查重复的列名
    """
    try:
        # 读取 Excel 文件
        df = pd.read_excel(input_file, dtype=str)

        # 检查列名是否存在
        if column_name not in df.columns:
            raise ValueError(f"列 '{column_name}' 不存在于输入文件中！")

        # 删除指定列的重复项，仅保留第一条
        df_deduplicated = df.drop_duplicates(subset=[column_name], keep='first')

        # 将去重后的数据保存到输出文件
        df_deduplicated.to_excel(output_file, index=False)

        # 返回去重后的行数
        return len(df_deduplicated)

    except Exception as e:
        print(f"处理文件时发生错误：{e}")
        return 0  # 如果出现错误，返回 0 行数


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


def copy_new_file(input_path, output_path):
    """
    复制生成新文件
    """
    # 读取原始 Excel 文件
    df = pd.read_excel(input_path, dtype=str)
    # 将数据写入新的 Excel 文件
    df.to_excel(output_path, index=False)


def split_excel_by_date_and_unique_count(
        input_file,
        time_column="Creation time/创建时间",
        unique_column="Platform Number/平台单号",
        file_prefix="",
        output_dir="output_files"
):
    # 读取 Excel 文件
    df = pd.read_excel(input_file)

    if time_column not in df.columns:
        raise ValueError(f"Excel 中没有找到列: {time_column}")
    if unique_column not in df.columns:
        raise ValueError(f"Excel 中没有找到列: {unique_column}")

    # 转换为 datetime 类型
    df[time_column] = pd.to_datetime(df[time_column], errors="coerce")

    # 去掉无效日期
    df = df.dropna(subset=[time_column])

    # 提取年月日
    df = df.copy()
    df["date_only"] = df[time_column].dt.strftime("%Y-%m-%d")

    # 按日期分组
    for dates, group in df.groupby("date_only"):
        # 先把 date 转换回 datetime 对象
        dt = datetime.strptime(dates, "%Y-%m-%d")
        # 获取月份和日期（不带前导 0）
        year = dt.year
        month = dt.month
        day = dt.day

        # 只计算去重后的个数（不保存去重数据）
        unique_count = group[unique_column].nunique()

        sub_output_dir = output_dir + f"/{year}.{month}"

        ensure_directory_exists(sub_output_dir)

        # 文件名：日期_去重个数.xlsx
        output_file = os.path.join(sub_output_dir, f"{file_prefix}{day}_{unique_count}.xlsx")

        # 保存原始分组数据（保持行数不变）
        group.drop(columns=["date_only"]).to_excel(output_file, index=False)

        print(f"已生成: {output_file} (去重个数: {unique_count}, 原始行数: {len(group)})")


split_excel_by_date_and_unique_count("/Users/zkp/Downloads/ParcelOutbound_20250822113727.xlsx",
                                     output_dir="/Users/zkp/Downloads/未命名文件夹 3")
