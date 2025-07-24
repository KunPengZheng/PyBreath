import pandas as pd
import random
import string
from xinshili import utils
from xinshili.utils import current_time
from collections import defaultdict
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import re
import os


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

    # 构建平台单号到 SKU:数量 的嵌套字典
    order_sku_map = defaultdict(lambda: defaultdict(int))

    for i in range(len(df1)):
        platform_order = str(df1.at[i, "平台单号"]).strip()
        sku_raw = str(df1.at[i, "SKU"]).strip()
        qty_raw = str(df1.at[i, "数量"]).strip()

        sku_lines = [s.strip() for s in sku_raw.splitlines() if s.strip()]
        qty_lines = [q.strip() for q in qty_raw.splitlines() if q.strip()]

        for idx, sku in enumerate(sku_lines):
            try:
                qty = int(qty_lines[idx]) if idx < len(qty_lines) else 1
            except Exception:
                qty = 1
            order_sku_map[platform_order][sku] += qty

    # 生成备注列内容（与 df2["订单号"] 匹配）
    remarks = []

    for i in range(len(df2)):
        order_id = str(df2.at[i, "订单号"]).strip()

        matched_sku_dict = {}
        for platform_order, sku_dict in order_sku_map.items():
            if platform_order in order_id:  # 模糊匹配
                matched_sku_dict = sku_dict
                break  # 找到即停止

        if matched_sku_dict:
            remark_text = "\n".join([f"{sku}*{qty}" for sku, qty in matched_sku_dict.items()])
            remarks.append(remark_text)
        else:
            remarks.append("  ")

    # df2["备注"] = remarks
    df2["备注"] = "  "

    # 去重
    if "订单号" in df2.columns:
        df2 = df2.drop_duplicates(subset=["订单号"], keep='first')
    else:
        print("⚠️ df2 中缺少“订单号”列，跳过去重。")

    output_path = ""
    if channel_flag == "usps":
        output_path = f"{output_dir}{current_time()}_fastU_usps阳单_{len(df2)}单.xlsx"
    elif channel_flag == "ups":
        output_path = f"{output_dir}{current_time()}_fastU_ups阳单_{len(df2)}单.xlsx"

    # 保存文件
    df2.to_excel(output_path, index=False)
    print(f"✅ 文件已更新并保存至：{output_path}")


def transfer_temu_kjd(file1_path, file2_path, output_dir, order_prefix, channel_flag, delayed=0):
    # 读取文件，并将所有内容当作字符串读入，避免数字变格式

    ext = os.path.splitext(file1_path)[1].lower()
    if ext == ".csv":
        df1 = pd.read_csv(file1_path, dtype=str).fillna("")
    elif ext == ".xlsx":
        df1 = pd.read_excel(file1_path, engine="openpyxl", dtype=str).fillna("")
    elif ext == ".xls":
        df1 = pd.read_excel(file1_path, engine="xlrd", dtype=str).fillna("")
    else:
        raise ValueError(f"❌ 不支持的文件格式：{ext}")

    # df1 = pd.read_excel(file1_path, dtype=str).fillna("")
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

    def clean_and_convert_to_china_time(original_time_str) -> str:
        """
        清理字符串中的时区标识并将 UTC-7/8 的时间转换为北京时间
        """
        try:
            # 去掉例如 " PDT(UTC-7)" 或 " PST(UTC-8)" 的部分
            cleaned_str = re.sub(r"\s*(P[SD]T)?\(UTC-[0-9]+\)", "", original_time_str).strip()
            # 解析为 datetime 对象
            dt = datetime.strptime(cleaned_str, "%b %d, %Y, %I:%M %p")
            # 设置美国西部时间（自动考虑夏令时）
            dt_usa = dt.replace(tzinfo=ZoneInfo("America/Los_Angeles"))
            # 转换为北京时间（中国）
            dt_china = dt_usa.astimezone(ZoneInfo("Asia/Shanghai"))
            dt_china_plus = dt_china + timedelta(hours=delayed)
            return dt_china_plus.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(f"❌ 解析失败：{original_time_str}，原因：{e}")
            return ""

    df2["订单创建时间"] = df1["purchase date"].astype(str).str.strip().apply(clean_and_convert_to_china_time)

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

    # 构建平台单号到 SKU:数量 的嵌套字典
    order_sku_map = defaultdict(lambda: defaultdict(int))

    for i in range(len(df1)):
        platform_order = str(df1.at[i, "order id"]).strip()
        sku_raw = str(df1.at[i, "contribution sku"]).strip()
        qty_raw = str(df1.at[i, "quantity purchased"]).strip()

        sku_lines = [s.strip() for s in sku_raw.splitlines() if s.strip()]
        qty_lines = [q.strip() for q in qty_raw.splitlines() if q.strip()]

        for idx, sku in enumerate(sku_lines):
            try:
                qty = int(qty_lines[idx]) if idx < len(qty_lines) else 1
            except Exception:
                qty = 1
            order_sku_map[platform_order][sku] += qty

    # 生成备注列内容（与 df2["订单号"] 匹配）
    remarks = []

    for i in range(len(df2)):
        order_id = str(df2.at[i, "订单号"]).strip()

        matched_sku_dict = {}
        for platform_order, sku_dict in order_sku_map.items():
            if platform_order in order_id:  # 模糊匹配
                matched_sku_dict = sku_dict
                break  # 找到即停止

        if matched_sku_dict:
            remark_text = "\n".join([f"{sku}*{qty}" for sku, qty in matched_sku_dict.items()])
            remarks.append(remark_text)
        else:
            remarks.append("  ")

    # df2["备注"] = remarks
    df2["备注"] = "  "

    # 去重
    if "订单号" in df2.columns:
        df2 = df2.drop_duplicates(subset=["订单号"], keep='first')
    else:
        print("⚠️ df2 中缺少“订单号”列，跳过去重。")

    output_path = ""
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
    select += "\n2：ups"
    select += "\n"
    select_input2 = input(select)
    if select_input == "1":
        channel_flag = 'usps'
    elif select_input == "2":
        channel_flag = 'ups'
    else:
        print("🈚️此项功能！")

    order_prefixs = f"_{remark_prefixs}_{channel_flag}_" + ''.join(random.choices(string.ascii_lowercase, k=3))

    dst_path = utils.current_dir() + "/xlsx/yd/fastusps_USPS_阳单模版.xlsx"
    output_dir = f"/Users/zkp/Desktop/B&Y/yd/yd_fast/"

    select = "请选择转换模版："
    select += "\n1：领星erp"
    select += "\n2：temu跨境店"
    select += "\n"
    select_input = input(select)
    if select_input == "1":
        transfer_lx_erp(source_file, dst_path, output_dir, order_prefixs, channel_flag)
    elif select_input == "2":
        transfer_temu_kjd(source_file, dst_path, output_dir, order_prefixs, channel_flag, 48)
    else:
        print("🈚️此项功能！")

    utils.open_dir(output_dir)
