import re
import os
import utils
from xinshili import openpyxl_utils
from xinshili.xlwings_utils import xw_map, beautify, xw_save, get_last_row_num, \
    get_range_row_value, set_cell_value, calculate_formula

"""
风向标:CZFF供应商对账表
"""


def write_data_to_sheet(sheet1, sheet2, columns1, columns2, exchange_rate):
    """
    从表1复制数据到表2
    """
    try:
        target_row = 2  # 表2从第2行开始写入
        for row in range(3, sheet1.max_row + 1):  # 跳过表1的第2行
            # 从表1获取数据,写入表2
            openpyxl_utils.set_cell_value(sheet2, target_row, columns2["日期"],
                                          openpyxl_utils.get_cell_value(sheet1, row,
                                                                        columns1["Paid Time"]))

            openpyxl_utils.set_cell_value(sheet2, target_row, columns2["订单单号"],
                                          openpyxl_utils.get_cell_value(sheet1, row,
                                                                        columns1["Order ID"]))

            openpyxl_utils.set_cell_value(sheet2, target_row, columns2["数量"],
                                          openpyxl_utils.get_cell_value(sheet1, row,
                                                                        columns1["Quantity"]))

            openpyxl_utils.set_cell_value(sheet2, target_row, columns2["款号"],
                                          openpyxl_utils.get_cell_value(sheet1, row,
                                                                        columns1["Seller SKU"]))

            # 写入公式到运费和汇率列，1个为2.99，在此基础上增加一个+0.5
            openpyxl_utils.set_cell_value(sheet2, target_row, columns2["运费"],
                                          f"=2.99+IF(E{target_row}=1,0,(E{target_row}-1)*0.5)")

            # 汇率
            openpyxl_utils.set_cell_value(sheet2, target_row, columns2["汇率"], exchange_rate)

            target_row += 1
    except Exception as e:
        raise Exception(f"写入数据到表2时发生错误: {e}")


def match_and_write_prices(sheet2, sheet4, columns2, sku_col_4, cost_col_4):
    """
    匹配表2和表4的款号，并提取成本价写入表2
    """
    try:
        for row_2 in range(2, sheet2.max_row + 1):  # 从表2的第2行开始
            sku_value_2 = openpyxl_utils.get_cell_value(sheet2, row_2, columns2["款号"])
            if sku_value_2:
                matched_cost = None
                for row_4 in range(2, sheet4.max_row + 1):  # 从表4的第2行开始
                    sku_value_4 = openpyxl_utils.get_cell_value(sheet4, row_4, sku_col_4)
                    if sku_value_4 == sku_value_2:  # 匹配款号
                        cost_value_4 = openpyxl_utils.get_cell_value(sheet4, row_4, cost_col_4)
                        # 提取括号中的数值
                        match = re.search(r"（([\d.]+)", cost_value_4)
                        if match:
                            matched_cost = float(match.group(1))
                        break
                # 将匹配到的成本价写入表2的采购价列
                openpyxl_utils.set_cell_value(sheet2, row_2, columns2["采购价"], matched_cost)
    except Exception as e:
        raise Exception(f"匹配和写入成本价时发生错误: {e}")


def calculate_rmb_prices(file_path):
    """
    计算采购价（RMB）并写入表格
    """
    try:
        xwMap = xw_map(file_path)
        app = xwMap["app"]
        wb = xwMap["workbook"]
        sheet = xwMap["sheet"]

        # 定义需要读取的列
        column_list = ["D", "E", "F", "G"]

        # 定义计算规则的回调函数
        def callback(column_result_dic):
            try:
                d_ = column_result_dic["D"]
                e_ = column_result_dic["E"]
                f_ = column_result_dic["F"]
                g_ = column_result_dic["G"]
                result = ((d_ * float(e_)) + f_) * g_
                return round(result, 2)
            except Exception as e:
                raise Exception(f"Error in callback function: {e}")

        # 调用计算函数
        calculate_formula(sheet, column_list, "H", callback)

        last_row = get_last_row_num(sheet, 'H')
        h_values = get_range_row_value(sheet, 'H', 2, last_row)
        h_total = utils.round2(sum(value for value in h_values if utils.isinstanceNums(value)))
        set_cell_value(sheet, "L", "1", f"总计:¥ {h_total} 元")

        beautify(sheet)
        xw_save(wb, app)

        return h_total
    except Exception as e:
        raise Exception(f"计算和写入采购价（RMB）时发生错误: {e}")


def main():
    try:
        source_file = input("请输入源表文件的绝对路径：")
        exchange_rate = utils.get_usd_to_cny_rate()

        # 加载文件
        wb1 = openpyxl_utils.load_excel_file(source_file)
        wb2 = openpyxl_utils.load_excel_file(utils.current_dir() + "/xlsx/fxb/CZFF供应商对账表模版.xlsx")
        wb4 = openpyxl_utils.load_excel_file(utils.current_dir() + "/xlsx/fxb/CZFF产品核对表.xlsx")

        # 获取活动表
        sheet1 = openpyxl_utils.get_active_sheet(wb1)
        sheet2 = openpyxl_utils.get_active_sheet(wb2)
        sheet4 = openpyxl_utils.get_active_sheet(wb4)

        # 查找列
        columns1 = openpyxl_utils.find_columns(sheet1, ["Paid Time", "Order ID", "Quantity", "Seller SKU"])
        columns2 = openpyxl_utils.find_columns(sheet2, ["日期", "订单单号", "数量", "运费", "款号", "汇率", "采购价"])

        # 写入数据
        write_data_to_sheet(sheet1, sheet2, columns1, columns2, exchange_rate)

        # 匹配款号和成本价
        match_and_write_prices(sheet2, sheet4, columns2, sku_col_4=8, cost_col_4=5)

        # 保存文件
        output_path = "/Users/zkp/Desktop/B&Y/CZFF供应商对账/CZFF供应商对账表_temp.xlsx"
        wb2.save(output_path)

        # 计算采购价（RMB）
        prices = calculate_rmb_prices(output_path)

        old_file_path = output_path
        new_file_dir = "/Users/zkp/Desktop/B&Y/CZFF供应商对账/"
        new_file_path = new_file_dir + "CZFF供应商对账表" + str(prices) + "元-" + utils.get_yd() + ".xlsx"
        utils.rename(old_file_path, new_file_path)
        print(f"文件已重命名为：{new_file_path}")
        utils.open_dir(new_file_dir)
    except Exception as e:
        print(f"程序运行时发生错误: {e}")


if __name__ == "__main__":
    main()
