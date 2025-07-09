import pandas as pd

from xinshili import utils
from xinshili.utils import current_time


def usps(file1_path, file2_path, output_dir, order_prefix, remark_prefix):
    # 读取文件，并将所有内容当作字符串读入，避免数字变格式
    df1 = pd.read_excel(file1_path, dtype=str).fillna("")
    df2 = pd.read_excel(file2_path, dtype=str).fillna("")

    # 定义列映射关系
    column_mapping = {
        "订单号": "订单号",
        "收货人姓名": "收件人",
        "城市": "收件人城市",
        "省份": "收件人州/省",
        "收货地址邮编": "收件人邮编",
        "订单创建时间": "订单创建时间",
        "详细地址1": "收件人地址1",
    }

    # 遍历映射，将文件1的数据填入文件2
    for source_col, target_col in column_mapping.items():
        if source_col in df1.columns and target_col in df2.columns:
            if source_col == "订单号" and target_col == "订单号":
                df2[target_col] = df1[source_col].astype(str).apply(lambda x: x.strip() + order_prefix)
            else:
                df2[target_col] = df1[source_col].astype(str)
        else:
            print(f"⚠️ 缺少列：{source_col} 或 {target_col}，跳过该列")

    # 拼接地址
    address_cols = ["详细地址2", "详细地址3"]
    for col in address_cols:
        if col not in df1.columns:
            df1[col] = ""

    df2["收件人地址2"] = df1[address_cols].apply(
        lambda row: " ".join(part.strip() for part in row if part.strip()), axis=1
    )

    # 生成备注列格式为“前缀-店铺-系统单号”
    if all(col in df1.columns for col in ["订单号"]) and "备注" in df2.columns:
        df2["备注"] = df1.apply(lambda row: f"{remark_prefix}-{row['订单号'].strip()}",
                                axis=1)
    else:
        print("⚠️ 缺少“订单号”或 df2 中无“备注”列，未处理备注信息")

    # 去重
    if "订单号" in df2.columns:
        df2 = df2.drop_duplicates(subset=["订单号"], keep='first')
    else:
        print("⚠️ df2 中缺少“订单号”列，跳过去重。")

    output_path = f"{output_dir}{current_time()}_usps阳单_{len(df2)}单.xlsx"

    # 保存文件
    df2.to_excel(output_path, index=False)
    print(f"✅ 文件已更新并保存至：{output_path}")


def ups(file1_path, file2_path, output_dir, remark_prefix, state):
    # 读取文件，并将所有内容当作字符串读入，避免数字变格式
    df1 = pd.read_excel(file1_path, dtype=str).fillna("")
    df2 = pd.read_excel(file2_path, dtype=str).fillna("")

    # ✅ 清除模板数据
    df2 = pd.DataFrame(columns=df2.columns)

    # 定义列映射关系
    column_mapping = {
        "订单创建时间": "发货日期",
        "城市": "签收城市",
        "省份": "签收州",
    }

    # 遍历映射，将文件1的数据填入文件2
    for source_col, target_col in column_mapping.items():
        if source_col in df1.columns and target_col in df2.columns:
            if source_col == "订单创建时间" and target_col == "发货日期":
                # 转换时间格式
                def format_date(x):
                    try:
                        dt = pd.to_datetime(x, errors="coerce")
                        if pd.isna(dt):
                            return ""
                        return f"{dt.year}/{dt.month}/{dt.day}"
                    except Exception:
                        return ""

                df2[target_col] = df1[source_col].apply(format_date)
            else:
                df2[target_col] = df1[source_col].astype(str)
        else:
            print(f"⚠️ 缺少列：{source_col} 或 {target_col}，跳过该列")

    # 生成备注列格式为“前缀-店铺-系统单号”
    if all(col in df1.columns for col in ["订单号"]) and "备注" in df2.columns:
        df2["备注"] = df1.apply(lambda row: f"{remark_prefix}-{row['订单号'].strip()}", axis=1)
    else:
        print("⚠️ 缺少“订单号”或 df2 中无“备注”列，未处理备注信息")

    if "状态" in df2.columns:
        # 从第2行（索引从1开始）开始填充有效行
        df2.loc[0:, "状态"] = state
    else:
        print("⚠️ 文件中不包含“状态”列")

    # 去重
    if "备注" in df2.columns:
        df2 = df2.drop_duplicates(subset=["备注"], keep='first')
    else:
        print("⚠️ df2 中缺少“订单号”列，跳过去重。")

    output_path = f"{output_dir}{current_time()}_ups阳单_{len(df2)}单.xlsx"

    # 保存文件
    df2.to_excel(output_path, index=False)
    print(f"✅ 文件已更新并保存至：{output_path}")


if __name__ == '__main__':
    source_file = input("请输入源表文件的绝对路径：")
    # platform_order_number_suffix = input("请输入平台订单号后缀：")
    #
    order_prefixs = ""
    # if not platform_order_number_suffix:
    #     order_prefixs = ""
    # else:
    #     if platform_order_number_suffix[0].isalpha():
    #         order_prefixs = "-" + platform_order_number_suffix
    #     else:
    #         raise ValueError(f"订单号后缀只能以字母为开头")

    remark_prefixs = 'yd'
    output_dir = f"/Users/zkp/Desktop/B&Y/yd/yd_temu_yf/"
    ups(source_file, f"{utils.current_dir()}/xlsx/yd/国际单号_UPS_阳单模板.xlsx",
        output_dir, remark_prefixs, "运输途中")
    usps(source_file, f"{utils.current_dir()}/xlsx/yd/国际单号_USPS_阳单模版.xlsx",
         output_dir, order_prefixs, remark_prefixs)

    utils.open_dir(output_dir)
