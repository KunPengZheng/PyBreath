# coding=gbk

import csv
import ctypes
import re
from datetime import datetime
import os

from base import api
from base.api import TdxHqApi


def is_chinese_stock_code(code: str) -> bool:
    """
     判断一个代码是否为中国 A 股（包括沪市、深市、科创板、创业板、北交所），
     排除 ETF、指数、基金、债券、B股 等。

     :param code: 股票代码字符串（6位）
     :return: 如果是 A 股代码，返回 True；否则返回 False。
     """
    if not isinstance(code, str) or len(code) != 6 or not code.isdigit():
        return False

    valid_prefixes = (
        "600", "601", "603", "605",  # 沪市主板
        "688", "689",  # 科创板
        "000", "001", "002", "003",  # 深市主板
        "300", "301", "302",  # 创业板
        "430", "830", "831", "832", "833", "834", "835", "837", "838", "839", "870", "871", "872", "873", "920",  # 北交所
    )

    return code.startswith(valid_prefixes)


def get_code_name(decoded_result):
    parsed_stocks_data = []

    lines = decoded_result.strip().split('\n')
    if not lines:
        print("没有获取到数据行。")
        return parsed_stocks_data

    # 处理表头行（去除空格、全角等）
    header_line = lines[0]
    headers = [h.strip().replace(' ', '').replace('　', '') for h in header_line.split('\t')]

    try:
        code_index = headers.index('代码')
        name_index = headers.index('名称')
    except ValueError as e:
        print(f"错误：找不到 '代码' 或 '名称' 列。{e}")
        return parsed_stocks_data

    for line in lines[1:]:
        # 跳过重复的表头行（有些批次会返回表头）
        if line.strip() == header_line or ('代码' in line and '名称' in line):
            continue

        columns = line.split('\t')
        if code_index < len(columns) and name_index < len(columns):
            parsed_stocks_data.append({
                '代码': columns[code_index].strip(),
                '名称': columns[name_index].strip()
            })
        else:
            print(f"?? 跳过列数不足的行：{line}")

    return parsed_stocks_data


def get_gd_number(data_string):
    # 按行分割字符串
    lines = data_string.strip().split('\n')

    # 提取数据的字典
    shareholder_research_info = {}

    # 遍历每一行，从第二行开始（跳过标题行）
    for line in lines[1:]:
        # 使用 split() 不带参数来按任意空白字符分割，并自动处理多个空格
        parts = line.split()

        # 确保行有足够的列
        if len(parts) >= 4:  # 至少有“类别”、“文件”、“开始”、“长度”四列
            category = parts[0]  # 第一列是“内容打印类别”

            if category == "股东研究":
                # 类别匹配，获取对应列的值
                file_name = parts[1]
                start_pos = int(parts[2])  # 转换为整数
                length = int(parts[3])  # 转换为整数

                shareholder_research_info = {
                    "文件": file_name,
                    "开始": start_pos,
                    "长度": length
                }
                break  # 找到后就可以停止遍历了

    # # 打印结果
    # if shareholder_research_info:
    #     print("已找到 '股东研究' 的对应信息：")
    #     print(f"文件: {shareholder_research_info['文件']}")
    #     print(f"开始: {shareholder_research_info['开始']}")
    #     print(f"长度: {shareholder_research_info['长度']}")
    # else:
    #     print("未找到 '股东研究' 的对应信息。")
    return shareholder_research_info


# --- 1. 隔离“股东人数变化”数据块 ---
def extract_shareholder_change_block(full_text):
    start_marker = "【5.股东人数变化】"
    # all_blocks = re.findall(rf"({re.escape(start_marker)}[\s\S]*?)(?=\n【\d+\.|\Z)", full_text, re.DOTALL)
    all_blocks = re.findall(f"({re.escape(start_marker)}[\\s\\S]*?)(?=\\n【\\d+\\.|\Z)", full_text, re.DOTALL)
    if all_blocks:
        return all_blocks[-1]
    return None


