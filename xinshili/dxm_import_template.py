import numpy as np
import pandas as pd
import re
import random
from dataclasses import dataclass
from xinshili import utils
from xinshili.yifu_pupin import rule_replace


@dataclass(frozen=True)
class Combined:
    White = '白'
    Black = '黑'
    Man = '男'
    Women = '女'
    Nones = '未知'


comfort_descriptions = [
    "Made to move with you",
    "Feather-light comfort",
    "Soft like second skin",
    "Built for all-day wear",
    "So soft, you'll forget it's there",
    "Comfort in every thread",
    "Feel the difference",
    "Breathable. Beautiful.",
    "Easy on your skin",
    "Fabric that loves you back",
    "Light on body, big on comfort",
    "Touchably soft",
    "Wears like a dream",
    "Silky smooth feel",
    "Stays cool, feels fresh",
    "Seamless comfort",
    "Every fiber matters",
    "Cozy meets classy",
    "Cloud-level softness",
    "Effortless on the inside",
    "Made for comfort days",
    "Simple, but never basic",
    "Quality you can feel",
    "So good, you’ll want two",
    "Fits like a favorite",
    "Stretch without squeeze",
    "All comfort, no fuss",
    "Soft enough to sleep in",
    "Fabric that breathes",
    "Gentle on your day",
    "Cool to the touch",
    "Not too loose, not too tight",
    "Sensibly soft",
    "Stay comfy, stay you",
    "The tee you’ll reach for",
    "Skin-first softness",
    "The luxury of ease",
    "Casual, but elevated",
    "Feels better with every wear",
    "Comfort is the new style",
    "Touch of smooth perfection",
    "Never itchy, always easy",
    "Styled for softness",
    "Laidback luxury",
    "Perfectly relaxed",
    "Comfort that lasts",
    "All-season softness",
    "Just-right fit, every time",
    "Wear it once, love it forever",
    "Tailored for feel-good days"
]

scene_descriptions = [
    "Ready for anything",
    "Wear it everywhere",
    "Effortless from AM to PM",
    "Desk to dinner approved",
    "Chic on the go",
    "Your weekend go-to",
    "Just right for travel days",
    "Easy fit, easy vibe",
    "Perfect for every plan",
    "From couch to coffee shop",
    "Looks great, feels better",
    "WFH essential",
    "Sunday brunch style",
    "Always in style, never too much",
    "Pair with anything",
    "Versatility in a tee",
    "A tee for every mood",
    "Comfy enough for errands",
    "Made for slow days",
    "Gym to grocery ready",
    "Layer it or love it solo",
    "Fits your schedule",
    "Great for daily wear",
    "Your everyday essential",
    "Minimal look, maximum use",
    "One tee, endless outfits",
    "Weekend-ready wear",
    "Made for morning walks",
    "Ideal for laid-back days",
    "Works with denim, skirts, joggers",
    "Stylish in any setting",
    "Casual doesn’t mean careless",
    "From airport to afterparty",
    "Dress it up or down",
    "Always the right choice",
    "Low effort, high reward",
    "Wherever you go, it fits",
    "Built for your lifestyle",
    "Timeless and wearable",
    "Comfort that travels",
    "All-day style, every day",
    "Chic in seconds",
    "Wherever life takes you",
    "Great for layering",
    "Just add jeans",
    "From sunrise to streetlight",
    "Keep it casual, keep it cool",
    "One and done",
    "Ready when you are",
    "Made to match your moments"
]


def ends_with_punctuation(sentence):
    sentence = sentence.strip()
    return sentence[-1] in {'.', '!', '?'} if sentence else False


