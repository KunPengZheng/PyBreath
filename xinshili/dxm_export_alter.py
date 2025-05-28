import pandas as pd


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
                    # 使用正则替换第一个数字
                    import re
                    # 查找 - 后面第一个数字并替换
                    new_suffix = re.sub(r'^\d', size_map[size], suffix, count=1)
                    new_sku = f"{prefix}-{new_suffix}"
                    df.at[idx, "SKU货号"] = new_sku

    # 保存结果
    df.to_excel(output_path, index=False)
    print(f"✅ 文件已处理并保存至：{output_path}")


if __name__ == '__main__':
    source_file = input("请输入源表文件的绝对路径：")
    process_excel(source_file, source_file)