# --- 2. 解析“股东人数变化”的数据块 ---
def parse_shareholder_data(block_string):
    parsed_records = []
    if not block_string:
        return parsed_records

    lines = block_string.strip().split('\n')

    header_line_index = -1
    for i, line in enumerate(lines):
        if "│截止日期" in line and "股东人数(户)" in line:
            header_line_index = i
            break

    if header_line_index == -1:
        # print("错误：在股东人数变化块中未找到表头行。") # Removed print for cleaner function output
        return parsed_records

    header_line = lines[header_line_index]
    headers_raw = [h.strip() for h in header_line.split('│')]
    headers = [h for h in headers_raw if h]

    try:
        date_idx = headers.index('截止日期')
        shareholders_idx = headers.index('股东人数(户)')
    except ValueError as e:
        # print(f"错误：表头中缺少必需的列名 ('截止日期' 或 '股东人数(户)'）。{e}") # Removed print for cleaner function output
        return parsed_records

    for i in range(header_line_index + 2, len(lines)):
        line = lines[i]

        if '─' * 5 in line or not line.strip():
            break

        match = re.match(r'│\s*(\d{4}-\d{2}-\d{2})\s*│\s*([\s\d]+)\s*│', line)
        if match:
            try:
                date_str = match.group(1)
                shareholders_str = match.group(2).replace(' ', '')

                record_date = datetime.strptime(date_str, '%Y-%m-%d')
                shareholders_count = int(shareholders_str)

                parsed_records.append({
                    '截止日期': record_date,
                    '股东人数(户)': shareholders_count
                })
            except (ValueError, IndexError) as e:
                # print(f"警告：解析股东人数行失败或数据格式不正确: '{line}'. 错误: {e}") # Removed print for cleaner function output
                continue
        else:
            continue
    return parsed_records


# --- 3. 获取特定年月的最新一天股东人数 ---
def get_latest_shareholders_by_month(parsed_records, target_years_months):
    results = {}
    for year, month in target_years_months:
        latest_date_in_month = None
        latest_shareholders_count = None

        for record in parsed_records:
            record_date = record['截止日期']
            if record_date.year == year and record_date.month == month:
                if latest_date_in_month is None or record_date > latest_date_in_month:
                    latest_date_in_month = record_date
                    latest_shareholders_count = record['股东人数(户)']

        if latest_date_in_month:
            results[f"{year}-{month:02d}"] = {
                "日期": latest_date_in_month.strftime('%Y-%m-%d'),
                "股东人数": latest_shareholders_count
            }
        else:
            results[f"{year}-{month:02d}"] = {
                "日期": "未找到",
                "股东人数": "未找到"
            }
    return results


def get_most_recent_data(parsed_records):
    if not parsed_records:
        return None

    sorted_records = sorted(parsed_records, key=lambda x: x['截止日期'], reverse=True)

    # The first element after sorting will be the most recent
    return sorted_records[0]


def parse(full_content):
    shareholder_block = extract_shareholder_change_block(full_content)
    result_data = []

    if shareholder_block:
        # 1. 解析数据块
        parsed_shareholder_data = parse_shareholder_data(shareholder_block)

        # --- 最新股东人数 ---
        # most_recent_record = get_most_recent_data(parsed_shareholder_data)
        # if most_recent_record:
        #     result_data.append({
        #         "最新日期": most_recent_record['截止日期'].strftime('%Y-%m-%d'),
        #         "股东人数": most_recent_record['股东人数(户)']
        #     })
        # else:
        #     result_data.append({"日期": "未找到", "股东人数": "未找到"})

        # 2. 获取特定年月的最新一天股东人数
        target_months = [
            (2025, 3),
            (2024, 12),
            (2024, 9),
            (2024, 6),
            (2024, 3)
        ]
        final_results = get_latest_shareholders_by_month(parsed_shareholder_data, target_months)

        for key, info in final_results.items():
            result_data.append({
                "指定日期": info['日期'],
                "股东人数": info['股东人数']
            })

        # 3. 获取 2025 年 3 月之后的所有数据（不止取最新）
        cutoff = (2025, 3)
        for record in parsed_shareholder_data:
            dt = record['截止日期']
            if (dt.year > cutoff[0]) or (dt.year == cutoff[0] and dt.month > cutoff[1]):
                result_data.append({
                    "日期": dt.strftime('%Y-%m-%d'),
                    "股东人数": record['股东人数(户)']
                })

    else:
        print("未能在提供的文本中找到 '股东人数变化' 的数据块。")

    return result_data


def read_code_name(file_path):
    data = []

    try:
        # 'r' 模式表示读取，encoding='utf-8-sig' 处理带BOM的UTF-8文件
        with open(file_path, 'r', newline='', encoding='gb18030') as csvfile:
            # 使用 DictReader 可以直接将每行读取为字典，字典的键是列头
            reader = csv.DictReader(csvfile)
            for row in reader:
                if '代码' in row and '名称' in row:
                    data.append({
                        '代码': row['代码'],
                        '名称': row['名称']
                    })
    except Exception as e:
        print(f"错误: {e}")

    return data


