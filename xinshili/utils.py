import requests
import calendar
from datetime import datetime
import os
import subprocess
import pandas as pd


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
    return 7.31


def get_yd():
    # 获取今天的日期
    today = datetime.now()
    # 格式化为 "月日"
    month_day = today.strftime("%m%d")
    return month_day


def delete_file(file_path):
    """
    删除指定的文件
    :param file_path: 要删除的文件的绝对路径
    """
    try:
        if os.path.exists(file_path):  # 检查文件是否存在
            os.remove(file_path)  # 删除文件
            print(f"文件 {file_path} 已成功删除")
        else:
            print(f"文件 {file_path} 不存在")
    except Exception as e:
        print(f"删除文件时发生错误: {e}")


def open_dir(folder_path):
    # 使用 os.system 调用 macOS 的 open 命令
    # os.system(f"open {folder_path}")
    subprocess.run(["open", folder_path])


def dirname(absolute_path):
    return os.path.dirname(absolute_path)  # 获取文件所在路径


def get_filename_without_extension(file_path):
    """
    获取路径的文件名（不含后缀）
    """
    filename = os.path.basename(file_path)  # 获取文件名（包含后缀）
    name_without_extension = os.path.splitext(filename)[0]  # 去掉后缀
    return name_without_extension


def get_filename_with_extension(file_path):
    """
    获取路径的文件名（含后缀）
    """
    filename = os.path.basename(file_path)  # 获取文件名（包含后缀）
    return filename


def ensure_directory_exists(dir_path):
    """
    确保文件夹存在，不存在则创建
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"文件夹已创建: {dir_path}")
    else:
        print(f"文件夹已存在: {dir_path}")


def rename(old_file_path, new_file_path):
    os.rename(old_file_path, new_file_path)


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


def get_file_dir(file_path):
    """
    获取当前文件所在的目录
    """
    return os.path.dirname(file_path)


def convert_csv_to_xlsx(csv_file, xlsx_file):
    """
    将 CSV 文件转换为 XLSX 文件格式。

    :param csv_file: 输入的 CSV 文件路径
    :param xlsx_file: 输出的 XLSX 文件路径
    """
    try:
        # 读取 CSV 文件
        data = pd.read_csv(csv_file)

        # 将数据写入 XLSX 文件
        data.to_excel(xlsx_file, index=False, engine="openpyxl")

        print(f"文件已成功转换为 XLSX 格式: {xlsx_file}")
    except Exception as e:
        print(f"转换过程中发生错误: {e}")


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def day_of_month():
    return datetime.today().day


def get_days_in_current_month():
    """
    获取当前月份的天数。
    """
    # 获取当前日期
    today = datetime.now()
    year = today.year
    month = today.month

    # 使用 calendar.monthrange 获取当前月份的天数
    _, days_in_month = calendar.monthrange(year, month)
    return days_in_month


def getYmd():
    # 获取今天的日期
    today = datetime.today()
    # 格式化为 "%Y/%m/%d" 格式
    formatted_today = today.strftime("%Y/%m/%d")
    # print(formatted_today)
    return formatted_today


def is_us_weekend(date_str):
    """
    中国和美国的时差相差：13-16 个钟头，目前日期的单位最小是日期，没有到小时，所以这里我们默认和美国相差一天，
    也就是中国时间周日为美国的周六，中国时间周一为美国的周日
    """
    # 解析字符串为 datetime 对象
    date_obj = datetime.strptime(date_str, "%Y/%m/%d")

    # 判断是否为 周日（6）或者周一 (0)，即为美国的周六和周日
    return date_obj.weekday()
