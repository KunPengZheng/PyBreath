import os
import re

from xinshili.gjgz_plus222 import extract_and_process_data, RowName
from xinshili.gjgz_plus333 import check_and_add_courier_column
from xinshili.openpyxl_utils import merge_xlsx_files
from xinshili.pd_utils import remove_duplicates_by_column
import os
import re
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill


def update_courier(file1_path, file2_path, output_path):
    """
    根据两个 Excel 文件中的物流跟踪号进行匹配，
    如果匹配成功，则将文件1中对应行的“Courier/快递”列内容和“SfDateInterval/SF消息间隔”列内容
    复制到文件2中对应行的“Courier/快递”列和“SfDateInterval/SF消息间隔”列，
    并将更新后的结果保存到 output_path 中。

    参数：
      file1_path: str，文件1路径，必须包含“Tracking No./物流跟踪号”和“Courier/快递”列
      file2_path: str，文件2路径，必须包含“Package 1 Tracking No./物流跟踪号1”和“Courier/快递”列
      output_path: str，保存更新后文件的路径
    """
    # 读取 Excel 文件
    df1 = pd.read_excel(file1_path)
    df2 = pd.read_excel(file2_path)

    # 提取文件1中需要的列：用于匹配的物流跟踪号、快递信息和消息间隔
    df1_subset = df1[["Tracking No./物流跟踪号",
                      "Courier/快递",
                      "PossessionSfDate/揽收时间",
                      "LatestEventSfDate/最新事件时间",
                      "SfDateInterval/SF消息间隔"]]

    # 合并两个 DataFrame：以文件2为主表，
    # 通过文件2的“Package 1 Tracking No./物流跟踪号1”与文件1的“Tracking No./物流跟踪号”匹配
    merged_df = pd.merge(
        df2,
        df1_subset,
        left_on="Package 1 Tracking No./物流跟踪号1",
        right_on="Tracking No./物流跟踪号",
        how="left",
        suffixes=("", "_file1")
    )

    # 将合并后文件1中的“Courier/快递”和“SfDateInterval/SF消息间隔”列数据赋值到文件2对应的列中
    merged_df["Courier/快递"] = merged_df["Courier/快递_file1"]
    merged_df["PossessionSfDate/揽收时间"] = merged_df["PossessionSfDate/揽收时间_file1"]
    merged_df["LatestEventSfDate/最新事件时间"] = merged_df["LatestEventSfDate/最新事件时间_file1"]
    merged_df["SfDateInterval/SF消息间隔"] = merged_df["SfDateInterval/SF消息间隔_file1"]

    # 删除合并过程中产生的临时列
    merged_df.drop(columns=["Courier/快递_file1",
                            "PossessionSfDate/揽收时间_file1",
                            "LatestEventSfDate/最新事件时间_file1",
                            "SfDateInterval/SF消息间隔_file1",
                            "Tracking No./物流跟踪号"],
                   inplace=True)

    # 将更新后的 DataFrame 保存为新的 Excel 文件
    merged_df.to_excel(output_path, index=False)

    print(f"更新后的文件已保存为 {output_path}")


def me(save_paths, target_dir, pattern_flag=True):
    lists = []
    pattern = r"^(出库时间|创建时间)\d+_\d+\.xlsx$"

    # 遍历目录，匹配符合条件的文件
    for root, dirs, files in os.walk(target_dir):
        for ele in files:
            if (pattern_flag):
                if re.match(pattern, ele):
                    xlsx_path = os.path.join(root, ele)  # 规范路径
                    try:
                        df = pd.read_excel(xlsx_path)  # 读取 Excel 文件
                        lists.append(df)  # 存入 DataFrame
                    except Exception as e:
                        print(f"错误: 无法读取文件 {xlsx_path}，错误信息: {e}")
            else:
                xlsx_path = os.path.join(root, ele)  # 规范路径
                try:
                    df = pd.read_excel(xlsx_path)  # 读取 Excel 文件
                    lists.append(df)  # 存入 DataFrame
                except Exception as e:
                    print(f"错误: 无法读取文件 {xlsx_path}，错误信息: {e}")

    # 确保 lists 不是空的
    if lists:
        merged_df = pd.concat(lists, ignore_index=True)  # 合并 DataFrame
        merged_df.to_excel(save_paths, index=False)  # 保存合并后的文件
        print(f"合并完成，结果保存为 {save_paths}")
    else:
        print("错误: 没有找到可合并的 Excel 文件")


