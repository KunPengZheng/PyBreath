from datetime import datetime, timezone, timedelta

import pandas as pd


def convert_china_to_us(china_time: datetime, offset_hours: int = -8) -> datetime:
    """
    将中国时间转换为美国时间，使用固定时差（忽略夏令时）
    :param china_time: 中国时间 datetime 对象
    :param offset_hours: 美国与 UTC 的偏移（如 -8 表示 UTC-8）
    :return: 美国时间（不含夏令时调整）
    """
    if not isinstance(china_time, datetime):
        raise ValueError("china_time 必须是 datetime 类型")

    china_tz = timezone(timedelta(hours=8))
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

    # 代码运行时的中国时间，转换为美国时间
    us_now = convert_china_to_us(datetime.now(), offset_hours=-8)
    # 美区
    us_tz = timezone(timedelta(hours=-8))

    for idx, row in df_filtered.iterrows():
        try:
            # ---------- 时间来源 ----------
            possession_str = str(row.get("PossessionSfDate/揽收时间", "")).strip()
            creation_str = str(row.get("OutboundTime/出库时间", "")).strip()

            base_time = None
            if possession_str and possession_str.lower() != "nan":  # PossessionSfDate/揽收时间 存在数据，优先使用
                # 揽收时间是美国时间，不需要转换
                base_time = datetime.strptime(possession_str, "%Y-%m-%d")
                base_us_time = base_time.replace(tzinfo=us_tz)  # 保持一致，加上 tzinfo
            elif creation_str and creation_str.lower() != "nan":  # PossessionSfDate/揽收时间 存在数据，证明是not-yet这些状态，则使用出库时间
                # 出库时间是中国时间，需要转换
                creation_china_time = datetime.strptime(creation_str, "%Y-%m-%d %H:%M:%S")
                base_us_time = convert_china_to_us(creation_china_time, offset_hours=-8)
            else:
                base_us_time = None

            if base_us_time:
                base_diff = us_now - base_us_time
                base_hours = round(base_diff.total_seconds() / 3600, 2)

                if base_hours > 72:
                    intervals.append(base_hours)
                    states.append("无法替换")
                    continue  # 不再处理事件时间，直接进入下一行

            # ---------- 最新事件时间判断 ----------
            date_str = str(row.get("LatestEventSfDate/最新事件时间", "")).strip()
            time_str = str(row.get("LatestEventSfTime/最新事件时间", "")).strip()

            if date_str and time_str and date_str.lower() != "nan" and time_str.lower() != "nan":
                event_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M").replace(tzinfo=us_tz)
                diff = us_now - event_time
            elif creation_str and creation_str.lower() != "nan":
                creation_time = datetime.strptime(creation_str, "%Y-%m-%d %H:%M:%S")
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
                elif hours >= 24:
                    states.append("预备阳单")
                else:
                    states.append("")
            else:
                intervals.append(None)
                states.append("")

        except Exception as e:
            print(f"⚠️ 第 {idx} 行处理失败: {e}")
            intervals.append(None)
            states.append("")

    # 写入结果列
    df_filtered["TrackTimeInterval/跟踪时间间隔"] = intervals
    df_filtered["TrackTimeIntervalState/跟踪时间间隔状态"] = states

    # 用处理后数据更新原始表
    df.update(df_filtered)
    df.to_excel(file_path, index=False)


if __name__ == '__main__':
    # process_tracking_time1("/Users/zkp/Downloads/创建时间19_74_副本.xlsx")
    process_tracking_time1("/Users/zkp/Downloads/创建时间19_74_副本2.xlsx")
