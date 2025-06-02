import pandas as pd
from datetime import datetime
import os

from xinshili import utils


def transfer_order_data(file1_path, file2_template_path, output_dir):
    # 读取两个 Excel 文件
    df1 = pd.read_excel(file1_path, dtype=str).fillna("")
    df2 = pd.read_excel(file2_template_path, dtype=str).fillna("")

    # 列映射：文件1 ➜ 模板（文件2）
    mapping = {
        "订单编号": "*订单号\n(必填)",
        "平台回传单号": "*跟踪号\n（必填）"
    }

    for src_col, target_col in mapping.items():
        if src_col in df1.columns and target_col in df2.columns:
            df2[target_col] = df1[src_col]
        else:
            print(f"⚠️ 缺少列: {src_col} 或 {target_col}，已跳过")

    # 批量填充固定值
    if "*物流方式\n（必填）" in df2.columns:
        df2["*物流方式\n（必填）"] = "USPS"
    if "*发货类型\n0：虚拟发货、1:发货\n（必填）" in df2.columns:
        df2["*发货类型\n0：虚拟发货、1:发货\n（必填）"] = "1"

    strftime = datetime.now().strftime("%Y-%m-%d")
    output_path = os.path.join(output_dir, f"{strftime}_{len(df2)}单.xlsx")

    # 保存结果
    df2.to_excel(output_path, index=False)
    print(f"✅ 文件已保存至: {output_path}")
    utils.open_dir(output_dir)


if __name__ == '__main__':
    source_file = input("请输入源表文件的绝对路径：")
    template_path = utils.current_dir() + "/xlsx/dxm/import_logistics_information_template.xlsx"
    output_dir = "/Users/zkp/Desktop/B&Y/yd/dxmyd/"
    transfer_order_data(source_file, template_path, output_dir)
