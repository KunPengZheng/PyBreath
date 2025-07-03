from datetime import datetime
import pandas as pd
import shutil
import os
from collections import defaultdict

from xinshili import utils
from xinshili.fs_utils_plus import insert_col_row, FsConstants, get_token, ClientMapConstants, ClientConstants, \
    MapFields, fs_col_to_index, value_range
from xinshili.gjgz_plus333 import RowName


def update_sales_data(file1_path, output_path):
    # 读取文件1和复制后的文件2
    df1 = pd.read_excel(file1_path).fillna("")
    df2 = pd.read_excel(output_path, sheet_name=None)

    # 👉 获取下单时间第一条有效数据并格式化为 "7月2日"
    order_time_str = df1.get("下单时间", "").astype(str).str.strip().replace("nan", "").values
    order_time = next((t for t in order_time_str if t), None)
    formatted_date = ""
    if order_time:
        try:
            dt = datetime.strptime(order_time, "%Y-%m-%d %H:%M:%S")
            formatted_date = f"{dt.month}月{dt.day}日"
            print(f"📅 首个下单时间对应日期为：{formatted_date}")
        except Exception as e:
            print(f"⚠️ 日期格式错误：{e}")

    # 产品总数要能转为数字以便汇总
    if RowName.Total_Of_Product in df1.columns:
        df1[RowName.Total_Of_Product] = pd.to_numeric(df1[RowName.Total_Of_Product], errors="coerce").fillna(0)

    # --- 构建映射 ---
    store_count_map = df1[RowName.Store_Account].value_counts().to_dict()
    sku_sum_map = df1.groupby(RowName.SKU)[RowName.Total_Of_Product].sum().to_dict()

    updated_sheets = {}

    # --- 店铺销量表 ---
    if RowName.Store_Sales in df2:
        sheet = df2[RowName.Store_Sales].copy()
        if RowName.Store_Name in sheet.columns and RowName.Order_Sales in sheet.columns:
            sheet[RowName.Order_Sales] = sheet[RowName.Store_Name].apply(
                lambda x: store_count_map.get(str(x).strip(), 0))
        updated_sheets[RowName.Store_Sales] = sheet

    # --- 销量更新表 ---
    if RowName.Sales_Update in df2:
        sheet = df2[RowName.Sales_Update].copy()
        if RowName.SKU in sheet.columns and RowName.Quantity in sheet.columns:
            sheet[RowName.Quantity] = sheet[RowName.SKU].apply(lambda x: sku_sum_map.get(str(x).strip(), 0))
        updated_sheets[RowName.Sales_Update] = sheet

    # --- 库存更新表（直接复制） ---
    if RowName.Inventory_Update in df2:
        updated_sheets[RowName.Inventory_Update] = df2[RowName.Inventory_Update].copy()

    # 写入更新后的 sheet
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, df_sheet in updated_sheets.items():
            df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"✅ 已更新并保存到：{output_path}")
    return formatted_date


def merge_excels_in_folder(folder_path, output_path):
    utils.delete_file(output_path)

    all_files = [f for f in os.listdir(folder_path) if f.endswith((".xlsx", ".xls"))]
    combined_df = pd.DataFrame()
    header_saved = False  # 只保留第一个文件的列头

    for filename in all_files:
        file_path = os.path.join(folder_path, filename)
        try:
            # 始终使用 header=0 保证列头是从文件中第一行读的
            df = pd.read_excel(file_path, header=0)

            if not header_saved:
                combined_df = pd.concat([combined_df, df], ignore_index=True)
                header_saved = True
            else:
                combined_df = pd.concat([combined_df, df], ignore_index=True)  # 直接合并，无需 iloc[1:]

            print(f"✅ 已处理文件：{filename}")
        except Exception as e:
            print(f"❌ 处理文件 {filename} 出错：{e}")

    # 保存合并结果
    combined_df.to_excel(output_path, index=False)
    print(f"\n✅ 合并完成，保存路径：{output_path}")


