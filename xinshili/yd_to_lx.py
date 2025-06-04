import pandas as pd
import os
import re
from datetime import datetime

from xinshili import utils


def update_shipping_info(file1_path, file2_path, output_dir):
    # 读取文件1（原始数据）
    df1 = pd.read_excel(file1_path, dtype=str).fillna("")

    if "包裹备注" not in df1.columns or "平台回传单号" not in df1.columns:
        print("❌ 文件1缺少必要列：包裹备注 或 平台回传单号")
        return

    # 提取数据：从“包裹备注”中获取第二个 "-" 后的编号
    new_rows = []
    for _, row in df1.iterrows():
        remark = row["包裹备注"]
        platform_no = row["平台回传单号"]
        match = re.match(r"[^-]+-[^-]+-(.+)", remark)
        if match:
            extracted_number = match.group(1).strip()
            new_rows.append({
                "*系统单号": extracted_number,
                "*运单号": platform_no,
                "*物流方式": "502-24417",
                "*发货仓库": "佛罗里达",
                "重量单位": "g",
                "尺寸单位": "cm",
                "费用币种": "CNY"
            })

    if not new_rows:
        print("⚠️ 未找到任何有效数据，未生成文件。")
        return

    # 读取模板文件（文件2），用于获取列结构
    df_template = pd.read_excel(file2_path, dtype=str).fillna("")
    output_columns = df_template.columns.tolist()

    # 构建最终 DataFrame，按模板列顺序填充，其他列留空
    df_output = pd.DataFrame(new_rows)
    for col in output_columns:
        if col not in df_output.columns:
            df_output[col] = ""

    df_output = df_output[output_columns]  # 确保列顺序与模板一致

    # 保存结果文件
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    strftime = datetime.now().strftime("%Y-%m-%d")
    output_path = os.path.join(output_dir, f"{strftime}_{len(df_output)}单.xlsx")

    df_output.to_excel(output_path, index=False)
    print(f"✅ 已更新并保存文件至：{output_path}")

    # 自动打开目录（可选）
    utils.open_dir(output_dir)


if __name__ == '__main__':
    source_file = input("请输入源表文件的绝对路径：")
    template_path = utils.current_dir() + "/xlsx/lx/领星出库单模板.xlsx"
    output_dir = "/Users/zkp/Desktop/B&Y/yd/yd_lx/"

    update_shipping_info(
        file1_path=source_file,
        file2_path=template_path,
        output_dir=output_dir
    )
