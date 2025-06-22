from datetime import datetime, timezone, timedelta

import pandas as pd

from xinshili.utils import convert_china_to_us


def process_tracking_time1(file_path):
    df = pd.read_excel(file_path)

    df_filtered = df[~df['Courier/快递'].str.lower().isin(['unpaid', 'delivered', "irregular_no_tracking"])].copy()

    intervals = []
    states = []

    us_time_utc8 = convert_china_to_us(datetime.now(), offset_hours=-8)
    us_tz = timezone(timedelta(hours=-8))  # 与 convert_china_to_us 中的 offset_hours 保持一致

    for idx, row in df_filtered.iterrows():
        date_str = str(row.get("LatestEventSfDate/最新事件时间", "")).strip()
        time_str = str(row.get("LatestEventSfTime/最新事件时间", "")).strip()
        creation_time_str = str(row.get("Creation time/创建时间", "")).strip()

        try:
            if date_str and time_str and date_str.lower() != "nan" and time_str.lower() != "nan":
                event_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M").replace(tzinfo=us_tz)
                diff = us_time_utc8 - event_time
            elif creation_time_str:
                creation_ch_time = datetime.strptime(creation_time_str, "%Y-%m-%d %H:%M:%S")
                creation_us_time = convert_china_to_us(creation_ch_time, offset_hours=-8)
                diff = us_time_utc8 - creation_us_time
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
            intervals.append(None)
            states.append("")
            print(f"⚠️ 第 {idx} 行处理失败: {e}")

    df_filtered["TrackTimeInterval/跟踪时间间隔"] = intervals
    df_filtered["TrackTimeIntervalState/跟踪时间间隔状态"] = states

    df.update(df_filtered)
    df.to_excel(file_path, index=False)


if __name__ == '__main__':
    process_tracking_time1("/Users/zkp/Downloads/创建时间19_74_副本.xlsx")
    # process_tracking_time1("/Users/zkp/Downloads/创建时间19_74_副本2.xlsx")
