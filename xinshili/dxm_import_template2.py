# import numpy as np
# import pandas as pd
# import re
# import random
# from dataclasses import dataclass
# from xinshili import utils
# from xinshili.yifu_pupin import rule_replace
#
#
# @dataclass(frozen=True)
# class Combined:
#     White = '白'
#     Black = '黑'
#     Man = '男'
#     Women = '女'
#     Nones = '未知'
#
#
# comfort_descriptions = [
#     "Made to move with you",
#     "Feather-light comfort",
#     "Soft like second skin",
#     "Built for all-day wear",
#     "So soft, you'll forget it's there",
#     "Comfort in every thread",
#     "Feel the difference",
#     "Breathable. Beautiful.",
#     "Easy on your skin",
#     "Fabric that loves you back",
#     "Light on body, big on comfort",
#     "Touchably soft",
#     "Wears like a dream",
#     "Silky smooth feel",
#     "Stays cool, feels fresh",
#     "Seamless comfort",
#     "Every fiber matters",
#     "Cozy meets classy",
#     "Cloud-level softness",
#     "Effortless on the inside",
#     "Made for comfort days",
#     "Simple, but never basic",
#     "Quality you can feel",
#     "So good, you’ll want two",
#     "Fits like a favorite",
#     "Stretch without squeeze",
#     "All comfort, no fuss",
#     "Soft enough to sleep in",
#     "Fabric that breathes",
#     "Gentle on your day",
#     "Cool to the touch",
#     "Not too loose, not too tight",
#     "Sensibly soft",
#     "Stay comfy, stay you",
#     "The tee you’ll reach for",
#     "Skin-first softness",
#     "The luxury of ease",
#     "Casual, but elevated",
#     "Feels better with every wear",
#     "Comfort is the new style",
#     "Touch of smooth perfection",
#     "Never itchy, always easy",
#     "Styled for softness",
#     "Laidback luxury",
#     "Perfectly relaxed",
#     "Comfort that lasts",
#     "All-season softness",
#     "Just-right fit, every time",
#     "Wear it once, love it forever",
#     "Tailored for feel-good days"
# ]
#
# scene_descriptions = [
#     "Ready for anything",
#     "Wear it everywhere",
#     "Effortless from AM to PM",
#     "Desk to dinner approved",
#     "Chic on the go",
#     "Your weekend go-to",
#     "Just right for travel days",
#     "Easy fit, easy vibe",
#     "Perfect for every plan",
#     "From couch to coffee shop",
#     "Looks great, feels better",
#     "WFH essential",
#     "Sunday brunch style",
#     "Always in style, never too much",
#     "Pair with anything",
#     "Versatility in a tee",
#     "A tee for every mood",
#     "Comfy enough for errands",
#     "Made for slow days",
#     "Gym to grocery ready",
#     "Layer it or love it solo",
#     "Fits your schedule",
#     "Great for daily wear",
#     "Your everyday essential",
#     "Minimal look, maximum use",
#     "One tee, endless outfits",
#     "Weekend-ready wear",
#     "Made for morning walks",
#     "Ideal for laid-back days",
#     "Works with denim, skirts, joggers",
#     "Stylish in any setting",
#     "Casual doesn’t mean careless",
#     "From airport to afterparty",
#     "Dress it up or down",
#     "Always the right choice",
#     "Low effort, high reward",
#     "Wherever you go, it fits",
#     "Built for your lifestyle",
#     "Timeless and wearable",
#     "Comfort that travels",
#     "All-day style, every day",
#     "Chic in seconds",
#     "Wherever life takes you",
#     "Great for layering",
#     "Just add jeans",
#     "From sunrise to streetlight",
#     "Keep it casual, keep it cool",
#     "One and done",
#     "Ready when you are",
#     "Made to match your moments"
# ]
#
#
# def ends_with_punctuation(sentence):
#     sentence = sentence.strip()
#     return sentence[-1] in {'.', '!', '?'} if sentence else False
#
#
# def normalize_punctuation_spacing(content, category_keyword):
#     # 定义要处理的标点符号（常见英文标点）
#     punctuations = [",", "\\.", "!", "\\?", ";", ":"]
#
#     # 构造正则表达式：匹配标点符号后无空格 或 多空格 的情况
#     pattern = re.compile(r"({})(?=\S)|({})\s{{2,}}".format("|".join(punctuations), "|".join(punctuations)))
#
#     replaced_text = rule_replace(content, False)
#
#     content_category_keyword = ""
#     if ends_with_punctuation(replaced_text):
#         content_category_keyword = replaced_text + " " + category_keyword
#     else:
#         content_category_keyword = replaced_text + ". " + category_keyword
#
#     def fix_spacing(text):
#         # 标准化空格（标点后添加一个空格）
#         text = pattern.sub(lambda m: m.group(0)[0] + " ", text)
#
#         # 删除多余的空格（多个空格 → 一个空格）
#         text = re.sub(r'\s{2,}', ' ', text)
#
#         # 去除开头/结尾空格
#         return text.strip()
#
#     return fix_spacing(content_category_keyword)
#
#
# def copy(
#         file1_path: object,
#         file2_path: object,
#         output_path: object,
#         lunbotu: object,
#         category_keyword,
#         color_value: object,
#         stock_quantity: object,
#         repertory: object,
# ) -> object:
#     df1 = pd.read_excel(file1_path, header=None, dtype=str)
#     df2 = pd.read_excel(file2_path, dtype=str)
#
#     valid_columns = df1.dropna(axis=1, how='all')
#     total_valid_cols = valid_columns.shape[1]
#     cols_to_copy = total_valid_cols - 3
#     if cols_to_copy <= 0:
#         print("❌ 有效列不足")
#         return
#
#     k_values = df1.iloc[:, 3:3 + cols_to_copy].values.flatten()
#     k_values = [v for v in k_values if pd.notna(v) and str(v).strip() != ""]
#
#     repeated_a_values = []
#     repeated_b_values = []
#     repeated_d_values = []
#
#     for _, row in df1.iterrows():
#         repeated_a_values.extend([str(row[2])] * cols_to_copy)  # file1 的 C → A
#         repeated_b_values.extend([str(row[1])] * cols_to_copy)  # file1 的 B → C/T/S
#         repeated_d_values.extend([str(row[0])] * cols_to_copy)  # file1 的 A → D
#
#     size_labels = ["S", "M", "L", "XL", "XXL", "XXXL", "XXXXL", "XXXXXL", "XXXXXXL"]
#     h_values = size_labels[:cols_to_copy]
#
#     while len(df2.columns) <= 25:
#         df2[df2.columns[-1] + "_"] = ""
#
#     col_A, col_B, col_C = df2.columns[0], df2.columns[1], df2.columns[2]
#     col_E, col_F = df2.columns[4], df2.columns[5]
#     col_G, col_H, col_J, col_K = df2.columns[6], df2.columns[7], df2.columns[9], df2.columns[10]
#     col_L, col_M, col_N, col_O = df2.columns[11], df2.columns[12], df2.columns[13], df2.columns[14]
#     col_S, col_T = df2.columns[18], df2.columns[19]
#     col_Y, col_Z = df2.columns[24], df2.columns[25]
#
#     empty_k_rows = df2[df2[col_K].isna() | (df2[col_K].astype(str).str.strip() == "")].index
#
#     for i in range(len(k_values)):
#         val_k = str(k_values[i])
#         val_a = repeated_a_values[i] if i < len(repeated_a_values) else ""
#         val_b = repeated_b_values[i] if i < len(repeated_b_values) else ""
#         val_d = repeated_d_values[i] if i < len(repeated_d_values) else ""
#         val_h = h_values[i % len(h_values)]
#
#         if i < len(empty_k_rows):
#             row_idx = empty_k_rows[i]
#         else:
#             row_idx = len(df2)
#             df2.loc[row_idx] = [np.nan] * len(df2.columns)
#
#         val_a_result = normalize_punctuation_spacing(val_a, category_keyword)
#
#         df2.at[row_idx, col_A] = val_a_result  # file1 的 C → A
#         df2.at[row_idx, col_B] = val_a_result  # file1 的 C → B
#         df2.at[row_idx, col_C] = val_b  # file1 的 B → C
#         df2.at[row_idx, df2.columns[3]] = val_d  # ✅ file1 的 A → D
#         df2.at[row_idx, col_T] = val_b  # file1 的 B → T
#         df2.at[row_idx, col_S] = str(val_b) + lunbotu  # file1 的 B + 图片 → S
#
#         df2.at[row_idx, col_E] = "Color"
#         df2.at[row_idx, col_F] = color_value
#         df2.at[row_idx, col_G] = "Size"
#         df2.at[row_idx, col_H] = val_h
#         df2.at[row_idx, col_J] = str(stock_quantity)
#         df2.at[row_idx, col_K] = val_k
#         df2.at[row_idx, col_L] = "20"
#         df2.at[row_idx, col_M] = "15"
#         df2.at[row_idx, col_N] = "2"
#         df2.at[row_idx, col_O] = "180"
#         df2.at[row_idx, col_Y] = repertory
#         df2.at[row_idx, col_Z] = "2"
#
#     df2.to_excel(output_path, index=False)
#     print(f"✅ 数据已处理并保存到: {output_path}")
#
#
# def detect_keywords(content):
#     # 判断颜色
#     if Combined.White in content:
#         color_flag = Combined.White
#     elif Combined.Black in content:
#         color_flag = Combined.Black
#     else:
#         color_flag = Combined.Nones
#
#     # 判断性别
#     if Combined.Man in content:
#         gender_flag = Combined.Man
#     elif Combined.Women in content:
#         gender_flag = Combined.Women
#     else:
#         gender_flag = Combined.Nones
#
#     return color_flag, gender_flag
#
#
# def handler(src_path, price, repertorys, w_front_no_design_Flag=False):
#     file_name_with_extension = utils.get_filename_with_extension(src_path)
#     color_flag, gender_flag = detect_keywords(file_name_with_extension)
#     if color_flag == Combined.Nones or gender_flag == Combined.Nones:
#         raise ValueError(f"文件名不存在 '男女'或'黑白' 等关键字！！！")
#
#     # 直接使用路径，不用 openpyxl_utils
#     template_path = utils.current_dir() + "/xlsx/dxm/import_created_product_popTemu.xlsx"
#     output_dir = "/Users/zkp/Desktop/B&Y/dxm/"
#     output = f"{output_dir}{file_name_with_extension}"
#
#     sex_man = "2025 Men's T-shirt"
#     sex_women = "2025 Women's T-shirt"
#     result_sex = sex_man if gender_flag == Combined.Man else sex_women
#
#     result_color = "White" if color_flag == Combined.White else "Black"
#
#     lunbotu_white = "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101012/616145e8af459c7495758a9aec2e5f37.jpg" \
#                     "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101012/db23824b806321f7b39f43137994f780.jpg" \
#                     "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101013/54570e517207968339038e80969780b9.jpg" \
#                     "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101014/2a1066b0bf75ae5c0ae23e580448c986.jpg" \
#                     "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101015/ce1447f258253c875aa2b0b4883b59b1.jpg"
#
#     lunbotu_white_front_no_design = \
#         "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250523145428/c8a045cad46f8706729202360061d4e4.jpg" \
#         "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101012/db23824b806321f7b39f43137994f780.jpg" \
#         "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101013/54570e517207968339038e80969780b9.jpg" \
#         "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101014/2a1066b0bf75ae5c0ae23e580448c986.jpg" \
#         "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101015/ce1447f258253c875aa2b0b4883b59b1.jpg"
#
#     lunbotu_black = "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101016/98e779932fa49e38c4b95fb57b13393a.jpg" \
#                     "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101016/957edc530ac9905385533f9c0f4eb7bc.jpg" \
#                     "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101017/bff7b4be4481c5c6e11d2edf1a8d9fc6.jpg" \
#                     "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101017/17666fe45e9b5f1254135febbd624721.jpg" \
#                     "\nhttps://wxalbum-10001658.image.myqcloud.com/wxalbum/1573179/20250515101018/d4acb5ca0dce2d7be4fc88a00ce00b44.jpg"
#
#     result_lbt = ""
#     if color_flag == Combined.White:
#         if w_front_no_design_Flag:
#             result_lbt = lunbotu_white_front_no_design
#         else:
#             result_lbt = lunbotu_white
#     else:
#         result_lbt = lunbotu_black
#
#     #####################################
#     #####################################
#     white_product_description = """
#         <img src="https://img.kwcdn.com/product/open/795b98429fa74638ae585568abfed1d6-goods.jpeg"/><br><p>This is a 100% cotton product designed for women. It features a special treatment to prevent shrinking, ensuring it remains beautiful and durable. The styles and colors are classic, making it simple yet fashionable, and it is easy to wear and versatile. Crafted from high-quality pure cotton fabric, it has a soft texture that feels comfortable against the skin. The round neck design is tailored to fit the body's natural curves without losing shape.</p><br><img src="https://img.kwcdn.com/product/open/2069dc3094e249949018d85b44bab0ee-goods.jpeg"/><br><img src="https://img.kwcdn.com/product/open/3c305c2c4bb54d828dd9f7d65e72ae70-goods.jpeg"/><br><img src="https://img.kwcdn.com/product/open/8c59f979f9ba4a27ae2bc93b5b3138c8-goods.jpeg"/>
#         """
#
#     black_product_description = """
#        <img src="https://img.kwcdn.com/product/open/795b98429fa74638ae585568abfed1d6-goods.jpeg"/><br><p>This is a 100% cotton product designed for women. It features a special treatment to prevent shrinking, ensuring it remains beautiful and durable. The styles and colors are classic, making it simple yet fashionable, and it is easy to wear and versatile. Crafted from high-quality pure cotton fabric, it has a soft texture that feels comfortable against the skin. The round neck design is tailored to fit the body's natural curves without losing shape.</p><br><img src="https://img.kwcdn.com/product/open/2069dc3094e249949018d85b44bab0ee-goods.jpeg"/><br><img src="https://img.kwcdn.com/product/open/3c305c2c4bb54d828dd9f7d65e72ae70-goods.jpeg"/><br><img src="https://img.kwcdn.com/product/open/8c59f979f9ba4a27ae2bc93b5b3138c8-goods.jpeg"/>
#         """
#
#     product_attribute = """
#     [{"propName":"里料纹理","refPid":6928,"pid":2050,"templatePid":1396039,"numberInputValue":"","valueUnit":"","vid":"161112","propValue":"无里料/无内衬"},{"propName":"面料纹理1","refPid":6926,"pid":2054,"templatePid":1396037,"numberInputValue":"","valueUnit":"","vid":"161198","propValue":"光面"},{"propName":"面料克重1（g/m²)","refPid":6930,"pid":2052,"templatePid":1396040,"numberInputValue":"","valueUnit":"g/㎡","vid":0,"propValue":"180"},{"propName":"织造方式","refPid":1192,"pid":1224,"templatePid":1396034,"numberInputValue":"","valueUnit":"","vid":"54654","propValue":"针织(含钩织、毛织面料)"},{"propName":"款式来源","refPid":2103,"pid":1514,"templatePid":1396033,"numberInputValue":"","valueUnit":"","vid":"70453","propValue":"现货款"},{"propName":"印花类型","refPid":1919,"pid":1437,"templatePid":1396031,"numberInputValue":"","valueUnit":"","vid":"36893","propValue":"定位印花"},{"propName":"成分","refPid":15,"pid":2,"templatePid":1396013,"numberInputValue":"100.00","valueUnit":"%","vid":"35391","propValue":"棉Cotton"},{"propName":"面料弹性","refPid":1352,"pid":1364,"templatePid":1396030,"numberInputValue":"","valueUnit":"","vid":"35197","propValue":"微弹"},{"propName":"护理说明","refPid":20,"pid":4,"templatePid":1396027,"numberInputValue":"","valueUnit":"","vid":"26003","propValue":"数码印花类可机洗且不可干洗"},{"propName":"风格","refPid":19,"pid":3,"templatePid":1396028,"numberInputValue":"","valueUnit":"","vid":"145","propValue":"休闲"},{"propName":"季节","refPid":76,"pid":24,"templatePid":1396026,"numberInputValue":"","valueUnit":"","vid":"645","propValue":"ALL/全球/所有"},{"propName":"是否透明","refPid":24,"pid":7,"templatePid":1396022,"numberInputValue":"","valueUnit":"","vid":"210","propValue":"否"},{"propName":"图案","refPid":26,"pid":10,"templatePid":1396021,"numberInputValue":"","valueUnit":"","vid":"216","propValue":"几何图案"},{"propName":"细节","refPid":83,"pid":21,"templatePid":1396020,"numberInputValue":"","valueUnit":"","vid":"29210","propValue":"无"},{"propName":"材质","refPid":12,"pid":1,"templatePid":1396014,"numberInputValue":"","valueUnit":"","vid":"49","propValue":"棉"}]
#     """
#
#     spu_attribute = """
#     [{"parentSpecId":1001,"parentSpecName":"颜色","propName":"颜色","templatePid":1396012,"pid":13,"refPid":63,"valueUnit":"","vid":376,"propValue":"白色","specId":2001,"specName":"白色","valueGroupId":1,"valueGroupName":"白色系"},{"parentSpecId":3001,"parentSpecName":"尺码","propName":"尺码","templatePid":1396011,"pid":14,"refPid":65,"valueUnit":"","vid":315,"propValue":"S","specId":10004,"specName":"S","valueGroupId":2,"valueGroupName":"中国码"},{"parentSpecId":3001,"parentSpecName":"尺码","propName":"尺码","templatePid":1396011,"pid":14,"refPid":65,"valueUnit":"","vid":317,"propValue":"M","specId":9005,"specName":"M","valueGroupId":2,"valueGroupName":"中国码"},{"parentSpecId":3001,"parentSpecName":"尺码","propName":"尺码","templatePid":1396011,"pid":14,"refPid":65,"valueUnit":"","vid":319,"propValue":"L","specId":11002,"specName":"L","valueGroupId":2,"valueGroupName":"中国码"},{"parentSpecId":3001,"parentSpecName":"尺码","propName":"尺码","templatePid":1396011,"pid":14,"refPid":65,"valueUnit":"","vid":320,"propValue":"XL","specId":12003,"specName":"XL","valueGroupId":2,"valueGroupName":"中国码"},{"parentSpecId":3001,"parentSpecName":"尺码","propName":"尺码","templatePid":1396011,"pid":14,"refPid":65,"valueUnit":"","vid":321,"propValue":"XXL","specId":8002,"specName":"XXL","valueGroupId":2,"valueGroupName":"中国码"}]
#     """
#
#     # 需要修改
#     skc_attribute = """
#     [{"parentSpecId":1001,"parentSpecName":"颜色","specId":2001,"specName":"白色","extCode":"","productSkcId":"","previewImgUrls":"https://img.kwcdn.com/product/open/ad67b6489a3242e28b982db62e9e1fd2-goods.jpeg|https://img.kwcdn.com/product/open/a7caa5c138f84287b8a488896ed91331-goods.jpeg|https://img.kwcdn.com/product/open/392582400dc240d8a944a63a54806a63-goods.jpeg|https://img.kwcdn.com/product/open/da9599bf70d64ea8afdf7781c577a96e-goods.jpeg|https://img.kwcdn.com/product/open/38fdac23328c45dd9efe4e3f641c8d22-goods.jpeg|https://img.kwcdn.com/product/open/33c3fd1d2e544001b0ca39afab41b905-goods.jpeg"}]
#     """
#
#     # 需要修改
#     sku_attribute = """
#     [{"specId":2001,"parentSpecName":"颜色","specName":"白色","parentSpecId":1001},{"specId":10004,"parentSpecName":"尺码","specName":"S","parentSpecId":3001}]
#     """
#
#     #####################################
#     #####################################
#
#     copy(
#         file1_path=src_path,
#         file2_path=template_path,  # 现在是字符串路径了 ✅
#         output_path=output,
#         lunbotu=result_lbt,
#         category_keyword=result_sex,
#         color_value=result_color,
#         stock_quantity=price,
#         repertory=repertorys
#     )
#
#     utils.open_dir(output_dir)
#
#
# # def check_column_duplicates(file_path):
# #     df = pd.read_excel(file_path, dtype=str)
# #     flag = False
# #
# #     for col_index, col in enumerate(df.columns):
# #         duplicated = df[col].duplicated(keep=False)  # 标记所有重复项
# #         if duplicated.any():
# #             flag = True
# #             # print(f"✅ 第 {col_index + 1} 列（列名：{col}）存在重复值。")
# #             print(f"✅ 第 {col_index + 1} 列 存在重复值：")
# #
# #             # 获取重复值及其行号
# #             duplicate_values = df.loc[duplicated, col].dropna().unique()
# #
# #             for val in duplicate_values:
# #                 row_indices = df[df[col] == val].index.tolist()
# #                 row_numbers = [i + 2 for i in row_indices]  # Excel 的行号从 2 开始（包含标题）
# #                 print(f"   🔁 重复行为: {row_numbers}    重复值为: {val}")
# #
# #     return flag
#
#
# def check_column_duplicates(file_path, output_path):
#     # 没有列名的 Excel 读取方式
#     df = pd.read_excel(file_path, dtype=str, header=None)
#     flag = False
#     third_col_modified = False
#
#     for col_index in range(df.shape[1]):
#         duplicated = df[col_index].duplicated(keep=False)
#         if duplicated.any():
#             duplicate_values = df.loc[duplicated, col_index].dropna().unique()
#
#             # ✅ 第三列：自动修改重复内容
#             if col_index == 2:
#                 print(f"✅ 第 {col_index + 1} 列存在重复值，将自动修改：")
#                 for val in duplicate_values:
#                     row_indices = df[df[col_index] == val].index.tolist()
#                     row_numbers = [i + 1 for i in row_indices]  # Excel 中从第 1 行开始
#                     print(f"   🔁 重复行为: {row_numbers}    重复值为: {val}")
#
#                 existing_values = set(df[col_index].dropna())
#
#                 for val in duplicate_values:
#                     indices = df[df[col_index] == val].index.tolist()
#                     for i in indices[1:]:  # 修改除第一个外的所有
#                         attempts = 0
#                         new_val = val
#                         while new_val in existing_values and attempts < 100:
#                             suffix = random.choice(comfort_descriptions) + ", " + random.choice(scene_descriptions)
#
#                             if ends_with_punctuation(val):
#                                 new_val = f"{val} {suffix}"
#                             else:
#                                 new_val = f"{val}. {suffix}"
#
#                             attempts += 1
#                         if new_val not in existing_values:
#                             original_val = df.at[i, col_index]
#                             df.at[i, col_index] = new_val
#                             existing_values.add(new_val)
#                             third_col_modified = True
#                             # print(f"   ✏️ 行 {i + 1}：{original_val} ➜ {new_val}")
#                             print(f"   ✏️ 行 {i + 1}：{new_val}")
#
#                 if third_col_modified:
#                     try:
#                         df.to_excel(output_path, index=False, header=False)
#                         print("✨ 第三列重复值已自动修改并保存。")
#                     except PermissionError as e:
#                         print(f"❌ 写入失败（权限问题）：{e}")
#                 continue  # 第三列已自动处理，不算错误
#
#             # ✅ 其他列：标记重复但不自动处理
#             flag = True
#             print(f"✅ 第 {col_index + 1} 列存在重复值：")
#             for val in duplicate_values:
#                 row_indices = df[df[col_index] == val].index.tolist()
#                 row_numbers = [i + 1 for i in row_indices]
#                 print(f"   🔁 重复行为: {row_numbers}    重复值为: {val}")
#
#     return flag, third_col_modified
#
#
# if __name__ == '__main__':
#     source_file = input("请输入源表文件的绝对路径：")
#     file_dir = utils.get_file_dir(source_file)
#     filename = utils.get_filename_without_extension(source_file)
#     ext = utils.get_file_ext(source_file)
#
#     ignore_io_permission = file_dir + "/" + filename + "_modify_title_column" + ext
#
#     flag, third_col_modified = check_column_duplicates(source_file, ignore_io_permission)
#
#     price = 52
#     repertorys = 800
#     w_front_no_design_Flag = False
#
#     if third_col_modified:
#         handler(ignore_io_permission, price, repertorys, w_front_no_design_Flag)
#     else:
#         if flag:
#             print("⚠️ 源文件的某列存在重复内容，已终止后续处理。")
#         else:
#             print("🎉 源文件所有列均无重复内容")
#             handler(source_file, price, repertorys, w_front_no_design_Flag)


