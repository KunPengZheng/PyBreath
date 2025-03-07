import os
import re

from xinshili.gjgz_plus222 import extract_and_process_data, RowName, check_and_add_courier_column
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
    如果匹配成功，则将文件1中对应行的“Courier/快递”列内容复制到文件2中对应行的“Courier/快递”列，
    并将更新后的结果保存到 output_path 中。

    参数：
      file1_path: str，文件1路径，必须包含“Tracking No./物流跟踪号”和“Courier/快递”列
      file2_path: str，文件2路径，必须包含“Package 1 Tracking No./物流跟踪号1”和“Courier/快递”列
      output_path: str，保存更新后文件的路径
    """
    # 读取 Excel 文件
    df1 = pd.read_excel(file1_path)
    df2 = pd.read_excel(file2_path)

    # 提取文件1中需要的列：用于匹配的物流跟踪号和要复制的快递信息
    df1_subset = df1[["Tracking No./物流跟踪号", "Courier/快递"]]

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

    # 将合并后文件1中的“Courier/快递”列数据赋值到文件2对应的“Courier/快递”列中
    merged_df["Courier/快递"] = merged_df["Courier/快递_file1"]

    # 删除合并过程中产生的临时列
    merged_df.drop(columns=["Courier/快递_file1", "Tracking No./物流跟踪号"], inplace=True)

    # 将更新后的 DataFrame 保存为新的 Excel 文件
    merged_df.to_excel(output_path, index=False)

    print(f"更新后的文件已保存为 {output_path}")


def me(paths):
    lists = []
    pattern = r"^出库时间\d+_\d+\.xlsx$"

    # 遍历目录，匹配符合条件的文件
    for root, dirs, files in os.walk("/Users/zkp/Desktop/B&Y/轨迹统计/mxdg/2025.2"):
        for ele in files:
            if re.match(pattern, ele):
                xlsx_path = os.path.join(root, ele)  # 规范路径
                try:
                    df = pd.read_excel(xlsx_path)  # 读取 Excel 文件
                    lists.append(df)  # 存入 DataFrame
                except Exception as e:
                    print(f"错误: 无法读取文件 {xlsx_path}，错误信息: {e}")

    # 确保 lists 不是空的
    if lists:
        merged_df = pd.concat(lists, ignore_index=True)  # 合并 DataFrame
        merged_df.to_excel(paths, index=False)  # 保存合并后的文件
        print(f"合并完成，结果保存为 {paths}")
    else:
        print("错误: 没有找到可合并的 Excel 文件")


def highlight_courier_column(file_path):
    wb = load_workbook(file_path)
    ws = wb.active  # 获取当前活动的工作表

    # 5. 创建红色背景填充样式
    red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

    # 6. 找到 "Courier/快递" 列的索引
    col_index = None
    for col_num, col_cell in enumerate(ws[1], 1):  # 遍历第一行（列头）
        if col_cell.value == "Courier/快递":
            col_index = col_num
            break

    if col_index is None:
        print("错误: 未找到 'Courier/快递' 列")
        return

    # 7. 遍历列中的每一行，如果值匹配则设置红色背景
    for row in range(2, ws.max_row + 1):  # 从第2行开始（跳过列头）
        cell = ws.cell(row=row, column=col_index)
        if cell.value in ["pre_ship", "not_yet", "no_tracking"]:
            for col in range(1, ws.max_column + 1):  # 让整行变红
                ws.cell(row=row, column=col).fill = red_fill

    # 8. 保存 Excel 文件
    wb.save(file_path)
    print(f"标记完成，已更新 {file_path}")


xlsx_path = "/Users/zkp/Downloads/me.xlsx"
xlsx_3301 = "/Users/zkp/Downloads/副本自发货3301单.xlsx"
xlsx_8370 = "/Users/zkp/Downloads/副本其他客户8370单.xlsx"

me(xlsx_path)

output_file = os.path.splitext(xlsx_path)[0] + "_去重.xlsx"
remove_duplicates_by_column(xlsx_path, output_file, RowName.Tracking_No)

check_and_add_courier_column(xlsx_3301)
check_and_add_courier_column(xlsx_8370)

update_courier(output_file, xlsx_3301, xlsx_3301)
update_courier(output_file, xlsx_8370, xlsx_8370)

highlight_courier_column(xlsx_3301)
highlight_courier_column(xlsx_8370)
