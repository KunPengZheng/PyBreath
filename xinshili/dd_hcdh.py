import pandas as pd


def copy_columns_between_excels(file_a, file_b, column_map, output_file="B_updated.xlsx"):
    """
    将 A 文件的指定列复制到 B 文件的对应列（支持B文件列名变化）

    参数:
        file_a (str): A 文件路径
        file_b (str): B 文件路径
        column_map (dict): 映射关系 {A列名: [B文件可能的列名关键字]}
        output_file (str): 输出文件路径，默认 "B_updated.xlsx"
    """
    df_a = pd.read_excel(file_a)
    df_b = pd.read_excel(file_b)

    for source_col, target_keywords in column_map.items():
        if source_col not in df_a.columns:
            print(f"⚠️ A 文件中没有列: {source_col}，跳过")
            continue

        # 找 B 文件目标列
        target_col = None
        for col in df_b.columns:
            for kw in target_keywords:
                if kw.lower() in col.lower():  # 忽略大小写
                    target_col = col
                    break
            if target_col:
                break

        if target_col:
            df_b[target_col] = df_a[source_col]
            print(f"✅ 已复制 {source_col} → {target_col}")
        else:
            print(f"❌ B 文件中未找到匹配列，跳过: {source_col}")

    # 保存结果
    df_b.to_excel(output_file, index=False)
    print(f"✅ 数据已更新并保存到 {output_file}")


column_map = {
    "order num": ["客户单号/入库单号", "客户单号/入库单号"],
    "Item-sku": ["物流产品", "物流产品(产品编号)", "配货备注1"],
    "Name": ["收件人名称", "收件人姓名"],
    "Abbreviation": ["收件人州/省", "收件人省/州"],
    "City": ["收件人城市"],
    "phone num1": ["收件人电话"],
}

copy_columns_between_excels(
    "A.xlsx",
    "B.xlsx",
    column_map,
    output_file="B_结果.xlsx"
)
