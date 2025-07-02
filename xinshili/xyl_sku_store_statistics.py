from dataclasses import dataclass

import pandas as pd
import shutil
import os
from collections import defaultdict

from xinshili.gjgz_plus333 import RowName


def update_sales_data(file1_path, output_path):
    # 读取文件1和复制后的文件2
    df1 = pd.read_excel(file1_path, dtype=str).fillna("")
    df2 = pd.read_excel(output_path, sheet_name=None, dtype=str)

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


def merge_excels_in_folder(folder_path, output_path):
    all_files = [f for f in os.listdir(folder_path) if f.endswith((".xlsx", ".xls"))]
    combined_df = pd.DataFrame()
    header_saved = False  # 只保留第一个文件的列头

    for filename in all_files:
        file_path = os.path.join(folder_path, filename)
        try:
            df = pd.read_excel(file_path, dtype=str)

            if not header_saved:
                combined_df = pd.concat([combined_df, df], ignore_index=True)
                header_saved = True
            else:
                combined_df = pd.concat([combined_df, df.iloc[1:]], ignore_index=True)  # 跳过列头行

            print(f"✅ 已处理文件：{filename}")
        except Exception as e:
            print(f"❌ 处理文件 {filename} 出错：{e}")

    # 保存合并结果
    combined_df.to_excel(output_path, index=False)
    print(f"\n✅ 合并完成，保存路径：{output_path}")


def update_available_inventory(file1_path, file2_path, output_path):
    # 读取文件1
    df1 = pd.read_excel(file1_path, dtype=str)
    df1.fillna('', inplace=True)

    # 构建 SKU → 可用库存总和 map
    sku_inventory_map = defaultdict(float)
    for _, row in df1.iterrows():
        sku = row.get(RowName.SKU, "").strip()
        inv = row.get(RowName.Available_Inventory, "").strip()
        try:
            inv_val = float(inv)
        except:
            inv_val = 0
        if sku:
            sku_inventory_map[sku] += inv_val

    # 读取文件2所有 Sheet
    df2_sheets = pd.read_excel(file2_path, sheet_name=None, dtype=str)

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


def update_shipping_inventory(csv_file_path, xlsx_file_path, output_path):
    # 读取 CSV 文件（文件1）
    df1 = pd.read_csv(csv_file_path, dtype=str).fillna("")

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
    xls = pd.read_excel(xlsx_file_path, sheet_name=None, dtype=str)
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


if __name__ == '__main__':
    dir_path = "/Users/zkp/Desktop/B&Y/dxm/sku_store_statistics/xyl"
    dxm_order_path = f"{dir_path}/order_120250630095056152_1573179.xlsx"
    template_path = f"{dir_path}/xyl运营统计.xlsx"
    template_copy_path = f"{dir_path}/xyl运营统计_copy.xlsx"
    oms_store_dir = f"{dir_path}/oms_store"
    oms_store_merger_path = f"{oms_store_dir}/oms_store_merger.xlsx"
    dszs_shipping_freight = f"{dir_path}/table_1 (1).csv"

    # 创建输出文件路径（复制一份文件2）
    template_copy_path = os.path.join(template_path, template_copy_path)
    shutil.copy(template_path, template_copy_path)

    # 更新店铺和sku的销量
    update_sales_data(dxm_order_path, template_copy_path)

    # 合并oms库存文件
    merge_excels_in_folder(oms_store_dir, oms_store_merger_path)

    # 更新库存
    update_available_inventory(oms_store_merger_path, template_copy_path, template_copy_path)
    # 更新海运空运
    update_shipping_inventory(dszs_shipping_freight, template_copy_path, template_copy_path)
