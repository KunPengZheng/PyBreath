import pandas as pd
import random
import string
from xinshili import utils
from xinshili.utils import current_time
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo


def transfer_lx_erp(file1_path, file2_path, output_dir, order_prefix, channel_flag):
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

    # 保证地址列存在
    address_cols = ["地址行1", "地址行2", "地址行3"]
    for col in address_cols:
        if col not in df1.columns:
            df1[col] = ""

    # 收件人地址1：直接使用地址行1
    df2["收件人地址1"] = df1["地址行1"].astype(str).str.strip()

    # 收件人地址2：拼接地址行2和地址行3（跳过空白）
    df2["收件人地址2"] = df1[["地址行2", "地址行3"]].apply(
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

    if channel_flag == "usps":
        output_path = f"{output_dir}{current_time()}_fastU_usps阳单_{len(df2)}单.xlsx"
    elif channel_flag == "ups":
        output_path = f"{output_dir}{current_time()}_fastU_ups阳单_{len(df2)}单.xlsx"

    # 保存文件
    df2.to_excel(output_path, index=False)
    print(f"✅ 文件已更新并保存至：{output_path}")


def transfer_temu_kjd(file1_path, file2_path, output_dir, order_prefix, channel_flag):
    # 读取文件，并将所有内容当作字符串读入，避免数字变格式
    df1 = pd.read_excel(file1_path, dtype=str).fillna("")
    df2 = pd.read_excel(file2_path, dtype=str).fillna("")

    # 定义列映射关系
    column_mapping = {
        "order id": "订单号",
        "recipient name": "收件人",
        "ship city": "收件人城市",
        "ship state": "收件人州/省",
        "ship postal code (Must be shipped to the following zip code.)": "收件人邮编",
    }

    # 遍历映射，将文件1的数据填入文件2
    for source_col, target_col in column_mapping.items():
        if source_col in df1.columns and target_col in df2.columns:
            if source_col == "order id" and target_col == "订单号":
                df2[target_col] = df1[source_col].astype(str).apply(lambda x: x.strip() + order_prefix)
            else:
                df2[target_col] = df1[source_col].astype(str)
        else:
            print(f"⚠️ 缺少列：{source_col} 或 {target_col}，跳过该列")

    def utc7_2_utc8(original_time_str):
        # 解析为 datetime 对象（注意格式匹配）
        dt = datetime.strptime(original_time_str, "%b %d, %Y, %I:%M %p")
        # 设置原时区为美国太平洋时间（UTC-7）
        dt_pdt = dt.replace(tzinfo=ZoneInfo("America/Los_Angeles"))
        # 转换为中国时区（北京时间，UTC+8）
        dt_china = dt_pdt.astimezone(ZoneInfo("Asia/Shanghai"))
        # 输出为字符串格式
        return dt_china.strftime("%Y-%m-%d %H:%M:%S")

    df2["订单创建时间"] = df1["purchase date"].astype(str).str.strip().apply(utc7_2_utc8)

    # 保证地址列存在
    address_cols = ["ship address 1", "ship address 2", "ship address 3"]
    for col in address_cols:
        if col not in df1.columns:
            df1[col] = ""

    # 收件人地址1：直接使用地址行1
    df2["收件人地址1"] = df1["ship address 1"].astype(str).str.strip()

    # 收件人地址2：拼接地址行2和地址行3（跳过空白）
    df2["收件人地址2"] = df1[["ship address 2", "ship address 3"]].apply(
        lambda row: " ".join(part.strip() for part in row if part.strip()), axis=1
    )

    if "备注" in df2.columns and "contribution sku" in df1.columns and "quantity purchased" in df1.columns:
        sku_qty_map = defaultdict(int)
        for i in range(len(df1)):
            sku_raw = str(df1.at[i, "contribution sku"]).strip()
            qty_raw = str(df1.at[i, "quantity purchased"]).strip()

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
        print("⚠️ 缺少“contribution sku”、“quantity purchased”或 df2 中无“备注”列，未处理备注信息")
    # df2["备注"] = "  "

    # 去重
    if "order id" in df2.columns:
        df2 = df2.drop_duplicates(subset=["order id"], keep='first')
    else:
        print("⚠️ df2 中缺少“order id”列，跳过去重。")

    if channel_flag == "usps":
        output_path = f"{output_dir}{current_time()}_fastU_usps阳单_{len(df2)}单.xlsx"
    elif channel_flag == "ups":
        output_path = f"{output_dir}{current_time()}_fastU_ups阳单_{len(df2)}单.xlsx"

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
        channel_flag = 'usps'
    elif select_input == "2":
        channel_flag = 'usp'
    else:
        print("🈚️此项功能！")

    order_prefixs = f"_{remark_prefixs}_{channel_flag}_" + ''.join(random.choices(string.ascii_lowercase, k=3))

    dst_path = utils.current_dir() + "/xlsx/yd/fastusps_USPS_阳单模版.xlsx"
    output_dir = f"/Users/zkp/Desktop/B&Y/yd/yd_fast/"

    transfer_lx_erp(source_file, dst_path, output_dir, order_prefixs, channel_flag)

    utils.open_dir(output_dir)
