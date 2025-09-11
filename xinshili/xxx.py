import pandas as pd

import pandas as pd

def find_missing_skus(file_a, file_b, sku_column="SKU", name_column="Product Name/产品名称"):
    # 读取两个文件
    data_a = pd.read_excel(file_a, dtype=str)
    data_b = pd.read_excel(file_b, dtype=str)

    # 确认列存在
    for df, name in [(data_a, "A"), (data_b, "B")]:
        if sku_column not in df.columns:
            raise ValueError(f"文件 {name} 缺少列: {sku_column}")
    if name_column not in data_a.columns:
        raise ValueError(f"文件 A 缺少列: {name_column}")

    # 去除空格（保留原始大小写，避免丢信息）
    data_a[sku_column] = data_a[sku_column].dropna().str.strip()
    data_b[sku_column] = data_b[sku_column].dropna().str.strip()

    # 找出 A 中有但 B 中没有的
    missing_mask = ~data_a[sku_column].isin(data_b[sku_column])
    missing_rows = data_a[missing_mask][[sku_column, name_column]]

    # 打印
    if not missing_rows.empty:
        print("❌ 以下 SKU 在 B 文件中未出现：")
        for _, row in missing_rows.iterrows():
            print(f"SKU: {row[sku_column]} | 产品名称: {row[name_column]}")
    else:
        print("✅ A 文件的 SKU 都存在于 B 文件中")

    return missing_rows

# find_missing_skus("/Users/zkp/Desktop/B&Y/dxm/sku_store_statistics/xyl/dxm_order.xlsx",
#                   "/Users/zkp/Desktop/B&Y/dxm/sku_store_statistics/xyl运营统计_副本.xlsx")


# find_missing_skus("/Users/zkp/Desktop/B&Y/dxm/sku_store_statistics/xyl运营统计_副本.xlsx",
#                   "/Users/zkp/Desktop/B&Y/dxm/sku_store_statistics/xyl/dxm_order.xlsx")

find_missing_skus("/Users/zkp/Desktop/B&Y/dxm/sku_store_statistics/xyl/oms_store/oms_store_merger.xlsx",
                  "/Users/zkp/Desktop/B&Y/dxm/sku_store_statistics/xyl运营统计_副本.xlsx")