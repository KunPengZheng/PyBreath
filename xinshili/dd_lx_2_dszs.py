import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill


def insert_blank_row(filepath: str, row: int):
    wb = load_workbook(filepath)
    ws = wb.active

    # 检查指定行是否全为空（None 或 空字符串）
    def is_row_empty(worksheet, row_idx):
        for cell in worksheet[row_idx]:
            if cell.value not in (None, ""):
                return False
        return True

    if is_row_empty(ws, row):
        print(f"⚠️ {filepath} 的第 {row} 行已是空白行，跳过插入")
    else:
        ws.insert_rows(row)
        wb.save(filepath)
        print(f"✅ 已在 {filepath} 的第 {row} 行插入空白行")

    wb.close()


def unify_platform_order_and_highlight(filepath: str, output: str = None):
    # 读取 Excel
    df = pd.read_excel(filepath, dtype=str)

    # 确认关键列存在
    required_cols = ["标签", "系统单号", "平台单号"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"缺少必要的列: {col}")

    # 找出合并订单的行
    merged_mask = df["标签"].str.contains("合并订单", na=False)
    df_merged = df[merged_mask]

    # 处理：同一系统单号 → 平台单号统一成第一个值
    for sys_id, group in df_merged.groupby("系统单号"):
        if len(group) > 1:
            first_value = group["平台单号"].iloc[0]
            df.loc[group.index, "平台单号"] = first_value

    # 保存修改后的数据（临时）
    temp_file = output or filepath.replace(".xlsx", "_processed.xlsx")
    df.to_excel(temp_file, index=False)

    # 用 openpyxl 打开，填充颜色
    wb = load_workbook(temp_file)
    ws = wb.active

    # 黄色填充样式
    fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

    # 遍历合并订单的行，整行标黄
    for idx in df[merged_mask].index:
        excel_row = idx + 2  # +2 是因为 Excel 行号从1开始，且第一行是表头
        for cell in ws[excel_row]:
            cell.fill = fill

    # 保存最终文件
    wb.save(temp_file)
    print(f"✅ 处理完成，结果已保存到 {temp_file}")


if __name__ == '__main__':
    file_path = "/Users/zkp/Downloads/东谷210单_ts.xlsx"

    insert_blank_row(file_path, row=2)
    unify_platform_order_and_highlight(file_path, file_path)
