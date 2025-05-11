import pandas as pd
from datetime import datetime, timedelta

from xinshili.utils import current_time


def transfer_and_merge_address(file1_path, file2_path, output_path):
    # 读取文件，并将所有内容当作字符串读入，避免数字变格式
    df1 = pd.read_excel(file1_path, dtype=str).fillna("")
    df2 = pd.read_excel(file2_path, dtype=str).fillna("")

    # 定义列映射关系
    column_mapping = {
        "平台单号": "订单号",
        "收件人": "收件人",
        "城市": "收件人城市",
        "省/州": "收件人州/省",
        "邮编": "收件人邮编"
    }

    # 遍历映射，将文件1的数据（转为字符串）填入文件2
    for source_col, target_col in column_mapping.items():
        if source_col in df1.columns and target_col in df2.columns:
            df2[target_col] = df1[source_col].astype(str)
        else:
            print(f"⚠️ 缺少列：{source_col} 或 {target_col}，跳过该列")

    # 地址列处理：不存在的列用空字符串补齐
    address_cols = ["地址行1", "地址行2", "地址行3"]
    for col in address_cols:
        if col not in df1.columns:
            df1[col] = ""

    # 拼接地址，只拼接非空项之间的空格
    df2["收件人地址1"] = df1[address_cols].apply(
        lambda row: " ".join(part.strip() for part in row if part.strip()), axis=1
    )

    # 保存为 Excel 文件
    df2.to_excel(output_path, index=False)
    print(f"✅ 文件已更新并保存至：{output_path}")


def convert_to_beijing_time(value):
    # 如果是 datetime 类型，直接使用
    if isinstance(value, datetime):
        dt = value

    # 如果是字符串类型，尝试两种格式进行转换
    elif isinstance(value, str):
        value = value.strip()
        if "/" in value and "AM" in value.upper() or "PM" in value.upper():
            dt = datetime.strptime(value, "%m/%d/%Y %I:%M:%S %p")  # 12 小时制
        elif "/" in value:
            dt = datetime.strptime(value, "%Y/%m/%d %H:%M:%S")  # 24 小时制
        else:
            raise ValueError(f"无法识别的时间格式: {value}")
    else:
        raise TypeError(f"不支持的时间类型: {type(value)}")

    # 转换为北京时间（GMT-7 ➜ GMT+8，+15 小时）
    dt_beijing = dt + timedelta(hours=15)
    return dt_beijing.strftime("%Y/%m/%d %H:%M:%S")


def process_excel_time_column(file_path, output_path):
    df = pd.read_excel(file_path)

    if "订单创建时间" not in df.columns:
        print("❌ 未找到“订单创建时间”列")
        return

    # 应用时间转换
    df["订单创建时间"] = df["订单创建时间"].apply(convert_to_beijing_time)

    # 保存文件
    df.to_excel(output_path, index=False)
    print(f"✅ 已转换并保存至：{output_path}")


if __name__ == '__main__':
    # scr_path = "/Users/zkp/Downloads/订单管理20250510-44-779759150004064256.xlsx"
    # dst_path = "/Users/zkp/Documents/代采出阳单模版.xlsx"
    # output_path = f"/Users/zkp/Documents/{current_time()}_阳单.xlsx"
    # transfer_and_merge_address(scr_path, dst_path, output_path)

    output_path = f"/Users/zkp/Documents/2025-05-11 15:46:51_阳单.xlsx"
    process_excel_time_column(output_path, output_path)
