from datetime import datetime

import pandas as pd
import re

from xinshili import utils


def update_shipping_info(file1_path, file2_path, output_dir):
    # 读取文件1（原始数据）
    df1 = pd.read_excel(file1_path, dtype=str).fillna("")

    if "包裹备注" not in df1.columns or "平台回传单号" not in df1.columns:
        print("❌ 文件1缺少必要列：包裹备注 或 平台回传单号")
        return

    # 提取数据：从“包裹备注”中获取第二个 "-" 后的编号
    extract_info = {}
    for _, row in df1.iterrows():
        remark = row["包裹备注"]
        platform_no = row["平台回传单号"]
        match = re.match(r"[^-]+-[^-]+-(.+)", remark)
        if match:
            extracted_number = match.group(1).strip()
            extract_info[platform_no] = extracted_number

    print(extract_info)

    # 读取文件2
    df2 = pd.read_excel(file2_path, dtype=str).fillna("")

    # 写入数据
    for idx, row in df2.iterrows():
        print(row, idx)
        platform_no = row.get("*系统单号", "").strip()
        if platform_no in extract_info:
            df2.at[idx, "*系统单号"] = platform_no
            df2.at[idx, "*运单号"] = extract_info[platform_no]

    # 设置固定值（对所有有效行）
    fixed_fields = {
        "*物流方式": "502-24417",
        "*发货仓库": "佛罗里达",
        "重量单位": "g",
        "尺寸单位": "cm",
        "费用币种": "CNY"
    }

    for col, val in fixed_fields.items():
        if col in df2.columns:
            df2[col] = df2[col].apply(lambda x: val if x.strip() == "" else x)

    strftime = datetime.now().strftime("%Y-%m-%d")
    output_path = f"{output_dir}{strftime}_{len(df2)}单.xlsx"

    # 保存结果
    df2.to_excel(output_path, index=False)
    print(f"✅ 已更新并保存文件至：{output_path}")
    utils.open_dir(output_dir)


if __name__ == '__main__':
    source_file = input("请输入源表文件的绝对路径：")
    template_path = utils.current_dir() + "/xlsx/daicai/领星出库单模板.xlsx"
    output_dir = "/Users/zkp/Desktop/B&Y/yd/lxyd/"

    update_shipping_info(
        file1_path=source_file,
        file2_path=template_path,
        output_dir=output_dir
    )
