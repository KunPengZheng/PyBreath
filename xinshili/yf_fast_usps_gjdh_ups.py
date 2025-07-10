import pandas as pd
from datetime import datetime
import os
import re

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

    # 替换 "--" 为 ""，并拼接
    df2["收件人地址2"] = df1[address_cols].apply(
        lambda row: " ".join(part.strip().replace("--", "") for part in row if part.strip() and part.strip() != "--"),
        axis=1
    )

    # 备注是给面单使用的 如："HS11168WE*1"
    if all(col in df1.columns for col in ["SKU货号"]) and "备注" in df2.columns:
        df2["备注"] = df1.apply(lambda row: f"{row['SKU货号'].strip()}*{row['应履约件数']}", axis=1)
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


def ups_yd_to_dxm(file1_path, file2_template_path, output_dir):
    def clean_order_id(order_id: str) -> str:
        order_id = order_id.strip()
        # 去除前缀 'yfyd-'
        if order_id.lower().startswith("yfyd-"):
            order_id = order_id[5:]
        return order_id

    # 读取两个 Excel 文件
    df1 = pd.read_excel(file1_path, dtype=str).fillna("")
    df2 = pd.read_excel(file2_template_path, dtype=str).fillna("")

    # 清理订单编号前缀
    if "备注" in df1.columns:
        df1["备注"] = df1["备注"].apply(clean_order_id)

    # 列映射：文件1 ➜ 模板（文件2）
    mapping = {
        "备注": "*订单号\n(必填)",
        "单号": "*跟踪号\n（必填）"
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
    output_path = os.path.join(output_dir, f"ups2dxm_{strftime}_{len(df2)}单.xlsx")

    # 保存结果
    df2.to_excel(output_path, index=False)
    print(f"✅ 文件已保存至: {output_path}")
    utils.open_dir(output_dir)


def usps_yd_to_gc(file1_path, file2_template_path, output_dir):
    def clean_order_id(order_id: str) -> str:
        """
        去除订单编号中最后一个 `-xxx` 后缀，例如：
        '123456-a' -> '123456'
        'ABC-123-sds' -> 'ABC-123'
        """
        order_id = order_id.strip()
        return re.sub(r"-[^-]+$", "", order_id)

    # 读取两个 Excel 文件
    df1 = pd.read_excel(file1_path, dtype=str).fillna("")
    df2 = pd.read_excel(file2_template_path, dtype=str).fillna("")

    # 清理订单编号后缀
    if "订单编号" in df1.columns:
        df1["订单编号"] = df1["订单编号"].apply(clean_order_id)

    # 列映射：文件1 ➜ 模板（文件2）
    mapping = {
        "订单编号": "*订单号",
        "平台回传单号": "*物流单号"
    }

    for src_col, target_col in mapping.items():
        if src_col in df1.columns and target_col in df2.columns:
            df2[target_col] = df1[src_col]
        else:
            print(f"⚠️ 缺少列: {src_col} 或 {target_col}，已跳过")

    # 批量填充固定值
    if "*快递公司" in df2.columns:
        df2["*工厂地址ID"] = "USPS"
    if "*快递公司" in df2.columns:
        df2["*工厂地址ID"] = "38ea2fc5e0c00"

    strftime = datetime.now().strftime("%Y-%m-%d")
    output_path = os.path.join(output_dir, f"usps2gc_{strftime}_{len(df2)}单.xlsx")

    # 保存结果
    df2.to_excel(output_path, index=False)
    print(f"✅ 文件已保存至: {output_path}")
    utils.open_dir(output_dir)


if __name__ == '__main__':
    select = "请选择功能："
    select += "\n1：ups_usps_yd"
    select += "\n2：国际单号ups阳单 转换 店小秘模版"
    select += "\n3：Fast USPS阳单 转换 工厂模版"
    select += "\n"
    select_input = input(select)

    output_dir = f"/Users/zkp/Desktop/B&Y/yd/yd_temu_yf/"

    if select_input == "1":
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

        remark_prefixs = 'yfyd'
        ups(source_file, f"{utils.current_dir()}/xlsx/yd/国际单号_UPS_阳单模板.xlsx",
            output_dir, remark_prefixs, "运输途中")
        usps(source_file, f"{utils.current_dir()}/xlsx/yd/fastusps_USPS_阳单模版.xlsx",
             output_dir, order_prefixs, remark_prefixs)

        utils.open_dir(output_dir)
    elif select_input == "2":
        source_file = input("请输入源表文件的绝对路径：")
        template_path = utils.current_dir() + "/xlsx/dxm/import_logistics_information_template.xlsx"
        ups_yd_to_dxm(source_file, template_path, output_dir)
    elif select_input == "3":
        source_file = input("请输入源表文件的绝对路径：")
        template_path = utils.current_dir() + "/xlsx/yd/衣服面单匹配模板.xlsx"
        usps_yd_to_gc(source_file, template_path, output_dir)
    else:
        print("🈚️此项功能！")
