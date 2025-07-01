import pandas as pd
import shutil
import os
from collections import defaultdict


def update_sales_data(file1_path, output_path):
    # 读取文件1和复制后的文件2
    df1 = pd.read_excel(file1_path, dtype=str).fillna("")
    df2 = pd.read_excel(output_path, sheet_name=None, dtype=str)

    # 产品总数要能转为数字以便汇总
    if "产品总数" in df1.columns:
        df1["产品总数"] = pd.to_numeric(df1["产品总数"], errors="coerce").fillna(0)

    # --- 构建映射 ---
    store_count_map = df1["店铺账号"].value_counts().to_dict()
    sku_sum_map = df1.groupby("SKU")["产品总数"].sum().to_dict()

    updated_sheets = {}

    # --- 店铺销量表 ---
    if "店铺销量" in df2:
        sheet = df2["店铺销量"].copy()
        if "店铺名称" in sheet.columns and "订单数量" in sheet.columns:
            sheet["订单数量"] = sheet["店铺名称"].apply(lambda x: store_count_map.get(str(x).strip(), 0))
        updated_sheets["店铺销量"] = sheet

    # --- 销量更新表 ---
    if "销量更新" in df2:
        sheet = df2["销量更新"].copy()
        if "SKU" in sheet.columns and "数量" in sheet.columns:
            sheet["数量"] = sheet["SKU"].apply(lambda x: sku_sum_map.get(str(x).strip(), 0))
        updated_sheets["销量更新"] = sheet

    # --- 库存更新表（直接复制） ---
    if "库存更新" in df2:
        updated_sheets["库存更新"] = df2["库存更新"].copy()

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
        sku = row.get("SKU", "").strip()
        inv = row.get("Available Inventory/可用库存", "").strip()
        try:
            inv_val = float(inv)
        except:
            inv_val = 0
        if sku:
            sku_inventory_map[sku] += inv_val

    # 读取文件2所有 Sheet
    df2_sheets = pd.read_excel(file2_path, sheet_name=None, dtype=str)

    # 修改库存更新 Sheet
    if "库存更新" in df2_sheets:
        df_kc = df2_sheets["库存更新"].copy()
        df_kc.fillna('', inplace=True)
        if "SKU" in df_kc.columns and "可用量" in df_kc.columns:
            df_kc["可用量"] = df_kc["SKU"].apply(lambda x: sku_inventory_map.get(str(x).strip(), 0))
        df2_sheets["库存更新"] = df_kc
    else:
        print("⚠️ 文件2中未找到 sheet：库存更新，已跳过更新")

    # 写入所有 sheet（保留原有的）
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet_name, df_sheet in df2_sheets.items():
            df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"✅ 已更新“库存更新”并保存至：{output_path}")


if __name__ == '__main__':
    data_path = "/Users/zkp/Desktop/B&Y/dxm/sku_store_statistics/order_120250630095056152_1573179.xlsx"
    dir_path = "/Users/zkp/Desktop/B&Y/dxm/sku_store_statistics"
    template_path = f"{dir_path}/xyl运营统计.xlsx"
    template_copy_path = f"{dir_path}/xyl运营统计_copy.xlsx"

    # 创建输出文件路径（复制一份文件2）
    template_copy_path = os.path.join(template_path, template_copy_path)
    shutil.copy(template_path, template_copy_path)

    # 更新店铺和sku的销量
    update_sales_data(data_path, template_copy_path)

    oms_store_dir = "/Users/zkp/Desktop/B&Y/dxm/sku_store_statistics/oms_store"
    oms_store_merger_path = f"{oms_store_dir}/oms_store_merger.xlsx"
    merge_excels_in_folder(oms_store_dir, oms_store_merger_path)

    update_available_inventory(oms_store_merger_path, template_copy_path, template_copy_path)
