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


def get_filename_without_extension(file_path):
    """
    获取路径的文件名（不含后缀）
    """
    filename = os.path.basename(file_path)  # 获取文件名（包含后缀）
    name_without_extension = os.path.splitext(filename)[0]  # 去掉后缀
    return name_without_extension


def ensure_directory_exists(dir_path):
    """
    确保文件夹存在，不存在则创建
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"文件夹已创建: {dir_path}")
    else:
        print(f"文件夹已存在: {dir_path}")


def round2(nums):
    """
    四舍五入，保留两位数
    """
    return round(nums, 2)


def isinstanceNums(value):
    """
    判断 value 的数据类型是否为整数（int）或浮点数（float）
    """
    return isinstance(value, (int, float))


def current_dir():
    """
    获取当前文件所在的目录
    """
    return os.path.dirname(os.path.abspath(__file__))
