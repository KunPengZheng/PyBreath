import pandas as pd
import numpy as np


def copy_columns_to_k_and_repeat_b_c_to_a_b(
        file1_path,
        file2_path,
        output_path,
        lunbotu,
        color_value="Black",
        stock_quantity=60
):
    # 读取文件
    df1 = pd.read_excel(file1_path, header=None, dtype=str)
    df2 = pd.read_excel(file2_path, dtype=str)

    # 获取有效列数
    valid_columns = df1.dropna(axis=1, how='all')
    total_valid_cols = valid_columns.shape[1]
    cols_to_copy = total_valid_cols - 3
    if cols_to_copy <= 0:
        print("❌ 有效列不足")
        return

    # 提取要填入 K 列的值
    k_values = df1.iloc[:, 3:3 + cols_to_copy].values.flatten()
    k_values = [v for v in k_values if pd.notna(v) and str(v).strip() != ""]

    # 准备填入 A 和 B 的重复值
    repeated_a_values = []
    repeated_b_values = []
    for _, row in df1.iterrows():
        repeated_a_values.extend([str(row[1])] * cols_to_copy)  # B列 → A
        repeated_b_values.extend([str(row[1])] * cols_to_copy)  # B列 → B

    # 尺寸列表
    size_labels = ["S", "M", "L", "XL", "XXL", "XXXL", "XXXXL", "XXXXXL", "XXXXXXL"]
    h_values = size_labels[:cols_to_copy]

    # 扩展 df2 至至少26列（到Z列，索引25）
    while len(df2.columns) <= 25:
        df2[df2.columns[-1] + "_"] = ""

    # 获取列名
    col_A, col_B, col_C = df2.columns[0], df2.columns[1], df2.columns[2]
    col_E, col_F = df2.columns[4], df2.columns[5]
    col_G, col_H, col_J, col_K = df2.columns[6], df2.columns[7], df2.columns[9], df2.columns[10]
    col_L, col_M, col_N, col_O = df2.columns[11], df2.columns[12], df2.columns[13], df2.columns[14]
    col_S, col_T = df2.columns[18], df2.columns[19]
    col_Y, col_Z = df2.columns[24], df2.columns[25]

    # 找空的 K 列行
    empty_k_rows = df2[df2[col_K].isna() | (df2[col_K].astype(str).str.strip() == "")].index

    for i in range(len(k_values)):
        val_k = str(k_values[i])
        val_a = repeated_a_values[i] if i < len(repeated_a_values) else ""
        val_b = repeated_b_values[i] if i < len(repeated_b_values) else ""
        val_h = h_values[i % len(h_values)]  # 尺寸循环

        if i < len(empty_k_rows):
            row_idx = empty_k_rows[i]
        else:
            row_idx = len(df2)
            df2.loc[row_idx] = [np.nan] * len(df2.columns)

        # 基本赋值
        df2.at[row_idx, col_A] = val_a
        df2.at[row_idx, col_B] = val_b
        df2.at[row_idx, col_E] = "Color"
        df2.at[row_idx, col_F] = color_value
        df2.at[row_idx, col_G] = "Size"
        df2.at[row_idx, col_H] = val_h
        df2.at[row_idx, col_J] = str(stock_quantity)
        df2.at[row_idx, col_K] = val_k
        df2.at[row_idx, col_L] = "20"
        df2.at[row_idx, col_M] = "15"
        df2.at[row_idx, col_N] = "2"
        df2.at[row_idx, col_O] = "180"
        df2.at[row_idx, col_Y] = "300"
        df2.at[row_idx, col_Z] = "2"

        # ✅ 新增要求：复制 file1 的 B列内容 到 C列、T列，并拼接到 S列
        df2.at[row_idx, col_C] = val_a  # file1 的 B → file2 的 C
        df2.at[row_idx, col_T] = val_a  # file1 的 B → file2 的 T
        # file1 的 B + "xxxx" → S
        df2.at[row_idx, col_S] = str(val_a) + lunbotu

        # 保存结果
    df2.to_excel(output_path, index=False)
    print(f"✅ 数据已处理并保存到: {output_path}")


# 示例用法（替换路径）
file1 = "/Users/zkp/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/aee968804ccf60699f2aada7c6e578a8/Message/MessageTemp/ef759ea81cdfa1cb6fec129aebe95142/File/Test-Q001-Q020.xlsx"
file2 = "/Users/zkp/Documents/import_created_product_popTemu_副本.xlsx"
output = "/Users/zkp/Documents/result1111.xlsx"

lunbotu = "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250514111809/63b0b6df8d9b39be54a6fc8c5b8bc7e7.jpg" \
          "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250514111808/892ab9494fd09b05f95d37d8c52d6aff.jpg" \
          "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250514111808/c6cc4267a5f50099aaded55b3c16ab95.jpg" \
          "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250514111808/d9432ffd685dabca4657c44c65265601.jpg" \
          "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250514111809/decb4cabfec356e545a99a098fa8d589.jpeg"

copy_columns_to_k_and_repeat_b_c_to_a_b(
    file1_path=file1,
    file2_path=file2,
    output_path=output,
    lunbotu=lunbotu,
    color_value="White",  # 可变参数
    stock_quantity=60  # 可变参数
)