def write_code_name(gp_cvs):
    success, Count = api.get_security_count()
    if success != 1:
        raise ValueError("get_security_count != 1")
    total_securities = Count.value

    batch_size = 1000  # 每次获取的批次大小
    all_securities_data_code_name = []

    # 开始循环分批获取数据
    for start_index in range(0, total_securities, batch_size):
        # 计算当前批次需要获取的数量，确保不会超出总数
        requested_batch_count = min(batch_size, total_securities - start_index)
        current_count_param = ctypes.c_ushort(requested_batch_count)
        success, result_decode = api.get_security_list(start_index, current_count_param)

        if success == 1:
            get_code_name_arr = get_code_name(result_decode)
            all_securities_data_code_name.extend(get_code_name_arr)

    fieldnames = ['代码', '名称']  # 你可以包含其他列，即使它们暂时没有数据
    # 写入CSV文件
    try:
        # 'w' 模式表示写入，如果文件不存在则创建，如果存在则清空
        # newline='' 参数非常重要，可以防止在Windows上出现额外的空行
        with open(gp_cvs, 'w', newline='', encoding='gbk') as csvfile:
            # 创建一个DictWriter对象，它能根据字典的键将数据写入对应的列
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # 写入列头
            writer.writeheader()
            # 写入数据行
            for row_data in all_securities_data_code_name:
                # 你可以选择性地只写入'代码'和'名称'，其他列保持为空或不写入
                # 如果DictWriter的fieldnames包含了所有row_data的键，可以直接写入
                writer.writerow(row_data)
        print(f"数据已成功写入到 '{gp_cvs}'")

    except IOError as e:
        print(f"写入文件时发生错误: {e}")


def write_gdrs(gp_cvs, gdrs_csv):
    stock_data_csv = read_code_name(gp_cvs)

    columns = ["代码", "名称", "最新日期(股东人数)", "2025-03(股东人数)", "2024-12(股东人数)", "2024-09(股东人数)",
               "2024-06(股东人数)", "2024-03(股东人数)"]

    write_data = []
    total_written = 0

    # 写入表头（如果文件不存在）
    if not os.path.exists(gdrs_csv):
        with open(gdrs_csv, "w", newline="", encoding="gbk") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()

    for index, stock_info in enumerate(stock_data_csv):
        code_ = stock_info['代码']
        info_ = stock_info['名称']

        if is_chinese_stock_code(code_):
            success, result_decode = api.get_company_info_category(code_)
            shareholder_research_info = get_gd_number(result_decode)
            if shareholder_research_info:
                file_info = shareholder_research_info['文件']
                start_info = int(shareholder_research_info['开始'])
                length_info = int(shareholder_research_info['长度'])
                success, result_decode = api.get_company_info_content(code_, file_info, start_info, length_info)
                result_data = parse(result_decode)

                row_data = {col: "" for col in columns}
                row_data["代码"] = code_
                row_data["名称"] = info_

                for item in result_data:
                    item_ = item["股东人数"]
                    if '最新日期' in item:
                        row_data["最新日期(股东人数)"] = item_
                    elif '指定日期' in item:
                        special_date = item["指定日期"]
                        if special_date.startswith("2025-03"):
                            row_data["2025-03(股东人数)"] = item_
                        elif special_date.startswith("2024-12"):
                            row_data["2024-12(股东人数)"] = item_
                        elif special_date.startswith("2024-09"):
                            row_data["2024-09(股东人数)"] = item_
                        elif special_date.startswith("2024-06"):
                            row_data["2024-06(股东人数)"] = item_
                        elif special_date.startswith("2024-03"):
                            row_data["2024-03(股东人数)"] = item_

                write_data.append(row_data)

        # 每100条写一次
        if len(write_data) >= 100:
            with open(gdrs_csv, "a", newline="", encoding="gbk") as f:
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writerows(write_data)
            total_written += len(write_data)
            # print(f"已写入 {total_written} 条数据")
            write_data.clear()

    # 写入最后不足100条的数据
    if write_data:
        with open(gdrs_csv, "a", newline="", encoding="gbk") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writerows(write_data)
        total_written += len(write_data)
        print(f"已完成，总共写入 {total_written} 条数据")


if __name__ == '__main__':
    api.mark_code = 1

    if api.mark_code == 0:
        gp_cvs = "C:\\Users\\Administrator\\Documents\\sz2.csv"
        gdrs_csv = "C:\\Users\\Administrator\\Documents\\sz2_gdrs.csv"
    elif api.mark_code == 1:
        gp_cvs = "C:\\Users\\Administrator\\Documents\\sh2.csv"
        gdrs_csv = "C:\\Users\\Administrator\\Documents\\sh2_gdrs.csv"
    else:
        raise ValueError("mark异常")

    if api.ConnectionID != -1:
        write_code_name(gp_cvs)
        write_gdrs(gp_cvs, gdrs_csv)

    TdxHqApi.TdxHq_Disconnect(api.ConnectionID)
