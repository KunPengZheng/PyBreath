import os
import pandas as pd
from collections import defaultdict
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


def unify_orders_across_files(folder: str, output_suffix="_processed"):
    """
    处理文件夹下所有文件：
    - 合并订单（统一平台单号）
    - 拆分订单（跨文件判断，加后缀）
    """
    files = [f for f in os.listdir(folder) if f.endswith(".xlsx") and not f.startswith("~$")]
    files.sort()

    all_data = []  # 存储所有文件的数据 {file_idx, row_idx, sysno, platform, 标签}
    files_data = []  # 存储每个文件的DataFrame

    # 读取所有文件
    for i, fname in enumerate(files):
        fpath = os.path.join(folder, fname)
        df = pd.read_excel(fpath, dtype=str).fillna("")
        if not {"标签", "系统单号", "平台单号"}.issubset(df.columns):
            print(f"⚠️ {fname} 缺少必要列，跳过")
            continue

        files_data.append({"filename": fname, "path": fpath, "df": df})

        for idx in df.index:
            all_data.append({
                "file_idx": i,
                "row_idx": idx,
                "标签": df.at[idx, "标签"],
                "sysno": df.at[idx, "系统单号"].strip(),
                "platform": df.at[idx, "平台单号"].strip()
            })

    if not all_data:
        print("⚠️ 没有找到可处理的数据")
        return

    # ---------------- 合并订单逻辑 ---------------- #
    for file_meta in files_data:
        df = file_meta["df"]
        merged_mask = df["标签"].str.contains("合并订单", na=False)
        for sys_id, group in df[merged_mask].groupby("系统单号"):
            if len(group) > 1:
                first_value = group["平台单号"].iloc[0]
                df.loc[group.index, "平台单号"] = first_value

    # ---------------- 拆分订单逻辑（跨文件） ---------------- #
    split_groups = defaultdict(list)
    for r in all_data:
        if "拆分订单" in r["标签"]:
            split_groups[(r["sysno"], r["platform"])].append(r)

    for (sysno, platform), group in split_groups.items():
        if len(group) <= 1:
            continue
        # 按文件顺序 + 行顺序排序
        group_sorted = sorted(group, key=lambda x: (x["file_idx"], x["row_idx"]))
        for i, rec in enumerate(group_sorted[1:], start=1):
            file_meta = files_data[rec["file_idx"]]
            df = file_meta["df"]
            old_val = df.at[rec["row_idx"], "平台单号"]
            new_val = f"{old_val}-{i}"
            df.at[rec["row_idx"], "平台单号"] = new_val
            print(f"✏️ 修改 {file_meta['filename']} 第 {rec['row_idx'] + 2} 行: {old_val} → {new_val}")

    # ---------------- 保存并标黄 ---------------- #
    yellow = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

    for meta in files_data:
        df = meta["df"]
        output_path = meta["path"].replace(".xlsx", f"{output_suffix}.xlsx")
        df.to_excel(output_path, index=False)

        wb = load_workbook(output_path)
        ws = wb.active

        mask = df["标签"].str.contains("合并订单|拆分订单", na=False)
        for idx in df[mask].index:
            excel_row = idx + 2  # pandas index → Excel 行号
            for cell in ws[excel_row]:
                cell.fill = yellow

        wb.save(output_path)
        wb.close()
        print(f"✅ 保存完成: {output_path}")


if __name__ == '__main__':
    folder_path = "/Users/zkp/Downloads/未命名文件夹 2/"
    unify_orders_across_files(folder_path)
