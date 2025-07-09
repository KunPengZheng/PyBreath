import pandas as pd

from xinshili import utils
from xinshili.utils import current_time


def transfer_and_merge_address(file1_path, file2_path, output_dir, remark_prefix, state):
    # 读取文件，并将所有内容当作字符串读入，避免数字变格式
    df1 = pd.read_excel(file1_path, dtype=str).fillna("")
    df2 = pd.read_excel(file2_path, dtype=str).fillna("")

    # ✅ 清除模板数据
    df2 = pd.DataFrame(columns=df2.columns)

    # 定义列映射关系
    column_mapping = {
        "邮编": "签收邮编",
        "付款时间": "发货日期",
    }

    # 遍历映射，将文件1的数据填入文件2
    for source_col, target_col in column_mapping.items():
        if source_col in df1.columns and target_col in df2.columns:
            if source_col == "付款时间" and target_col == "发货日期":
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
    if all(col in df1.columns for col in ["店铺", "系统单号"]) and "备注" in df2.columns:
        df2["备注"] = df1.apply(lambda row: f"{remark_prefix}-{row['店铺'].strip()}-{row['系统单号'].strip()}", axis=1)
    else:
        print("⚠️ 缺少“店铺”、“系统单号”或 df2 中无“备注”列，未处理备注信息")

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

    # 删除“签收邮编”列为空的行
    if "签收邮编" in df2.columns:
        df2 = df2[df2["签收邮编"].str.strip() != ""]
    else:
        print("⚠️ 文件中不包含“签收邮编”列，未执行删除空邮编行操作")

    output_path = f"{output_dir}{current_time()}_阳单_{len(df2)}单.xlsx"

    # 保存文件
    df2.to_excel(output_path, index=False)
    print(f"✅ 文件已更新并保存至：{output_path}")


if __name__ == '__main__':
    source_file = input("请输入源表文件的绝对路径：")

    select_channel = "请选择渠道："
    select_channel += "\n1：UPS"
    select_channel += "\n2：USPS"
    select_channel += "\n"
    select_channel_input = input(select_channel)

    select = "请选择备注前缀："
    select += "\n1：daicai"
    select += "\n2：yd"
    select += "\n"
    select_input = input(select)

    if select_input == "1":
        remark_prefixs = 'daicai'
    elif select_input == "2":
        remark_prefixs = 'yd'
    else:
        print("🈚️此项功能！")

    dst_path = ""
    output_dir = ""
    if select_channel_input == "1":
        output_dir = f"/Users/zkp/Desktop/B&Y/yd/yd_gjdh/ups"
        dst_path = utils.current_dir() + "/xlsx/yd/国际单号_UPS_阳单模板.xlsx"
    elif select_channel_input == "2":
        output_dir = f"/Users/zkp/Desktop/B&Y/yd/yd_gjdh/usps"
        dst_path = utils.current_dir() + "/xlsx/yd/国际单号_USPS_阳单模版.xlsx"
    else:
        print("🈚️此项功能！")

    state = "运输途中"

    transfer_and_merge_address(source_file, dst_path, output_dir, remark_prefixs, state)

    utils.open_dir(output_dir)
