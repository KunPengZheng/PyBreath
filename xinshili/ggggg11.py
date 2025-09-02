import pandas as pd


def remove_st_rows_excel(input_file, output_file=None):
    # 读取 Excel
    df = pd.read_excel(input_file, dtype=object)

    # 删除 "名称" 列中包含 "ST" 或 "st" 的行
    df = df[~df["名称"].str.contains("ST|st", na=False)]

    # 输出文件路径
    if output_file is None:
        output_file = input_file.replace(".xlsx", "_clean.xlsx")

    # 保存为 Excel
    df.to_excel(output_file, index=False)

    print(f"✅ 已处理完成，结果保存到: {output_file}")


def merge_excels_with_dynamic_columns(file1, file2, output_file):
    # 固定列（顺序必须固定）
    fixed_columns = [
        "代码", "名称",
        "2024-03(股东人数)", "2024-06(股东人数)",
        "2024-09(股东人数)", "2024-12(股东人数)",
        "2025-03(股东人数)"
    ]

    # 读取两个 Excel
    df1 = pd.read_excel(file1, dtype=object)
    df2 = pd.read_excel(file2, dtype=object)

    # 收集所有列名（固定列 + 动态列）
    all_columns = list(dict.fromkeys(fixed_columns + list(df1.columns) + list(df2.columns)))

    # 确保所有 DataFrame 都有这些列，缺失填 0
    for df in [df1, df2]:
        for col in all_columns:
            if col not in df.columns:
                df[col] = 0

    # 统一列顺序（固定列在前，动态列按字母/时间顺序排列）
    dynamic_columns = [c for c in all_columns if c not in fixed_columns]
    dynamic_columns = sorted(dynamic_columns)  # 按时间排序（如果列名规范化了）
    final_columns = fixed_columns + dynamic_columns

    # 合并
    merged_df = pd.concat([df1[final_columns], df2[final_columns]], ignore_index=True)

    # 保存结果
    merged_df.to_excel(output_file, index=False)
    print(f"✅ 合并完成，保存到: {output_file}")


remove_st_rows_excel("/Users/zkp/Documents/d d/副本sh3_gdrs 2.xlsx")
remove_st_rows_excel("/Users/zkp/Documents/d d/副本sz3_gdrs 2.xlsx")

# 调用示例
merge_excels_with_dynamic_columns(
    "/Users/zkp/Documents/d d/副本sz3_gdrs 2_clean.xlsx",
    "/Users/zkp/Documents/d d/副本sh3_gdrs 2_clean.xlsx",
    "/Users/zkp/Documents/d d/merged.xlsx"
)
