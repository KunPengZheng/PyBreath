import pandas as pd
from datetime import datetime, timedelta
from xinshili.utils import current_time


def transfer_and_merge_address(file1_path, file2_path, output_path, order_prefix, remark_prefix):
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

    # “店铺”列复制到“备注”列，并加前缀
    if "店铺" in df1.columns and "备注" in df2.columns:
        df2["备注"] = df1["店铺"].astype(str).apply(lambda x: remark_prefix + x.strip())
    else:
        print("⚠️ 缺少“店铺”或“备注”列，未处理备注信息")

    # 保存为 Excel 文件
    df2.to_excel(output_path, index=False)
    print(f"✅ 文件已更新并保存至：{output_path}")


def convert_to_beijing_time(value):
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

    dt_beijing = dt + timedelta(hours=15)
    return dt_beijing.strftime("%Y/%m/%d %H:%M:%S")


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
    # scr_path = "/Users/zkp/Documents/订单管理20250514-97-781175708892880896.xlsx"
    # dst_path = "/Users/zkp/Documents/代采出阳单模版.xlsx"
    # output_path = f"/Users/zkp/Documents/{current_time()}_阳单.xlsx"
    # transfer_and_merge_address(scr_path, dst_path, output_path, order_prefix="", remark_prefix="daicai-")

    # 若需要时间转换功能，可启用下面一行：
    output_path = f"/Users/zkp/Documents/2025-05-14 15:15:31_阳单 2.xlsx"
    process_excel_time_column(output_path, output_path)
