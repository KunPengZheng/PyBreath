import re

from xinshili.yd_gjgz import get_specified_node_info, extract_first_date_time_node, extract_first_datetime_site, \
    extract_info, split_excel_by_date_and_unique_count

arr = ['Delivered', 'Out for Delivery', 'Preparing for Delivery',
       'Moving Through Network\n\nIn Transit to Next Facility, Arriving On Time\n\nAugust 20, 2025',
       'Departed USPS Regional Facility\n\nOPA LOCKA FL DISTRIBUTION CENTER \n\nAugust 19, 2025, 5:32 am',
       '\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\tArrived at USPS Regional Origin Facility\n\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\tOPA LOCKA FL DISTRIBUTION CENTER \n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tAugust 19, 2025,\n\t\t\t\t\t\t\t\t\t4:14 am\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t', ]

arr = ['Alert', 'Contact Customer Care at 1-800-275-8777',
       'Processing Exception, Other Delay\n\nAugust 14, 2025, 12:00 pm',
       '\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\tOut for Delivery\n\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\tBLUEFIELD, WV 24701 \n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tAugust 13, 2025,\n\t\t\t\t\t\t\t\t\t6:10 am\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t', ]

arr = ['Delivery Attempt: Action Needed',
       'Reminder to Schedule Redelivery of your item before August 25, 2025\n\nAugust 16, 2025',
       'Available for Pickup\n\nWHITMAN\n1125 WHITMAN CREEK RD\nWHITMAN WV 25652-9998\nM-F 0800-1200; SAT 0900-1100\n\nAugust 11, 2025, 8:36 am',
       '\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\tArrived at Post Office\n\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\tWHITMAN, WV 25652 \n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tAugust 11, 2025,\n\t\t\t\t\t\t\t\t\t8:29 am\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t', ]

arr = ['Delivered\n\nDelivered, Individual Picked Up at Post Office\n\nLAKESIDE, CA 92040 \n\nAugust 25, 2025, 9:28 am',
       '\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\tOut for Delivery\n\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\tLAKESIDE, CA 92040 \n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tAugust 25, 2025,\n\t\t\t\t\t\t\t\t\t7:44 am\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t',
       '\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\tArrived at Post Office\n\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\tLAKESIDE, CA 92040 \n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tAugust 25, 2025,\n\t\t\t\t\t\t\t\t\t7:33 am\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t', ]

# objss = get_specified_node_info(arr)

# possession_first_event = objss["possession_first_event"]
# possession_second_event = objss["possession_second_event"]
# possession_last_event = objss["possession_last_event"]
# possession_newest_time_event = objss["possession_newest_time_event"]
#
# newest_dates, newest_times = extract_first_date_time_node(possession_newest_time_event)
# newest_site = extract_first_datetime_site(possession_newest_time_event)
#
# print(f"possession_first_event:\n {possession_first_event}")
# print(f"possession_second_event:\n {possession_second_event}")
# print(f"possession_last_event:\n {possession_last_event}")
# print(f"possession_newest_time_event:\n {possession_newest_time_event}")
# print(f"newest_dates:\n {newest_dates}")
# print(f"newest_times:\n {newest_times}")
# print(f"newest_site:\n {newest_site}")
#
# result_map = {}
# excel_result_map = {}
# result_map["sss"] = {
#                                         "PossessionFirstEvent": possession_first_event,
#                                         "PossessionSecondEvent": possession_second_event,
#                                         "PossessionLastEvent": possession_last_event,
#                                         "PossessionNewestTimeEvent": possession_newest_time_event}
#
# extract_info(result_map,excel_result_map)

# split_excel_by_date_and_unique_count(
#     "/Users/zkp/Desktop/B&Y/轨迹统计/dxm_xyl_track/order_120250829111401423_1573179.xlsx",
#     "发货时间", "订单号",
#     "订单号", "发货时间",
#     "/Users/zkp/Desktop/B&Y/轨迹统计/dxm_xyl_track")