def update_available_inventory(file1_path, file2_path, output_path):
    # 读取文件1
    df1 = pd.read_excel(file1_path)
    df1.fillna('', inplace=True)

    # 构建 SKU → 可用库存总和 map
    sku_inventory_map = defaultdict(float)
    for _, row in df1.iterrows():
        sku = row.get(RowName.SKU, "").strip()
        inv = row.get(RowName.Available_Inventory, "")
        try:
            inv_val = float(inv)
        except:
            inv_val = 0
        if sku:
            sku_inventory_map[sku] += inv_val

    # 读取文件2所有 Sheet
    df2_sheets = pd.read_excel(file2_path, sheet_name=None)

    # 修改库存更新 Sheet
    if RowName.Inventory_Update in df2_sheets:
        df_kc = df2_sheets[RowName.Inventory_Update].copy()
        df_kc.fillna('', inplace=True)
        if RowName.SKU in df_kc.columns and RowName.Available_Quantity in df_kc.columns:
            df_kc[RowName.Available_Quantity] = df_kc[RowName.SKU].apply(
                lambda x: sku_inventory_map.get(str(x).strip(), 0))
        df2_sheets[RowName.Inventory_Update] = df_kc
    else:
        print("⚠️ 文件2中未找到 sheet：库存更新，已跳过更新")

    # 写入所有 sheet（保留原有的）
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet_name, df_sheet in df2_sheets.items():
            df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"✅ 已更新“库存更新”并保存至：{output_path}")


def update_total_inventory(file1_path, file2_path, output_path):
    # 读取文件1，填充空值
    df1 = pd.read_excel(file1_path)
    df1.fillna('', inplace=True)

    # 将库存数值列转换为 float
    df1["Available Inventory/可用库存"] = pd.to_numeric(df1.get("Available Inventory/可用库存", 0),
                                                        errors="coerce").fillna(0)
    df1["In-transit inventory/在途库存"] = pd.to_numeric(df1.get("In-transit inventory/在途库存", 0),
                                                         errors="coerce").fillna(0)

    # 构建 SKU → 可用库存/在途库存 映射表
    available_map = defaultdict(float)
    transit_map = defaultdict(float)

    for _, row in df1.iterrows():
        sku = row.get("SKU", "").strip()
        if sku:
            available_map[sku] += row["Available Inventory/可用库存"]
            transit_map[sku] += row["In-transit inventory/在途库存"]

    # 读取文件2的所有 sheet
    df2_sheets = pd.read_excel(file2_path, sheet_name=None)

    # 处理“库存更新”sheet
    sheet_name_target = "库存更新"
    if sheet_name_target in df2_sheets:
        df_kc = df2_sheets[sheet_name_target].copy()
        df_kc.fillna('', inplace=True)

        if "SKU" in df_kc.columns:
            df_kc["库存(全部)"] = df_kc["SKU"].apply(lambda x: available_map.get(str(x).strip(), 0))
            df_kc["在途（全部）"] = df_kc["SKU"].apply(lambda x: transit_map.get(str(x).strip(), 0))
        else:
            print("⚠️ '库存更新' 表中缺少 SKU 列，未更新")

        # 更新 sheet 回 sheet dict
        df2_sheets[sheet_name_target] = df_kc
    else:
        print("⚠️ 文件2中未找到 sheet：库存更新，已跳过更新")

    # 写入所有 sheet 到 output_path
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet, df_sheet in df2_sheets.items():
            df_sheet.to_excel(writer, sheet_name=sheet, index=False)

    print(f"✅ 已更新“库存更新”并保存至：{output_path}")


def update_shipping_inventory(csv_file_path, xlsx_file_path, output_path):
    # 读取 CSV 文件（文件1）
    df1 = pd.read_csv(csv_file_path).fillna("")

    # 转换为数值，便于求和
    df1[RowName.Sea_transportation] = pd.to_numeric(df1.get(RowName.Sea_transportation, 0), errors="coerce").fillna(0)
    df1[RowName.Air_transportation] = pd.to_numeric(df1.get(RowName.Air_transportation, 0), errors="coerce").fillna(0)

    # 构建 SKU → 海/空 运在途数量 Map
    sea_map = defaultdict(float)
    air_map = defaultdict(float)

    for _, row in df1.iterrows():
        sku = row.get(RowName.SKU, "").strip()
        if sku:
            sea_map[sku] += row[RowName.Sea_transportation]
            air_map[sku] += row[RowName.Air_transportation]

    # 读取 Excel 所有工作表
    xls = pd.read_excel(xlsx_file_path, sheet_name=None)
    updated_sheets = {}

    for sheet_name, df_sheet in xls.items():
        df_sheet = df_sheet.fillna("")
        if sheet_name == RowName.Inventory_Update and RowName.SKU in df_sheet.columns:
            # 更新库存更新表的海运在途和空运在途
            df_sheet[RowName.Sea_transportation] = df_sheet[RowName.SKU].apply(lambda x: sea_map.get(str(x).strip(), 0))
            df_sheet[RowName.Air_transportation] = df_sheet[RowName.SKU].apply(lambda x: air_map.get(str(x).strip(), 0))
        updated_sheets[sheet_name] = df_sheet

    # 写入到新文件，保留所有 sheet
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, df_sheet in updated_sheets.items():
            df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"✅ 所有工作表已写入，库存更新已处理并保存至：{output_path}")


