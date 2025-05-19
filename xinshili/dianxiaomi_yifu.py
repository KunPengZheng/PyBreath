import numpy as np
import pandas as pd
import re
from dataclasses import dataclass
from xinshili import utils, openpyxl_utils


@dataclass(frozen=True)
class Combined:
    White = '白'
    Black = '黑'
    Man = '男'
    Women = '女'
    Nones = '未知'


def normalize_punctuation_spacing(content, category_keyword):
    # 定义要处理的标点符号（常见英文标点）
    punctuations = [",", "\\.", "!", "\\?", ";", ":"]

    # 构造正则表达式：匹配标点符号后无空格 或 多空格 的情况
    pattern = re.compile(r"({})(?=\S)|({})\s{{2,}}".format("|".join(punctuations), "|".join(punctuations)))

    def fix_spacing(text, ):
        if not isinstance(text, str):
            return text + f"{category_keyword}"

        # 标准化空格（标点后添加一个空格）
        text = pattern.sub(lambda m: m.group(0)[0] + " ", text)

        # 删除多余的空格（多个空格 → 一个空格）
        text = re.sub(r'\s{2,}', ' ', text)

        text = text + f"{category_keyword}"

        # 去除开头/结尾空格
        return text.strip()

    return fix_spacing(content)


def copy(
        file1_path: object,
        file2_path: object,
        output_path: object,
        lunbotu: object,
        category_keyword,
        color_value: object,
        stock_quantity: object = 77.1
) -> object:
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

        normalize_punctuation_spacing(val_a, category_keyword)

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


def detect_keywords(content):
    # 判断颜色
    if Combined.White in content:
        color_flag = Combined.White
    elif Combined.Black in content:
        color_flag = Combined.Black
    else:
        color_flag = Combined.Nones

    # 判断性别
    if Combined.Man in content:
        gender_flag = Combined.Man
    elif Combined.Women in content:
        gender_flag = Combined.Women
    else:
        gender_flag = Combined.Nones

    return color_flag, gender_flag


def handler(src_path):
    file_name_with_extension = utils.get_filename_with_extension(src_path)
    color_flag, gender_flag = detect_keywords(file_name_with_extension)
    if color_flag == Combined.Nones or gender_flag == Combined.Nones:
        raise ValueError(f"文件名不存在 '男女'或'黑白' 等关键字！！！")

    template_path = openpyxl_utils.load_excel_file(
        utils.current_dir() + "/xlsx/dxm/import_created_product_popTemu.xlsx")
    output = f"/Users/zkp/Desktop/B&Y/dxm/{file_name_with_extension}"

    sex_man = ". 2025 Men's T-shirt"
    sex_women = ". 2025 Women's T-shirt"
    result_sex = ""
    if color_flag == Combined.Man:
        result_sex = sex_man
    else:
        result_sex = sex_women

    white = "White"
    black = "Black"
    result_color = ""
    if color_flag == Combined.White:
        result_color = white
    else:
        result_color = black

    lunbotu_white = "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101012/616145e8af459c7495758a9aec2e5f37.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101012/db23824b806321f7b39f43137994f780.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101013/54570e517207968339038e80969780b9.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101014/2a1066b0bf75ae5c0ae23e580448c986.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101015/ce1447f258253c875aa2b0b4883b59b1.jpg"

    lunbotu_black = "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101016/98e779932fa49e38c4b95fb57b13393a.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101016/957edc530ac9905385533f9c0f4eb7bc.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101017/bff7b4be4481c5c6e11d2edf1a8d9fc6.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101017/17666fe45e9b5f1254135febbd624721.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101018/d4acb5ca0dce2d7be4fc88a00ce00b44.jpg"
    result_lbt = ""
    if color_flag == Combined.White:
        result_lbt = lunbotu_white
    else:
        result_lbt = lunbotu_black

    copy(
        file1_path=src_path,
        file2_path=template_path,
        output_path=output,
        lunbotu=result_lbt,
        category_keyword=result_sex,
        color_value=result_color
    )

    utils.open_dir(output)


if __name__ == '__main__':
    src = "/Users/zkp/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/aee968804ccf60699f2aada7c6e578a8/Message/MessageTemp/24fe1b1c873f588c7b3f70c4efe61bb7/File/白色女装Y401-500上传表格.xlsx"
    handler(src)
