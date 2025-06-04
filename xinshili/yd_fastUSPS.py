from dataclasses import dataclass
from datetime import datetime

import pandas as pd
import pytz

from xinshili import utils
from xinshili.pd_utils import remove_duplicates_by_column
from xinshili.utils import current_time


@dataclass(frozen=True)
class RowName:
    PlatformOrder = '平台单号'
    Order = '订单号'
    Receiver = '收件人'
    City = '城市'
    ReceiverCity = '收件人城市'
    State = '省/州'
    ReceiverState = '收件人州/省'
    ZipCode = '邮编'
    ReceiverZipCode = '收件人邮编'
    PaymentTime = '付款时间'
    OrderPaymentTime = '订单创建时间'


def transfer_and_merge_address(file1_path, file2_path, output_dir, order_prefix, remark_prefix):
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

    # 生成备注列格式为“前缀-店铺-系统单号”
    if all(col in df1.columns for col in ["店铺", "系统单号"]) and "备注" in df2.columns:
        df2["备注"] = df1.apply(lambda row: f"{remark_prefix}-{row['店铺'].strip()}-{row['系统单号'].strip()}", axis=1)
    else:
        print("⚠️ 缺少“店铺”、“系统单号”或 df2 中无“备注”列，未处理备注信息")

    # 去重
    if "订单号" in df2.columns:
        df2 = df2.drop_duplicates(subset=["订单号"], keep='first')
    else:
        print("⚠️ df2 中缺少“订单号”列，跳过去重。")

    output_path = f"{output_dir}{current_time()}_阳单_{len(df2)}单.xlsx"

    # 保存文件
    df2.to_excel(output_path, index=False)
    print(f"✅ 文件已更新并保存至：{output_path}")


def convert_to_beijing_time(value):
    # 定义时区
    la_tz = pytz.timezone("America/Los_Angeles")
    bj_tz = pytz.timezone("Asia/Shanghai")

    # 解析时间
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, str):
        value = value.strip()
        for fmt in ["%m/%d/%Y %I:%M:%S %p", "%d/%m/%Y %H:%M:%S", "%Y/%m/%d %H:%M:%S"]:
            try:
                dt = datetime.strptime(value, fmt)
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"无法识别的时间格式: {value}")
    else:
        raise TypeError(f"不支持的时间类型: {type(value)}")

    # 加入洛杉矶时区信息（自动识别夏令时/冬令时）
    dt_la = la_tz.localize(dt)

    # 转换为北京时间
    dt_bj = dt_la.astimezone(bj_tz)

    return dt_bj.strftime("%Y/%m/%d %H:%M:%S")


def process_excel_time_column(file_path, output_path):
    df = pd.read_excel(file_path)

    if "订单创建时间" not in df.columns:
        print("❌ 未找到“订单创建时间”列")
        return

    df["订单创建时间"] = df["订单创建时间"].apply(convert_to_beijing_time)

    # 强制某些列为字符串，防止写入 Excel 后变为数值
    for col in ["订单号", "收件人邮编"]:
        if col in df.columns:
            df[col] = df[col].astype("string")  # 或者 .astype(str).fillna("")

    df.to_excel(output_path, index=False)
    print(f"✅ 已转换并保存至：{output_path}")


if __name__ == '__main__':
    source_file = input("请输入源表文件的绝对路径：")
    platform_order_number_suffix = input("请输入平台订单号后缀：")

    select = "请选择备注前缀："
    select += "\n1：daicai"
    select += "\n2：yd_test"
    select += "\n"
    select_input = input(select)

    if select_input == "1":
        remark_prefixs = 'daicai'
    elif select_input == "2":
        remark_prefixs = 'yd_test'
    else:
        print("🈚️此项功能！")

    dst_path = utils.current_dir() + "/xlsx/yd/fastusps_USPS_阳单模版.xlsx"
    output_dir = f"/Users/zkp/Desktop/B&Y/yd/yd_fast/"

    order_prefixs = ""
    if not platform_order_number_suffix:
        order_prefixs = ""
    else:
        if platform_order_number_suffix[0].isalpha():
            order_prefixs = "-" + platform_order_number_suffix
        else:
            raise ValueError(f"订单号后缀只能以字母为开头")

    transfer_and_merge_address(source_file, dst_path, output_dir,
                               order_prefix=order_prefixs,
                               remark_prefix=remark_prefixs)

    utils.open_dir(output_dir)

    # 若需要时间转换功能，可启用下面一行：
    # process_excel_time_column(source_file, source_file)