def get_range_column_data(file_path, sheet_name, column_name, start_row, end_row):
    """
    获取 Excel 指定 sheet 的某一列数据（包含列头），支持行区间选择。

    :param file_path: Excel 文件路径
    :param sheet_name: 工作表名称
    :param column_name: 要读取的列名
    :param start_row: 起始行号（从 0 开始，0 表示包含列头）
    :param end_row: 结束行号（包含，None 表示到末尾）
    :return: 列表形式返回数据
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=object).fillna("")

        if column_name not in df.columns:
            raise ValueError(f"❌ 指定列名 '{column_name}' 不存在于工作表 '{sheet_name}' 中。")

        # 列数据（包含列头）
        data_with_header = [column_name] + df[column_name].tolist()

        # 切片区间（包含列头），行号从 0 开始，包含 end_row
        start_idx = max(0, start_row - 1)
        end_idx = end_row + 1 if end_row is not None else None

        return data_with_header[start_idx:end_idx]

    except Exception as e:
        print(f"⚠️ 获取失败: {e}")
        return []


def get_range_column_row_data(file_path, sheet_name, start_row, end_row, start_col, end_col):
    """
    获取 Excel 指定 sheet 中指定行列区域的数据，返回二维数组形式。

    :param file_path: Excel 文件路径
    :param sheet_name: 表名（Sheet 名）
    :param start_row: 起始行号（从 0 开始，包含）
    :param end_row: 结束行号（从 0 开始，包含）
    :param start_col: 起始列号（从 0 开始，包含）
    :param end_col: 结束列号（从 0 开始，包含）
    :return: 二维数组（嵌套列表）
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    df.fillna('', inplace=True)

    # 将 Excel 行号（从 1 开始）转换为 Pandas 行索引（从 0 开始）
    pandas_start_row = start_row - 1
    pandas_end_row = end_row - 1

    # 将列名（如 "C"）转换为列索引（从 0 开始）
    start_col_num = fs_col_to_index(start_col) - 1
    end_col_num = fs_col_to_index(end_col) - 1

    region = df.iloc[pandas_start_row:pandas_end_row + 1, start_col_num:end_col_num + 1]
    return region.values.tolist()


