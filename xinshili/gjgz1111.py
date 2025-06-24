from datetime import datetime, timezone, timedelta

import pandas as pd
import os

from xinshili.fs_utils_plus import get_token, dimension_range, FsConstants, value_range


def convert_china_to_us(china_time: datetime, offset_hours: int = -8) -> datetime:
    """
    将中国时间转换为美国时间，使用固定时差（忽略夏令时）
    :param china_time: 中国时间 datetime 对象
    :param offset_hours: 美国与 UTC 的偏移
        （如 -8 表示 UTC-8，冬令时，通常称为 PST（Pacific Standard Time））
        （如 -7 表示 UTC-7，夏令时，通常称为 PDT（Pacific Daylight Time））
    :return: 美国时间（不含夏令时调整）
    """
    if not isinstance(china_time, datetime):
        raise ValueError("china_time 必须是 datetime 类型")

    china_tz = timezone(timedelta(hours=8))  # 中国时间固定 UTC+8
    us_fixed_tz = timezone(timedelta(hours=offset_hours))

    # 将 naive datetime 标准化为中国时间
    china_time = china_time.replace(tzinfo=china_tz)

    # 转换为美国固定时差时间
    us_time = china_time.astimezone(us_fixed_tz)

    return us_time


def process_tracking_time1(file_path):
    df = pd.read_excel(file_path)

    # 先排除特定状态的数据
    df_filtered = df[~df['Courier/快递'].str.lower().isin(['unpaid', 'delivered', "irregular_no_tracking"])].copy()

    intervals = []
    states = []
    yd_states = []
    track_times = []

    # 代码运行时的中国时间，转换为美国时间
    us_now = convert_china_to_us(datetime.now(), offset_hours=-8)
    # 美区
    us_tz = timezone(timedelta(hours=-8))

    for idx, row in df_filtered.iterrows():
        try:
            # ---------- 时间来源 ----------
            possession_str = str(row.get("PossessionSfDate/揽收时间", "")).strip()
            outbound_time_str = str(row.get("OutboundTime/出库时间", "")).strip()

            # base_time = None
            # if possession_str and possession_str.lower() != "nan":  # PossessionSfDate/揽收时间 存在数据，优先使用
            #     # 揽收时间是美国时间，不需要转换
            #     base_time = datetime.strptime(possession_str, "%Y-%m-%d")
            #     base_us_time = base_time.replace(tzinfo=us_tz)  # 保持一致，加上 tzinfo
            if outbound_time_str and outbound_time_str.lower() != "nan":  # PossessionSfDate/揽收时间 存在数据，证明是not-yet这些状态，则使用出库时间
                # 出库时间是中国时间，需要转换
                creation_china_time = datetime.strptime(outbound_time_str, "%Y-%m-%d %H:%M:%S")
                base_us_time = convert_china_to_us(creation_china_time, offset_hours=-8)
            else:
                base_us_time = None

            if base_us_time:
                base_diff = us_now - base_us_time
                base_hours = round(base_diff.total_seconds() / 3600, 2)

                if base_hours > 72:
                    intervals.append(base_hours)
                    states.append("超时")
                    continue  # 不再处理事件时间，直接进入下一行

            # ---------- 最新事件时间判断 ----------
            date_str = str(row.get("LatestEventSfDate/最新事件时间", "")).strip()
            time_str = str(row.get("LatestEventSfTime/最新事件时间", "")).strip()

            if date_str and time_str and date_str.lower() != "nan" and time_str.lower() != "nan":
                event_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M").replace(tzinfo=us_tz)
                diff = us_now - event_time
            elif outbound_time_str and outbound_time_str.lower() != "nan":
                creation_time = datetime.strptime(outbound_time_str, "%Y-%m-%d %H:%M:%S")
                diff = us_now - convert_china_to_us(creation_time, offset_hours=-8)
            else:
                diff = None

            if diff is not None:
                hours = round(diff.total_seconds() / 3600, 2)
                intervals.append(hours)

                if hours >= 72:
                    states.append("无法替换")
                elif hours >= 48:
                    states.append("阳单替换")
                    yd_states.append("YD")
                elif hours >= 24:
                    states.append("预备阳单")
                    yd_states.append("YD")
                else:
                    states.append("")
                    yd_states.append("")
            else:
                intervals.append(None)
                states.append("")
                yd_states.append("")

            track_times.append(us_now)

        except Exception as e:
            print(f"⚠️ 第 {idx} 行处理失败: {e}")
            intervals.append(None)
            states.append("")
            yd_states.append("")
            track_times.append(us_now)

    # 写入结果列
    df_filtered["TrackTimeInterval/跟踪时间间隔"] = intervals
    df_filtered["TrackTimeIntervalState/跟踪时间间隔状态"] = states
    df_filtered["YD/yd状态"] = yd_states
    df_filtered["Tacking_Time/追踪时间"] = track_times

    # 用处理后数据更新原始表
    df.update(df_filtered)
    df.to_excel(file_path, index=False)


