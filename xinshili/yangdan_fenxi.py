import pandas as pd

from xinshili.gjgz_plus333 import extract_and_process_data, CourierStateMapKey, RowName, update_courier_status


def compare_tracking_numbers(file1_path, file2_path, output_path):
    # 读取 Excel 文件
    df1 = pd.read_excel(file1_path, dtype=str)
    df2 = pd.read_excel(file2_path, dtype=str)

    # 定义关键列名
    order_col_1 = "订单号"
    tracking_col_1 = "运单号"
    order_col_2 = "Platform Number/平台单号"
    tracking_col_2 = "Package 1\nTracking No./物流跟踪号1"

    # 清理空格
    df1[order_col_1] = df1[order_col_1].str.strip()
    df1[tracking_col_1] = df1[tracking_col_1].str.strip()
    df2[order_col_2] = df2[order_col_2].str.strip()
    df2[tracking_col_2] = df2[tracking_col_2].str.strip()

    # 过滤掉任意关键列为空的行
    df1_clean = df1.dropna(subset=[order_col_1, tracking_col_1])
    df2_clean = df2.dropna(subset=[order_col_2, tracking_col_2])
    df1_clean = df1_clean[(df1_clean[order_col_1] != "") & (df1_clean[tracking_col_1] != "")]
    df2_clean = df2_clean[(df2_clean[order_col_2] != "") & (df2_clean[tracking_col_2] != "")]

    # 合并两个 DataFrame：根据订单号匹配
    merged = pd.merge(
        df1_clean[[order_col_1, tracking_col_1]],
        df2_clean[[order_col_2, tracking_col_2]],
        left_on=order_col_1,
        right_on=order_col_2,
        how='inner'
    )

    # 找出运单号不一致的记录
    mismatched = merged[merged[tracking_col_1] != merged[tracking_col_2]]

    # 整理输出列
    result = mismatched[[order_col_1, tracking_col_1, tracking_col_2]]
    result.columns = ['订单号', '文件1_运单号', '文件2_运单号']

    # 导出结果
    result.to_excel(output_path, index=False)
    print(f"✅ 差异记录已保存到: {output_path}")


def check_and_add_courier_column(file_path):
    """
    检查 Excel 文件是否存在 '快递' 列，如果没有，则在最后一列添加该列。

    :param file_path: Excel 文件路径
    :param courier_column: 快递列名，默认为 'Courier/快递'
    :return: None
    """
    try:
        # 加载 Excel 文件
        data = pd.read_excel(file_path, engine='openpyxl')
        # 判断是否存在 '快递' 列
        if '文件1_快递状态' not in data.columns:
            # 如果没有 '快递' 列，则在最后一列添加该列
            data['文件1_快递状态'] = ""  # 默认为空值，可以根据需求填充其他默认值
        if '文件2_快递状态' not in data.columns:
            data['文件2_快递状态'] = ""
        if '文件1_签收时间' not in data.columns:
            data['文件1_签收时间'] = ""
        if '文件2_签收时间' not in data.columns:
            data['文件2_签收时间'] = ""
        if '签收时间_间隔' not in data.columns:
            data['签收时间_间隔'] = ""
        # 保存修改后的文件
        data.to_excel(file_path, index=False, engine='openpyxl')
        # print("check_and_add_courier_column 方法执行完成")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == '__main__':
    file1 = "/Users/zkp/Documents/未命名文件夹 2/930单12-20号_副本.xlsx"
    file2 = "/Users/zkp/Documents/未命名文件夹 2/ParcelOutbound_20250520160403_副本.xlsx"
    output = "/Users/zkp/Documents/未命名文件夹 2/差异输出.xlsx"

    compare_tracking_numbers(file1, file2, output)
    check_and_add_courier_column(output)

    results1 = extract_and_process_data(output, '文件1_快递状态', 100, "文件1_运单号")
    all_maps1 = {
        CourierStateMapKey.not_yet_map: results1[CourierStateMapKey.not_yet_map],
        CourierStateMapKey.pre_ship_map: results1[CourierStateMapKey.pre_ship_map],
        CourierStateMapKey.unpaid_map: results1[CourierStateMapKey.unpaid_map],
        CourierStateMapKey.delivered_map: results1[CourierStateMapKey.delivered_map],
        CourierStateMapKey.no_tracking_map: results1[CourierStateMapKey.no_tracking_map],
        CourierStateMapKey.tracking_map: results1[CourierStateMapKey.tracking_map],
        CourierStateMapKey.delivered_time_map: results1[CourierStateMapKey.delivered_time_map],
    }
    column_mapping1 = {
        CourierStateMapKey.not_yet_map: '文件1_快递状态',
        CourierStateMapKey.pre_ship_map: '文件1_快递状态',
        CourierStateMapKey.unpaid_map: '文件1_快递状态',
        CourierStateMapKey.delivered_map: '文件1_快递状态',
        CourierStateMapKey.no_tracking_map: '文件1_快递状态',
        CourierStateMapKey.tracking_map: '文件1_快递状态',
        CourierStateMapKey.delivered_time_map: '文件1_签收时间',
    }
    update_courier_status(output, all_maps1, wl="文件1_运单号", column_map=column_mapping1)

    results2 = extract_and_process_data(output, '文件2_快递状态', 100, "文件2_运单号")
    all_maps2 = {
        CourierStateMapKey.not_yet_map: results2[CourierStateMapKey.not_yet_map],
        CourierStateMapKey.pre_ship_map: results2[CourierStateMapKey.pre_ship_map],
        CourierStateMapKey.unpaid_map: results2[CourierStateMapKey.unpaid_map],
        CourierStateMapKey.delivered_map: results2[CourierStateMapKey.delivered_map],
        CourierStateMapKey.no_tracking_map: results2[CourierStateMapKey.no_tracking_map],
        CourierStateMapKey.tracking_map: results2[CourierStateMapKey.tracking_map],
        CourierStateMapKey.delivered_time_map: results2[CourierStateMapKey.delivered_time_map],
    }
    column_mapping2 = {
        CourierStateMapKey.not_yet_map: '文件2_快递状态',
        CourierStateMapKey.pre_ship_map: '文件2_快递状态',
        CourierStateMapKey.unpaid_map: '文件2_快递状态',
        CourierStateMapKey.delivered_map: '文件2_快递状态',
        CourierStateMapKey.no_tracking_map: '文件2_快递状态',
        CourierStateMapKey.tracking_map: '文件2_快递状态',
        CourierStateMapKey.delivered_time_map: '文件2_签收时间',
    }
    update_courier_status(output, all_maps2, wl="文件2_运单号", column_map=column_mapping2)