def normalize_punctuation_spacing(content, category_keyword):
    # 定义要处理的标点符号（常见英文标点）
    punctuations = [",", "\\.", "!", "\\?", ";", ":"]

    # 构造正则表达式：匹配标点符号后无空格 或 多空格 的情况
    pattern = re.compile(r"({})(?=\S)|({})\s{{2,}}".format("|".join(punctuations), "|".join(punctuations)))

    replaced_text = rule_replace(content, False)

    content_category_keyword = ""
    if ends_with_punctuation(replaced_text):
        content_category_keyword = replaced_text + " " + category_keyword
    else:
        content_category_keyword = replaced_text + ". " + category_keyword

    def fix_spacing(text):
        # 标准化空格（标点后添加一个空格）
        text = pattern.sub(lambda m: m.group(0)[0] + " ", text)

        # 删除多余的空格（多个空格 → 一个空格）
        text = re.sub(r'\s{2,}', ' ', text)

        # 去除开头/结尾空格
        return text.strip()

    return fix_spacing(content_category_keyword)


def copy(
        file1_path: object,
        file2_path: object,
        output_path: object,
        lunbotu: object,
        category_keyword,
        color_value: object,
        stock_quantity: object,
        repertory: object,
        length: object,
        width: object,
        height: object,
        weight: object
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

        val_a_result = normalize_punctuation_spacing(val_a, category_keyword)

        df2.at[row_idx, col_A] = val_a_result  # file1 的 C → A
        df2.at[row_idx, col_B] = val_a_result  # file1 的 C → B
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
        df2.at[row_idx, col_L] = length
        df2.at[row_idx, col_M] = width
        df2.at[row_idx, col_N] = height
        df2.at[row_idx, col_O] = weight
        df2.at[row_idx, col_Y] = repertory
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


def handler(src_path, price, repertorys, w_front_no_design_Flag=False):
    file_name_with_extension = utils.get_filename_with_extension(src_path)
    color_flag, gender_flag = detect_keywords(file_name_with_extension)
    if color_flag == Combined.Nones or gender_flag == Combined.Nones:
        raise ValueError(f"文件名不存在 '男女'或'黑白' 等关键字！！！")

    # 直接使用路径，不用 openpyxl_utils
    template_path = utils.current_dir() + "/xlsx/dxm/import_created_product_popTemu.xlsx"
    output_dir = "/Users/zkp/Desktop/B&Y/dxm/"
    output = f"{output_dir}{file_name_with_extension}"

    sex_man = "2025 Men's T-shirt"
    sex_women = "2025 Women's T-shirt"
    result_sex = sex_man if gender_flag == Combined.Man else sex_women

    result_color = "White" if color_flag == Combined.White else "Black"

    lunbotu_white = "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101012/616145e8af459c7495758a9aec2e5f37.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101012/db23824b806321f7b39f43137994f780.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101013/54570e517207968339038e80969780b9.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101014/2a1066b0bf75ae5c0ae23e580448c986.jpg" \
                    "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101015/ce1447f258253c875aa2b0b4883b59b1.jpg"

    lunbotu_white_front_no_design = \
        "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250523145428/c8a045cad46f8706729202360061d4e4.jpg" \
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
        if w_front_no_design_Flag:
            result_lbt = lunbotu_white_front_no_design
        else:
            result_lbt = lunbotu_white
    else:
        result_lbt = lunbotu_black

    lengths = ""
    widths = ""
    heights = ""
    weights = ""
    if gender_flag == Combined.Man:
        lengths = "35"
        widths = "25"
        heights = "1"
        weights = "130"
    else:
        lengths = "20"
        widths = "15"
        heights = "2"
        weights = "180"

    copy(
        file1_path=src_path,
        file2_path=template_path,  # 现在是字符串路径了 ✅
        output_path=output,
        lunbotu=result_lbt,
        category_keyword=result_sex,
        color_value=result_color,
        stock_quantity=price,
        repertory=repertorys,
        length=lengths,
        width=widths,
        height=heights,
        weight=weights
    )

    utils.open_dir(output_dir)


# def check_column_duplicates(file_path):
#     df = pd.read_excel(file_path, dtype=str)
#     flag = False
#
#     for col_index, col in enumerate(df.columns):
#         duplicated = df[col].duplicated(keep=False)  # 标记所有重复项
#         if duplicated.any():
#             flag = True
#             # print(f"✅ 第 {col_index + 1} 列（列名：{col}）存在重复值。")
#             print(f"✅ 第 {col_index + 1} 列 存在重复值：")
#
#             # 获取重复值及其行号
#             duplicate_values = df.loc[duplicated, col].dropna().unique()
#
#             for val in duplicate_values:
#                 row_indices = df[df[col] == val].index.tolist()
#                 row_numbers = [i + 2 for i in row_indices]  # Excel 的行号从 2 开始（包含标题）
#                 print(f"   🔁 重复行为: {row_numbers}    重复值为: {val}")
#
#     return flag


def check_column_duplicates(file_path, output_path):
    # 没有列名的 Excel 读取方式
    df = pd.read_excel(file_path, dtype=str, header=None)
    flag = False
    third_col_modified = False

    for col_index in range(df.shape[1]):
        duplicated = df[col_index].duplicated(keep=False)
        if duplicated.any():
            duplicate_values = df.loc[duplicated, col_index].dropna().unique()

            # ✅ 第三列：自动修改重复内容
            if col_index == 2:
                print(f"✅ 第 {col_index + 1} 列存在重复值，将自动修改：")
                for val in duplicate_values:
                    row_indices = df[df[col_index] == val].index.tolist()
                    row_numbers = [i + 1 for i in row_indices]  # Excel 中从第 1 行开始
                    print(f"   🔁 重复行为: {row_numbers}    重复值为: {val}")

                existing_values = set(df[col_index].dropna())

                for val in duplicate_values:
                    indices = df[df[col_index] == val].index.tolist()
                    for i in indices[1:]:  # 修改除第一个外的所有
                        attempts = 0
                        new_val = val
                        while new_val in existing_values and attempts < 100:
                            suffix = random.choice(comfort_descriptions) + ", " + random.choice(scene_descriptions)

                            if ends_with_punctuation(val):
                                new_val = f"{val} {suffix}"
                            else:
                                new_val = f"{val}. {suffix}"

                            attempts += 1
                        if new_val not in existing_values:
                            original_val = df.at[i, col_index]
                            df.at[i, col_index] = new_val
                            existing_values.add(new_val)
                            third_col_modified = True
                            # print(f"   ✏️ 行 {i + 1}：{original_val} ➜ {new_val}")
                            print(f"   ✏️ 行 {i + 1}：{new_val}")

                if third_col_modified:
                    try:
                        df.to_excel(output_path, index=False, header=False)
                        print("✨ 第三列重复值已自动修改并保存。")
                    except PermissionError as e:
                        print(f"❌ 写入失败（权限问题）：{e}")
                continue  # 第三列已自动处理，不算错误

            # ✅ 其他列：标记重复但不自动处理
            flag = True
            print(f"✅ 第 {col_index + 1} 列存在重复值：")
            for val in duplicate_values:
                row_indices = df[df[col_index] == val].index.tolist()
                row_numbers = [i + 1 for i in row_indices]
                print(f"   🔁 重复行为: {row_numbers}    重复值为: {val}")

    return flag, third_col_modified


if __name__ == '__main__':
    source_file = input("请输入源表文件的绝对路径：")
    file_dir = utils.get_file_dir(source_file)
    filename = utils.get_filename_without_extension(source_file)
    ext = utils.get_file_ext(source_file)

    ignore_io_permission = file_dir + "/" + filename + "_modify_title_column" + ext

    flag, third_col_modified = check_column_duplicates(source_file, ignore_io_permission)

    price = 57
    repertorys = 800
    w_front_no_design_Flag = False

    if third_col_modified:
        handler(ignore_io_permission, price, repertorys, w_front_no_design_Flag)
    else:
        if flag:
            print("⚠️ 源文件的某列存在重复内容，已终止后续处理。")
        else:
            print("🎉 源文件所有列均无重复内容")
            handler(source_file, price, repertorys, w_front_no_design_Flag)