def create_fs_xlsx_file(file_path):
    # 定义表头
    columns = [
        "创建时间", "出库时间", "订单号", "运单号",
        "轨迹状态", "最新轨迹位置", "最新轨迹时间", "追踪时间",
        "时间间隔", "处理状态"
    ]

    # 创建空的 DataFrame 并写入文件（覆盖或新建）
    df = pd.DataFrame(columns=columns)
    df.to_excel(file_path, index=False)
    print(f"✅ 文件已{'创建' if not os.path.exists(file_path) else '清空并重建'}：{file_path}")


def export_yd_data(source_file, target_file):
    # 读取文件1（源文件）
    df = pd.read_excel(source_file)

    # 筛选 "YD/yd状态" 为 "YD" 的行
    df_filtered = df[df["YD/yd状态"].astype(str).str.upper() == "YD"].copy()

    # 构造“最新轨迹时间”字段：拼接 日期 + 空格 + 时间
    df_filtered["最新轨迹时间"] = df_filtered["LatestEventSfDate/最新事件时间"].astype(str).str.strip() + " " + \
                                  df_filtered["LatestEventSfTime/最新事件时间"].astype(str).str.strip()

    # 构造目标列的数据
    export_df = pd.DataFrame({
        "创建时间": df_filtered["Creation time/创建时间"],
        "出库时间": df_filtered["OutboundTime/出库时间"],
        "订单号": df_filtered["Platform Number/平台单号"],
        "运单号": df_filtered["Tracking No./物流跟踪号"],
        "轨迹状态": df_filtered["Courier/快递"],
        "最新轨迹位置": df_filtered["LatestEventSfSite/最新事件地点"],
        "最新轨迹时间": df_filtered["最新轨迹时间"],
        "追踪时间": df_filtered["Tacking_Time/追踪时间"],
        "时间间隔": df_filtered["TrackTimeInterval/跟踪时间间隔"],
        "处理状态": df_filtered["TrackTimeIntervalState/跟踪时间间隔状态"],
    })

    # 写入到目标文件（如果存在则覆盖）
    export_df.to_excel(target_file, index=False)
    print(f"✅ 已成功导出 YD 数据至：{target_file}")

    return len(export_df)


if __name__ == '__main__':
    xlsx1 = "/Users/zkp/Downloads/创建时间21_59_副本.xlsx"
    process_tracking_time1(xlsx1)
    xlsx2 = "/Users/zkp/Desktop/B&Y/轨迹统计/xyl_track/xyl_track_merger_temp.xlsx"
    # create_fs_xlsx_file(xlsx2)
    data_len = export_yd_data(xlsx1, xlsx2)
    print(f"dsdsds:{data_len}")

    # token = get_token()
    # dimension_range(token, FsConstants.gjgz_token, "yTIUrm", 1, 10, majorDimension="COLUMNS")
    # value_range(token, FsConstants.gjgz_token, "yTIUrm", "A1:I41")