def xyl_fs(formatted_date, template_copy_path):
    # token = get_token()
    # startIndex = fs_col_to_index("K")
    # endIndex = fs_col_to_index("L")

    # insert_col_row(token, FsConstants.xyl_sales_repertory_token,
    #                ClientMapConstants[ClientConstants.xyl_sales_repertory][MapFields.xyl_sku_zjhz],
    #                startIndex, endIndex, FsConstants.COLUMNS, FsConstants.AFTER)
    # insert_col_row(token, FsConstants.xyl_sales_repertory_token,
    #                ClientMapConstants[ClientConstants.xyl_sales_repertory][MapFields.xyl_sku_ejyxhz],
    #                startIndex, endIndex, FsConstants.COLUMNS, FsConstants.AFTER)
    # insert_col_row(token, FsConstants.xyl_sales_repertory_token,
    #                ClientMapConstants[ClientConstants.xyl_sales_repertory][MapFields.xyl_store],
    #                fs_col_to_index("D"), fs_col_to_index("E"), FsConstants.COLUMNS, FsConstants.AFTER)

    xyl_sku_zjhz_arr = get_range_column_data(template_copy_path, RowName.Sales_Update, RowName.Quantity, 2, 124)
    xyl_sku_zjhz_arr.insert(0, formatted_date)
    print(f"1111:{len(xyl_sku_zjhz_arr)}")
    xyl_sku_zjhz_arr.append({"type": "formula", "text": f"=SUM(L2:L124"})

    xyl_sku_ejyxhz_arr = get_range_column_data(template_copy_path, RowName.Sales_Update, RowName.Quantity, 126, 234)
    xyl_sku_ejyxhz_arr.insert(0, formatted_date)
    print(f"2222:{len(xyl_sku_ejyxhz_arr)}")
    xyl_sku_ejyxhz_arr.append({"type": "formula", "text": f"=SUM(L2:L110"})

    xyl_store_arr = get_range_column_data(template_copy_path, RowName.Store_Sales, RowName.Order_Sales, 2, 45)
    xyl_store_arr.insert(0, formatted_date)
    print(f"3333:{len(xyl_store_arr)}")
    xyl_store_arr.append({"type": "formula", "text": f"=SUM(E2:E48"})

    print(xyl_sku_zjhz_arr)
    print(xyl_sku_ejyxhz_arr)
    print(xyl_store_arr)

    # value_range(token, FsConstants.xyl_sales_repertory_token,
    #             ClientMapConstants[ClientConstants.xyl_sales_repertory][MapFields.xyl_sku_zjhz],
    #             f"L1:L{len(xyl_sku_zjhz_arr)}", xyl_sku_zjhz_arr)
    # value_range(token, FsConstants.xyl_sales_repertory_token,
    #             ClientMapConstants[ClientConstants.xyl_sales_repertory][MapFields.xyl_sku_ejyxhz],
    #             f"L1:L{len(xyl_sku_ejyxhz_arr)}", xyl_sku_ejyxhz_arr)
    # value_range(token, FsConstants.xyl_sales_repertory_token,
    #             ClientMapConstants[ClientConstants.xyl_sales_repertory][MapFields.xyl_store],
    #             f"E1:E{len(xyl_store_arr)}", xyl_store_arr)

    xyl_sku_inventory_zjhz_arr = get_range_column_row_data(template_copy_path, RowName.Inventory_Update, 2, 124, "C",
                                                           "E")
    xyl_sku_inventory_ejyxhz_arr = get_range_column_row_data(template_copy_path, RowName.Inventory_Update, 126, 234,
                                                             "C", "E")
    print(xyl_sku_inventory_zjhz_arr)
    print(xyl_sku_inventory_ejyxhz_arr)


def call(analyse_obj):
    root_path = "/Users/zkp/Desktop/B&Y/dxm/sku_store_statistics"
    analyse_dir_path = f"{root_path}/{analyse_obj}"
    dxm_order_path = f"{analyse_dir_path}/dxm_order.xlsx"
    template_path = f"{root_path}/{analyse_obj}运营统计.xlsx"
    template_copy_path = f"{analyse_dir_path}/{analyse_obj}运营统计_copy.xlsx"
    oms_store_dir = f"{analyse_dir_path}/oms_store"
    oms_store_merger_path = f"{oms_store_dir}/oms_store_merger.xlsx"
    dszs_inventory_path = f"{analyse_dir_path}/dszs_inventory.csv"

    # 创建输出文件路径（复制一份文件2）
    template_copy_path = os.path.join(template_path, template_copy_path)
    shutil.copy(template_path, template_copy_path)

    # 更新店铺和sku的销量
    formatted_date = update_sales_data(dxm_order_path, template_copy_path)

    # 合并oms库存文件
    merge_excels_in_folder(oms_store_dir, oms_store_merger_path)

    if analyse_obj == "xyl":
        # 更新库存
        update_available_inventory(oms_store_merger_path, template_copy_path, template_copy_path)
        # 更新海运空运
        update_shipping_inventory(dszs_inventory_path, template_copy_path, template_copy_path)
        # 数据写入飞书表格
        xyl_fs(formatted_date, template_copy_path)
    elif analyse_obj == "sanrio":
        update_total_inventory(oms_store_merger_path, template_copy_path, template_copy_path)


if __name__ == '__main__':
    call("xyl")
    # call("sanrio")
