import pandas as pd
import random
import string
from xinshili import utils
from xinshili.utils import current_time
from collections import defaultdict


def transfer_lx_erp(file1_path, file2_path, output_dir, order_prefix):
    # 读取文件，并将所有内容当作字符串读入，避免数字变格式
    df1 = pd.read_excel(file1_path, dtype=str).fillna("")
    df2 = pd.read_excel(file2_path, dtype=str).fillna("")

    # 定义列映射关系
    column_mapping = {
        "平台单号": "订单号",
        "收件人": "收件人",
        "城市": "收件人城市",
        "省/州": "收件人州/省",
        "邮编": "收件人邮编",
        "付款时间": "订单创建时间",
    }

    # 遍历映射，将文件1的数据填入文件2
    for source_col, target_col in column_mapping.items():
        if source_col in df1.columns and target_col in df2.columns:
            if source_col == "平台单号" and target_col == "订单号":
                df2[target_col] = df1[source_col].astype(str).apply(lambda x: x.strip() + order_prefix)
            else:
                df2[target_col] = df1[source_col].astype(str)
        else:
            print(f"⚠️ 缺少列：{source_col} 或 {target_col}，跳过该列")

    # 拼接地址
    address_cols = ["地址行1", "地址行2", "地址行3"]
    for col in address_cols:
        if col not in df1.columns:
            df1[col] = ""

    df2["收件人地址1"] = df1[address_cols].apply(
        lambda row: " ".join(part.strip() for part in row if part.strip()), axis=1
    )

    if "备注" in df2.columns and "SKU" in df1.columns and "数量" in df1.columns:
        sku_qty_map = defaultdict(int)
        for i in range(len(df1)):
            sku_raw = str(df1.at[i, "SKU"]).strip()
            qty_raw = str(df1.at[i, "数量"]).strip()

            sku_lines = sku_raw.splitlines()
            qty_lines = qty_raw.splitlines()

            for idx, sku in enumerate(sku_lines):
                sku = sku.strip()
                if not sku:
                    continue

                qty_str = qty_lines[idx].strip() if idx < len(qty_lines) else "1"

                try:
                    qty = int(qty_str)
                except ValueError:
                    qty = 1  # 默认数量为 1

                sku_qty_map[sku] += qty

        result_dict = dict(sku_qty_map)
        # 拼接成字符串：每个键值对使用 *，每行一个
        formatted_str = ""
        for i, (k, v) in enumerate(result_dict.items()):
            pair_str = f"{k}*{v}"
            if i == 0:
                formatted_str += pair_str
            else:
                formatted_str += "\n" + pair_str
        df2["备注"] = formatted_str
    else:
        print("⚠️ 缺少“SKU”、“数量”或 df2 中无“备注”列，未处理备注信息")
    # df2["备注"] = "  "

    # 去重
    if "订单号" in df2.columns:
        df2 = df2.drop_duplicates(subset=["订单号"], keep='first')
    else:
        print("⚠️ df2 中缺少“订单号”列，跳过去重。")

    output_path = f"{output_dir}{current_time()}_阳单_{len(df2)}单.xlsx"

    # 保存文件
    df2.to_excel(output_path, index=False)
    print(f"✅ 文件已更新并保存至：{output_path}")


if __name__ == '__main__':
    source_file = input("请输入源表文件的绝对路径：")

    select = "请选择类型："
    select += "\n1：dc"
    select += "\n2：yd"
    select += "\n"
    select_input = input(select)
    if select_input == "1":
        remark_prefixs = 'dc'
    elif select_input == "2":
        remark_prefixs = 'yd'
    else:
        print("🈚️此项功能！")

    select = "请选择运输商："
    select += "\n1：usps"
    select += "\n2：usp"
    select += "\n"
    select_input2 = input(select)
    if select_input == "1":
        remark_prefixs2 = 'usps'
    elif select_input == "2":
        remark_prefixs2 = 'usp'
    else:
        print("🈚️此项功能！")

    order_prefixs = f"_{remark_prefixs}_{remark_prefixs2}_" + ''.join(random.choices(string.ascii_lowercase, k=3))

    dst_path = utils.current_dir() + "/xlsx/yd/fastusps_USPS_阳单模版.xlsx"
    output_dir = f"/Users/zkp/Desktop/B&Y/yd/yd_fast/"

    transfer_lx_erp(source_file, dst_path, output_dir,
                    order_prefix=order_prefixs)

    utils.open_dir(output_dir)
