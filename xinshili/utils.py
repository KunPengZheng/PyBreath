import re

import requests
import calendar
from datetime import datetime
import os
import subprocess
import pandas as pd
import holidays
import platform
import uuid
import math
import platform
import subprocess
import sys


def round_up_to_2_decimal(x):
    # 乘1000保留3位，减去乘100保留2位 → 判断是否有第3位小数
    scaled = x * 1000
    remainder = scaled % 10
    if remainder > 0:
        # 有第三位小数，则进1
        return math.ceil(x * 100) / 100
    else:
        return round(x, 2)


def get_usd_to_cny_rate():
    url = "https://api.exchangerate.host/live?access_key=c9ba58232ee9b955236a7def78ba88d2&currencies=CNY"
    try:
        response = requests.get(url)
        data = response.json()
        # 获取 USD 对 CNY 的汇率
        rate = data["quotes"]["USDCNY"]
        # exchange_rate = round(rate, 2)
        exchange_rate = round_up_to_2_decimal(rate)
        print(f"当前 USD 对 CNY 的汇率是：{rate}, {exchange_rate}")
        return exchange_rate
    except Exception as e:
        print(f"获取汇率失败：{e}")
        return None


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
            # print(f"文件 {file_path} 已成功删除")
        else:
            print(f"文件 {file_path} 不存在")
    except Exception as e:
        print(f"删除文件时发生错误: {e}")


def open_dir(folder_path):
    system_platform = platform.system()

    try:
        if system_platform == "Darwin":  # macOS
            subprocess.run(["open", folder_path])
        elif system_platform == "Windows":
            os.startfile(folder_path)
        elif system_platform == "Linux":
            subprocess.run(["xdg-open", folder_path])
        else:
            print(f"不支持的系统: {system_platform}")
    except Exception as e:
        print(f"打开文件夹失败: {e}")


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


def get_file_ext(file_path):
    """
    获取文件的后缀
    """
    ext = os.path.splitext(file_path)[1]  # 获取扩展名，包括“.”
    return ext


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
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")


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


def get_weekday(date_str):
    weekday_num = is_us_weekend(date_str)

    # 将数字转为中文星期
    weekday_chinese = {
        0: "星期一",
        1: "星期二",
        2: "星期三",
        3: "星期四",
        4: "星期五",
        5: "星期六",
        6: "星期天"
    }
    return weekday_chinese[weekday_num]


# 查询美国节日
def get_american_holiday(date):
    us_holidays = holidays.US(years=date.year)
    if date in us_holidays:
        return us_holidays[date]
    return None


# 查询中国节日
def get_chinese_holiday(date):
    cn_holidays = holidays.China(years=date.year)
    if date in cn_holidays:
        return cn_holidays[date]
    return None


# 自然排序的辅助函数
def natural_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]


def rename_images_by_filename(folder_path, alphabet, start_num, end_num):
    """
    安全批量重命名图片，保持顺序不变，使用 _temp 避免命名冲突
    :param folder_path: 图片所在文件夹路径
    :param alphabet: 新文件名前缀
    :param start_num: 起始编号
    :param end_num: 结束编号
    """
    valid_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

    image_files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(valid_exts) and os.path.isfile(os.path.join(folder_path, f))
    ]

    # 自然排序
    image_files.sort(key=natural_key)

    if len(image_files) > (end_num - start_num + 1):
        print(f"📛 图片数量超出编号范围（最多 {end_num - start_num + 1} 张），停止处理。")
        return

    # 第一步：临时加 "_temp" 后缀
    temp_names = []
    for filename in image_files:
        old_path = os.path.join(folder_path, filename)
        name, ext = os.path.splitext(filename)
        temp_name = f"{name}_temp{ext}"
        temp_path = os.path.join(folder_path, temp_name)
        os.rename(old_path, temp_path)
        temp_names.append(temp_name)

    # 第二步：重命名为目标格式
    count = start_num
    for temp_name in temp_names:
        temp_path = os.path.join(folder_path, temp_name)
        ext = os.path.splitext(temp_name)[1].lower()
        new_filename = f"{alphabet}{count}{ext}"
        new_path = os.path.join(folder_path, new_filename)
        os.rename(temp_path, new_path)
        print(f"✅ {temp_name} → {new_filename}")
        count += 1

    print("🎉 重命名完成。")


def get_computer_model():
    system = platform.system()

    try:
        if system == "Windows":
            result = subprocess.check_output(["wmic", "computersystem", "get", "model"], shell=True)
            return result.decode().split("\n")[1].strip()

        elif system == "Darwin":  # macOS
            result = subprocess.check_output(["system_profiler", "SPHardwareDataType"])
            for line in result.decode().splitlines():
                if "Model Identifier" in line:
                    return line.split(":")[1].strip()

        elif system == "Linux":
            try:
                # 尝试读取 product_name 文件
                with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
                    return f.read().strip()
            except FileNotFoundError:
                # 使用 dmidecode（需要 root 权限）
                result = subprocess.check_output(["sudo", "dmidecode", "-s", "system-product-name"])
                return result.decode().strip()

        else:
            return f"Unsupported OS: {system}"

    except Exception as e:
        return f"Error retrieving model: {e}"
