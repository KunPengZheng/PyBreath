import pandas as pd
from datetime import datetime
import xlsxwriter

from xinshili.fs_utils_plus import get_token, yy_sheet_value, ClientConstants
from xinshili.gjgz_plus333 import extract_and_process_data, CourierStateMapKey, RowName, update_courier_status
from xinshili.utils import getYmd

"""
1. 下载 店小秘 和 领星 tk平台对应日期的数据，然后使用功能1
2. 间隔十的倍数的天数，就可以对之前的数据进行功能2的分析
"""


def compare_tracking_numbers(file1_path, file2_path, output_dir):
    # 引用常量名称（你需确保这些常量在其他地方定义过）
    order_col_1 = RowName.Order_Num  # df1 中的订单号
    tracking_col_1 = RowName.Track_Num  # df1 中的运单号
    order_col_2 = RowName.Platform_Num  # df2 中的订单号（平台单号）
    tracking_col_2 = RowName.Package1_Tracking  # df2 中的运单号
    create_time_col_2 = RowName.OutboundTime  # df2 中的创建时间列
    create_time_out_col = RowName.Create_Time  # 输出文件中的创建时间列名
    store_col = "店铺账号"  # df1 中的店铺账号列

    # 读取 Excel 文件（强制所有列为字符串以防止科学计数法）
    df1 = pd.read_excel(file1_path, dtype=str).fillna("")
    df2 = pd.read_excel(file2_path, dtype=str).fillna("")

    # 清理空格
    for col in [order_col_1, tracking_col_1, store_col]:
        df1[col] = df1[col].astype(str).str.strip()
    for col in [order_col_2, tracking_col_2, create_time_col_2]:
        df2[col] = df2[col].astype(str).str.strip()

    # 删除缺失值或空字符串的行
    df1_clean = df1[(df1[order_col_1] != "") & (df1[tracking_col_1] != "")]
    df2_clean = df2[(df2[order_col_2] != "") & (df2[tracking_col_2] != "")]

    # 合并两个 DataFrame：根据订单号匹配，并保留创建时间和店铺账号
    merged = pd.merge(
        df1_clean[[order_col_1, tracking_col_1, store_col]],
        df2_clean[[order_col_2, tracking_col_2, create_time_col_2]],
        left_on=order_col_1,
        right_on=order_col_2,
        how='inner'
    )

    # 查找运单号不一致的记录
    mismatched = merged[merged[tracking_col_1] != merged[tracking_col_2]]

    # 整理输出
    result = mismatched[[order_col_1, tracking_col_1, tracking_col_2, create_time_col_2, store_col]].copy()
    result.columns = [RowName.Order_Num, RowName.Yang_Num, RowName.Yin_Num, create_time_out_col, "店铺账号"]

    # 强制订单号为字符串（防止科学计数法）
    result[RowName.Order_Num] = result[RowName.Order_Num].astype(str)

    # 追加必要的空列（便于后续填充）
    for col in [
        RowName.Yang_Track_State, RowName.Yin_Track_State,
        RowName.Yang_Delivered_Time, RowName.Yin_Delivered_Time,
        RowName.YY_Delivered_Time
    ]:
        if col not in result.columns:
            result[col] = ""

    # ✅ 打印创建时间列中的最早和最晚时间（仅日期部分）
    try:
        create_times = pd.to_datetime(result[create_time_out_col], errors='coerce')
        create_times = create_times.dropna()
        if not create_times.empty:
            min_date = create_times.min().strftime("%Y-%m-%d")
            max_date = create_times.max().strftime("%Y-%m-%d")
            print(f"📅 最早创建时间：{min_date}")
            print(f"📅 最晚创建时间：{max_date}")
        else:
            print("⚠️ 创建时间列中无有效日期，无法提取最早和最晚时间。")
    except Exception as e:
        print(f"❌ 创建时间解析失败: {e}")

    # 保存为 Excel 文件
    output_path = output_dir + min_date + "_" + max_date + "_" + f"{len(result)}单" + ".xlsx"
    result.to_excel(output_path, index=False)
    print(f"✅ 差异记录已保存到: {output_path}")


