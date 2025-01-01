import requests
from datetime import datetime
import os
import subprocess


def get_usd_to_cny_rate():
    # url = "https://api.exchangerate.host/live?access_key=c9ba58232ee9b955236a7def78ba88d2&currencies=CNY"
    # try:
    #     response = requests.get(url)
    #     data = response.json()
    #     # 获取 USD 对 CNY 的汇率
    #     rate = data["quotes"]["USDCNY"]
    #     exchange_rate = round(rate, 2) + 0.01
    #     print(f"当前 USD 对 CNY 的汇率是：{rate}, {exchange_rate}")
    #     return exchange_rate
    # except Exception as e:
    #     print(f"获取汇率失败：{e}")
    #     return None
    return 7.36


def get_yd():
    # 获取今天的日期
    today = datetime.now()
    # 格式化为 "月日"
    month_day = today.strftime("%m%d")
    return month_day


def open_dir(folder_path):
    # 使用 os.system 调用 macOS 的 open 命令
    # os.system(f"open {folder_path}")
    subprocess.run(["open", folder_path])
