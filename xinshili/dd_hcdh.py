from dataclasses import dataclass

import pandas as pd
import os


@dataclass(frozen=True)
class KeyName:
    address = '地址'
    city = '城市'
    state = "省州"
    zip = "邮编"
    name = "姓名"
    phone = "电话"
    mx = "美西"
    mz = "美中"
    fc = "费城"
    flld = "佛罗里达"


# 美中1 美中休斯敦
WAREHOUSE_mz_xsd = {
    KeyName.address: "9197 Winkler Dr STE B",
    KeyName.city: "Houston",
    KeyName.state: "TX",
    KeyName.zip: "77017",
    KeyName.name: "Jeck Som",
    KeyName.phone: "（+1）8328236666",
}

# 东谷 美西东谷
WAREHOUSE_mx_dg = {
    KeyName.address: "1180 E Francis St",
    KeyName.city: "ontario",
    KeyName.state: "CA",
    KeyName.zip: "91761",
    KeyName.name: "Jim Som",
    KeyName.phone: "（+1）3333333333",
}

# 费城 费城
WAREHOUSE_fc = {
    KeyName.address: "38930 Chalfont Dr",
    KeyName.city: "PHILADELPHIA",
    KeyName.state: "PA",
    KeyName.zip: "19154",
    KeyName.name: "Tony Zheng",
    KeyName.phone: "（+1）4335115177",
}

# 佛罗里达
WAREHOUSE_flld = {
    KeyName.address: "13621 NW 12th St",
    KeyName.city: "Sunrise",
    KeyName.state: "FL",
    KeyName.zip: "33323",
    KeyName.name: "kk dick",
    KeyName.phone: "(+1)5689741235",
}


def copy_columns_between_excels(
        file_a,
        file_b,
        output_file,
        column_map,
        warehouse_configs,
        b_column_alias
):
    # 读取文件
    df_a = pd.read_excel(file_a)
    df_b = pd.read_excel(file_b)

    # 1️⃣ 判断仓库
    filename_a = os.path.basename(file_a)
    matched_warehouse = None
    for keyword, config in warehouse_configs.items():
        if keyword in filename_a:
            matched_warehouse = config
            print(f"✅ 文件名匹配到仓库: {keyword}")
            break

    # 2️⃣ 如果匹配到仓库，填充发件人信息
    if matched_warehouse:
        for attr, value in matched_warehouse.items():
            if attr in b_column_alias:
                matched_col = None
                for alias in b_column_alias[attr]:
                    for col in df_b.columns:
                        if alias in col:  # 模糊匹配
                            matched_col = col
                            break
                    if matched_col:
                        break
                if matched_col:
                    df_b[matched_col] = value
                    print(f"✅ 已将 {attr}({value}) → {matched_col}")
                else:
                    print(f"⚠️ B 文件中未找到 {attr} 对应列")

    # 3️⃣ 按映射关系复制 A→B 列
    for source_col, target_keywords in column_map.items():
        if source_col not in df_a.columns:
            print(f"⚠️ A 文件中没有列: {source_col}，跳过")
            continue

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

    # 4️⃣ 保存结果
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

warehouse_configs = {
    KeyName.mx: WAREHOUSE_mx_dg,
    KeyName.mz: WAREHOUSE_mz_xsd,
    KeyName.fc: WAREHOUSE_fc,
    KeyName.flld: WAREHOUSE_flld,
}

b_column_alias = {
    KeyName.name: ["发件人姓名", "发件人名称"],
    KeyName.state: ["发件人省/州", "发件人州/省", "发件人省", "发件人州"],
    KeyName.city: ["发件人城市"],
    KeyName.address: ["发件人地址"],
    KeyName.zip: ["发件人邮编"],
    KeyName.phone: ["发件人电话"],
}

file_a = "/Users/zkp/Desktop/B&Y/dd/9.23/科技单/打单_双木_佛罗里达_18单_0923.xlsx"
file_b = "/Users/zkp/Downloads/订单导入-模版.xlsx"
file_result = "/Users/zkp/Downloads/订单导入-1.xlsx"

copy_columns_between_excels(
    file_a,
    file_b,
    file_result,
    column_map,
    warehouse_configs,
    b_column_alias
)
