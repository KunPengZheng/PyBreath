import pandas as pd
import numpy as np


def copy(
        file1_path,
        file2_path,
        output_path,
        lunbotu,
        color_value="Black",
        stock_quantity=60
):
    df1 = pd.read_excel(file1_path, header=None, dtype=str)
    df2 = pd.read_excel(file2_path, dtype=str)

    valid_columns = df1.dropna(axis=1, how='all')
    total_valid_cols = valid_columns.shape[1]
    cols_to_copy = total_valid_cols - 3
    if cols_to_copy <= 0:
        print("❌ 有效列不足")
        return

    k_values = df1.iloc[:, 3:3 + cols_to_copy].values.flatten()
    k_values = [v for v in k_values if pd.notna(v) and str(v).strip() != ""]

    repeated_a_values = []
    repeated_b_values = []
    repeated_d_values = []

    for _, row in df1.iterrows():
        repeated_a_values.extend([str(row[2])] * cols_to_copy)  # file1 的 C → A
        repeated_b_values.extend([str(row[1])] * cols_to_copy)  # file1 的 B → C/T/S
        repeated_d_values.extend([str(row[0])] * cols_to_copy)  # file1 的 A → D

    size_labels = ["S", "M", "L", "XL", "XXL", "XXXL", "XXXXL", "XXXXXL", "XXXXXXL"]
    h_values = size_labels[:cols_to_copy]

    while len(df2.columns) <= 25:
        df2[df2.columns[-1] + "_"] = ""

    col_A, col_B, col_C = df2.columns[0], df2.columns[1], df2.columns[2]
    col_E, col_F = df2.columns[4], df2.columns[5]
    col_G, col_H, col_J, col_K = df2.columns[6], df2.columns[7], df2.columns[9], df2.columns[10]
    col_L, col_M, col_N, col_O = df2.columns[11], df2.columns[12], df2.columns[13], df2.columns[14]
    col_S, col_T = df2.columns[18], df2.columns[19]
    col_Y, col_Z = df2.columns[24], df2.columns[25]

    empty_k_rows = df2[df2[col_K].isna() | (df2[col_K].astype(str).str.strip() == "")].index

    for i in range(len(k_values)):
        val_k = str(k_values[i])
        val_a = repeated_a_values[i] if i < len(repeated_a_values) else ""
        val_b = repeated_b_values[i] if i < len(repeated_b_values) else ""
        val_d = repeated_d_values[i] if i < len(repeated_d_values) else ""
        val_h = h_values[i % len(h_values)]

        if i < len(empty_k_rows):
            row_idx = empty_k_rows[i]
        else:
            row_idx = len(df2)
            df2.loc[row_idx] = [np.nan] * len(df2.columns)

        df2.at[row_idx, col_A] = val_a  # file1 的 C → A
        df2.at[row_idx, col_B] = val_a  # file1 的 C → B
        df2.at[row_idx, col_C] = val_b  # file1 的 B → C
        df2.at[row_idx, df2.columns[3]] = val_d  # ✅ file1 的 A → D
        df2.at[row_idx, col_T] = val_b  # file1 的 B → T
        df2.at[row_idx, col_S] = str(val_b) + lunbotu  # file1 的 B + 图片 → S

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

    df2.to_excel(output_path, index=False)
    print(f"✅ 数据已处理并保存到: {output_path}")


if __name__ == '__main__':
    # 示例用法（替换路径）
    file1 = "/Users/zkp/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/aee968804ccf60699f2aada7c6e578a8/Message/MessageTemp/ef759ea81cdfa1cb6fec129aebe95142/File/白色女装P951-P953(2).xlsx"
    file2 = "/Users/zkp/Documents/import_created_product_popTemu_副本.xlsx"
    output = "/Users/zkp/Documents/result5555.xlsx"

    lunbotu_white = "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101012/616145e8af459c7495758a9aec2e5f37.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101012/db23824b806321f7b39f43137994f780.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101013/54570e517207968339038e80969780b9.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101014/2a1066b0bf75ae5c0ae23e580448c986.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101015/ce1447f258253c875aa2b0b4883b59b1.jpg"

    # lunbotu_black = "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101016/98e779932fa49e38c4b95fb57b13393a.jpg" \
    #                 "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101016/957edc530ac9905385533f9c0f4eb7bc.jpg" \
    #                 "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101017/bff7b4be4481c5c6e11d2edf1a8d9fc6.jpg" \
    #                 "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101017/17666fe45e9b5f1254135febbd624721.jpg" \
    #                 "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101018/d4acb5ca0dce2d7be4fc88a00ce00b44.jpg"

    white = "White"
    black = "Black"

    copy(
        file1_path=file1,
        file2_path=file2,
        output_path=output,
        lunbotu=lunbotu_white,
        color_value=white,  # 可变参数
        stock_quantity=77.1  # 可变参数
    )