def compare_delivery_times(file_path):
    df = pd.read_excel(file_path)

    result = []

    for idx, row in df.iterrows():
        time1 = row.get(RowName.Yang_Delivered_Time)
        time2 = row.get(RowName.Yin_Delivered_Time)

        # 处理空值
        if pd.isna(time1) and pd.isna(time2):
            result.append("")
            continue
        elif pd.notna(time1) and pd.isna(time2):
            result.append("阳单先到达")
            continue
        elif pd.isna(time1) and pd.notna(time2):
            result.append("阴单先到达")
            continue

        # 转换为 datetime 类型
        try:
            t1 = pd.to_datetime(time1)
            t2 = pd.to_datetime(time2)
        except Exception:
            result.append("时间格式错误")
            continue

        # 比较时间差
        time_diff = (t1 - t2).total_seconds() / 3600  # 单位为小时
        if time_diff < 0:
            result.append(f"阳单先到达{abs(round(time_diff, 2))}小时")
        elif time_diff > 0:
            result.append(f"阴单先到达{round(time_diff, 2)}小时")
        else:
            result.append("同时到达")

    df[RowName.YY_Delivered_Time] = result

    # 保存结果
    # output_path = file_path.replace(".xlsx", "_带间隔.xlsx")
    df.to_excel(file_path, index=False)
    print(f"✅ 处理完成，已保存为：{file_path}")


def calculate_sign_time_distribution(file_path):
    df = pd.read_excel(file_path)

    if RowName.YY_Delivered_Time not in df.columns:
        print("❌ 未找到“签收时间_间隔”列，请检查文件内容。")
        return

    if RowName.Create_Time not in df.columns:
        print("❌ 未找到“创建时间”列，请检查文件内容。")
        return

    # 转换“创建时间”为日期
    df[RowName.Create_Time] = pd.to_datetime(df[RowName.Create_Time], errors='coerce')
    df = df.dropna(subset=[RowName.Create_Time])

    df[RowName.YY_Delivered_Time] = df[RowName.YY_Delivered_Time].fillna("").astype(str)
    df["创建日期"] = df[RowName.Create_Time].dt.date

    grouped = df.groupby("创建日期")

    print("📊 按“创建时间”分组统计结果：")
    tat = get_token()
    for date, group in grouped:
        total = len(group)
        yang_count = group[RowName.YY_Delivered_Time].str.contains("阳单先到达").sum()
        yin_count = group[RowName.YY_Delivered_Time].str.contains("阴单先到达").sum()
        empty_count = (group[RowName.YY_Delivered_Time] == "").sum()

        text = f"\n订单总数：{total}"
        text += f"\n阳单先到达：({yang_count}, {yang_count / total:.2%})"
        text += f"\n阴单先到达：({yin_count}, {yin_count / total:.2%})"
        text += f"\n均未到达：({empty_count}, {empty_count / total:.2%})"

        date_text = f"\n📅 日期: {date}" + text
        print(date_text)

        formatted_date = date.strftime("%Y/%m/%d")
        gz_time = getYmd()
        yy_sheet_value(tat, [text], formatted_date, gz_time, ClientConstants.yy)


def calculate_sum_up_distribution(file_path):
    df = pd.read_excel(file_path)

    if RowName.YY_Delivered_Time not in df.columns:
        print("❌ 未找到“签收时间_间隔”列，请检查文件内容。")
        return

    total = len(df)
    if total == 0:
        print("⚠️ 文件中无数据。")
        return

    col = df[RowName.YY_Delivered_Time].fillna("").astype(str)

    yang_count = col.str.contains("阳单先到达").sum()
    yin_count = col.str.contains("阴单先到达").sum()
    empty_count = (col == "").sum()

    # ✅ 打印创建时间列中的最早和最晚时间（仅日期部分）
    try:
        create_times = pd.to_datetime(df[RowName.Create_Time], errors='coerce')
        create_times = create_times.dropna()
        if not create_times.empty:
            min_date = create_times.min().strftime("%Y-%m-%d")
            max_date = create_times.max().strftime("%Y-%m-%d")
            print(f"📅 最早创建时间：{min_date}")
            print(f"📅 最晚创建时间：{max_date}")
        else:
            print("⚠️ 创建时间列中无有效日期，无法提取最早和最晚时间。")
    except Exception as e:
        print(f"❌ 创建时间解析失败: {e}")

    print(f"📊 {min_date}_{max_date}_统计结果（共 {total} 单）：")
    print(f"✅ 阳单先到达：{yang_count} 行，占比 {yang_count / total:.2%}")
    print(f"✅ 阴单先到达：{yin_count} 行，占比 {yin_count / total:.2%}")
    print(f"🔲 均未到达：{empty_count} 行，占比 {empty_count / total:.2%}")


