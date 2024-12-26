import requests
from datetime import datetime


def get_usd_to_cny_rate():
    url = "https://api.exchangerate.host/live?access_key=c9ba58232ee9b955236a7def78ba88d2&currencies=CNY"
    try:
        response = requests.get(url)
        data = response.json()
        # 获取 USD 对 CNY 的汇率
        rate = data["quotes"]["USDCNY"]
        print(f"当前 USD 对 CNY 的汇率是：{rate}")
        return rate
    except Exception as e:
        print(f"获取汇率失败：{e}")
        return None


def get_yd():
    # 获取今天的日期
    today = datetime.now()
    # 格式化为 "月日"
    month_day = today.strftime("%m%d")
    return month_day
