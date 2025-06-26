import pandas as pd


def find_column_duplicates(file_path):
    df = pd.read_excel(file_path, dtype=str).fillna("")

    check_columns = ["订单号", "物流单号"]

    for col in check_columns:
        if col not in df.columns:
            print(f"⚠️ 未找到列：{col}")
            continue

        # 标记重复值（包括首次出现）
        duplicated = df[col].duplicated(keep=False)
        duplicate_values = df.loc[duplicated, col].dropna().unique()

        if len(duplicate_values) == 0:
            print(f"✅ 列【{col}】没有重复值。")
        else:
            print(f"\n🔁 列【{col}】存在重复内容，共 {len(duplicate_values)} 个：")
            for val in duplicate_values:
                row_indices = df[df[col] == val].index.tolist()
                row_numbers = [i + 2 for i in row_indices]  # Excel 从第2行开始是数据
                print(f"  ➤ 值: {val}   ➟ 出现于行: {row_numbers}")


if __name__ == '__main__':
    # 示例调用
    file_path = "/Users/zkp/Desktop/B&Y/fxb_unpaid.xlsx"
    find_column_duplicates(file_path)