def fenxi(output):
    results1 = extract_and_process_data(output, RowName.Yang_Track_State, 100, RowName.Yang_Num)
    all_maps1 = {
        CourierStateMapKey.not_yet_map: results1[CourierStateMapKey.not_yet_map],
        CourierStateMapKey.pre_ship_map: results1[CourierStateMapKey.pre_ship_map],
        CourierStateMapKey.unpaid_map: results1[CourierStateMapKey.unpaid_map],
        CourierStateMapKey.delivered_map: results1[CourierStateMapKey.delivered_map],
        CourierStateMapKey.no_tracking_map: results1[CourierStateMapKey.no_tracking_map],
        CourierStateMapKey.tracking_map: results1[CourierStateMapKey.tracking_map],
        CourierStateMapKey.delivered_time_map: results1[CourierStateMapKey.delivered_time_map],
    }
    column_mapping1 = {
        CourierStateMapKey.not_yet_map: RowName.Yang_Track_State,
        CourierStateMapKey.pre_ship_map: RowName.Yang_Track_State,
        CourierStateMapKey.unpaid_map: RowName.Yang_Track_State,
        CourierStateMapKey.delivered_map: RowName.Yang_Track_State,
        CourierStateMapKey.no_tracking_map: RowName.Yang_Track_State,
        CourierStateMapKey.tracking_map: RowName.Yang_Track_State,
        CourierStateMapKey.delivered_time_map: RowName.Yang_Delivered_Time,
    }
    update_courier_status(output, all_maps1, wl=RowName.Yang_Num, column_map=column_mapping1)

    results2 = extract_and_process_data(output, RowName.Yin_Track_State, 100, RowName.Yin_Num)
    all_maps2 = {
        CourierStateMapKey.not_yet_map: results2[CourierStateMapKey.not_yet_map],
        CourierStateMapKey.pre_ship_map: results2[CourierStateMapKey.pre_ship_map],
        CourierStateMapKey.unpaid_map: results2[CourierStateMapKey.unpaid_map],
        CourierStateMapKey.delivered_map: results2[CourierStateMapKey.delivered_map],
        CourierStateMapKey.no_tracking_map: results2[CourierStateMapKey.no_tracking_map],
        CourierStateMapKey.tracking_map: results2[CourierStateMapKey.tracking_map],
        CourierStateMapKey.delivered_time_map: results2[CourierStateMapKey.delivered_time_map],
    }
    column_mapping2 = {
        CourierStateMapKey.not_yet_map: RowName.Yin_Track_State,
        CourierStateMapKey.pre_ship_map: RowName.Yin_Track_State,
        CourierStateMapKey.unpaid_map: RowName.Yin_Track_State,
        CourierStateMapKey.delivered_map: RowName.Yin_Track_State,
        CourierStateMapKey.no_tracking_map: RowName.Yin_Track_State,
        CourierStateMapKey.tracking_map: RowName.Yin_Track_State,
        CourierStateMapKey.delivered_time_map: RowName.Yin_Delivered_Time,
    }
    update_courier_status(output, all_maps2, wl=RowName.Yin_Num, column_map=column_mapping2)

    compare_delivery_times(output)
    calculate_sign_time_distribution(output)
    calculate_sum_up_distribution(output)


if __name__ == '__main__':
    select = "请选择功能："
    select += "\n1：🍺合并阴阳单☯️"
    select += "\n2：📊分析阴阳单☯️"
    select += "\n"
    select_input = input(select)

    if select_input == "1":
        dxm_input = input("请输入店小秘文件路径：")
        omp_input = input("请输入领星OMP文件路径：")
        output_dir = "/Users/zkp/Desktop/B&Y/yd/yd_analyse/"
        compare_tracking_numbers(dxm_input, omp_input, output_dir)
    elif select_input == "2":
        input_path = input("请输入源文件路径：")
        fenxi(input_path)
    else:
        print("🈚️此项功能！")