def highlight_courier_column(file_path):
    wb = load_workbook(file_path)
    ws = wb.active  # 获取当前活动的工作表

    red_fill = PatternFill(start_color="C0D79B", end_color="C0D79B", fill_type="solid")

    # 找到 "Courier/快递" 列和 "SfDateInterval/SF消息间隔" 列的索引
    courier_col_index = None
    sf_date_interval_col_index = None

    # 遍历第一行（列头）找到相关列的索引
    for col_num, col_cell in enumerate(ws[1], 1):
        if col_cell.value == "Courier/快递":
            courier_col_index = col_num
        elif col_cell.value == "SfDateInterval/SF消息间隔":
            sf_date_interval_col_index = col_num

    if courier_col_index is None:
        print("错误: 未找到 'Courier/快递' 列")
        return
    if sf_date_interval_col_index is None:
        print("错误: 未找到 'SfDateInterval/SF消息间隔' 列")
        return

    # 遍历列中的每一行，如果满足条件则设置红色背景
    for row in range(2, ws.max_row + 1):  # 从第2行开始（跳过列头）
        courier_cell = ws.cell(row=row, column=courier_col_index)
        sf_date_interval_cell = ws.cell(row=row, column=sf_date_interval_col_index)

        # 检查 Courier/快递 为特定值并且 SfDateInterval/SF消息间隔 为 0
        if courier_cell.value in ["pre_ship", "not_yet", "no_tracking"] or \
                (courier_cell.value == "tracking" and sf_date_interval_cell.value == 0):
            for col in range(1, ws.max_column + 1):  # 让整行变红
                ws.cell(row=row, column=col).fill = red_fill

    # 保存 Excel 文件
    wb.save(file_path)
    print(f"标记完成，已更新 {file_path}")


xlsx_zfh = "/Users/zkp/Downloads/副本25年3月自发货_副本.xlsx"
xlsx_qtkh = "/Users/zkp/Downloads/副本25年3月其他客户_副本.xlsx"

zbw_month_dir = "/Users/zkp/Desktop/B&Y/轨迹统计/zbw/2025.3"
sanrio_month_dir = "/Users/zkp/Desktop/B&Y/轨迹统计/sanrio/2025.3"
xyl_month_dir = "/Users/zkp/Desktop/B&Y/轨迹统计/xyl/2025.3"
me_dir = "/Users/zkp/Downloads/me/"
me_file = f"{me_dir}me.xlsx"

# 客户各自的数据合并
me(f"{me_dir}zbw_me.xlsx", zbw_month_dir)
me(f"{me_dir}sanrio_me.xlsx", sanrio_month_dir)
me(f"{me_dir}xyl_me.xlsx", xyl_month_dir)
# 合并多个客户
me(me_file, me_dir, False)

# 去重
remove_duplicates_me_file = os.path.splitext(me_file)[0] + "_remove_duplicates.xlsx"
remove_duplicates_by_column(me_file, remove_duplicates_me_file, RowName.Tracking_No)

# 补充缺少的列名
check_and_add_courier_column(xlsx_zfh)
check_and_add_courier_column(xlsx_qtkh)

# 根据指定列匹配，匹配成功后将对应列的内容复制过来
update_courier(remove_duplicates_me_file, xlsx_zfh, xlsx_zfh)
update_courier(remove_duplicates_me_file, xlsx_qtkh, xlsx_qtkh)

# 根据指定条件标记背景颜色
highlight_courier_column(xlsx_zfh)
highlight_courier_column(xlsx_qtkh)
