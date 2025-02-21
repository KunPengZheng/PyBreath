from xinshili.openpyxl_utils import mark_by_row_content
from xinshili.pd_utils import merge_xlsx_files, remove_duplicates_by_column
from xinshili.gjgz_plus111 import extract_and_process_data, RowName, check_and_add_courier_column, \
    update_courier_status, CourierStateMapKey, find_irregular_tracking_numbers

output_path1 = '/Users/zkp/Downloads/1月份15026（zbw,sanrio,xyl）.xlsx'
output_path2 = '/Users/zkp/Downloads/1月份15026（zbw,sanrio,xyl）_qc.xlsx'
remove_duplicates_by_column(output_path1, output_path2, "Tracking No./物流跟踪号")
check_and_add_courier_column(output_path2)

irregular_number_map = find_irregular_tracking_numbers(output_path2)
irregular_number_list = []
if (len(irregular_number_map) > 0):
    irregular_number_list = list(irregular_number_map.keys())
    print(f"存在无效的物流跟踪号：{irregular_number_list}")
    update_courier_status(output_path2, irregular_number_map)

results = extract_and_process_data(output_path2, RowName.Courier, 100)
update_courier_status(output_path2, results[CourierStateMapKey.not_yet_map])
update_courier_status(output_path2, results[CourierStateMapKey.pre_ship_map])
update_courier_status(output_path2, results[CourierStateMapKey.unpaid_map])
update_courier_status(output_path2, results[CourierStateMapKey.delivered_map])
update_courier_status(output_path2, results[CourierStateMapKey.no_tracking_map])
update_courier_status(output_path2, results[CourierStateMapKey.tracking_map])

mark_by_row_content(output_path2, RowName.Courier, "Tracking No./物流跟踪号",
                    ['not_yet', 'pre_ship', 'no_tracking', 'irregular_no_tracking'])