import pandas as pd
import re

def process_excel(file_path, output_path):
    # 读取 Excel 数据
    df = pd.read_excel(file_path, dtype=str).fillna("")

    # 尺码映射
    size_map = {
        "S": "1",
        "M": "2",
        "L": "3",
        "XL": "4",
        "XXL": "5"
    }

    # 遍历每一行处理 XXS/XS 替换
    for idx, row in df.iterrows():
        row_str = " ".join(row.values)

        # 替换 XXS → XXL，10002 → 8002
        if "XXS" in row_str:
            df.loc[idx] = df.loc[idx].apply(
                lambda x: x.replace("XXS", "XXL") if isinstance(x, str) else x
            )
            df.loc[idx] = df.loc[idx].apply(
                lambda x: x.replace("10002", "8002") if isinstance(x, str) else x
            )

        # 替换 XS → XL，12001 → 12003
        if "XS" in row_str:
            df.loc[idx] = df.loc[idx].apply(
                lambda x: x.replace("XS", "XL") if isinstance(x, str) else x
            )
            df.loc[idx] = df.loc[idx].apply(
                lambda x: x.replace("12001", "12003") if isinstance(x, str) else x
            )

    # 变种属性值二与 SKU货号 调整
    if "变种属性值二" in df.columns and "SKU货号" in df.columns:
        for idx, row in df.iterrows():
            size = row["变种属性值二"].strip()
            if size in size_map:
                sku = row["SKU货号"]
                if "-" in sku:
                    prefix, suffix = sku.split("-", 1)
                    new_sku = f"{prefix}-{size_map[size]}{suffix}"
                    df.at[idx, "SKU货号"] = new_sku

    # 保存结果
    df.to_excel(output_path, index=False)
    print(f"✅ 文件已处理并保存至：{output_path}")


if __name__ == '__main__':
    input_file = "/Users/zkp/Desktop/22222.xlsx"
    output_file = "/Users/zkp/Desktop/22222.xlsx"
    process_excel(input_file, output_file)
