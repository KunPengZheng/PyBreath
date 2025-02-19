from xinshili.openpyxl_utils import merge_xlsx_files
import pandas as pd

from xinshili.pd_utils import remove_duplicates_by_column

import pandas as pd

import pandas as pd


def delete_matching_rows(input_file: str, output_file: str, keywords: list = ["运费和差价专用", "刷数据", "专拍"]):
    # 读取 Excel 文件
    df = pd.read_excel(input_file, engine='openpyxl')
    # 构建一个包含所有关键字的过滤条件
    condition = df['标题'].str.contains('|'.join(keywords), na=False)
    # 删除标题列匹配到的行
    df = df[~condition]  # ~condition 表示保留不匹配的行
    # 将删除后的数据保存为新的 Excel 文件
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"删除匹配行后的数据已保存为: {output_file}")


def filter_pei_jian(input_file: str, output_file: str,
                    keywords: list = ["配件", "插座", "电池管理系统BMS", "电池管理系统bms",
                                      "采集板从控模块", "采集板", "低压线束", "电池底壳", "外壳",
                                      "上盖", "高压互锁插座", "烟感器", "低压接触器",
                                      "预充电阻", "低压通讯", "电流传感器", "继电器", "保险丝", "熔断器", "分流器",
                                      "接插件","维修开关", "烟雾传感器", "高压总成BDU", "高压插座", "低压通讯接口"]):
    # 读取 Excel 文件
    df = pd.read_excel(input_file, engine='openpyxl')

    # 构建一个包含所有关键字的过滤条件
    condition = df['标题'].str.contains('|'.join(keywords), na=False) | df['描述'].str.contains('|'.join(keywords),
                                                                                                na=False)
    # 过滤出包含关键字的行
    filtered_df = df[condition]

    # 将过滤后的数据保存为新的 Excel 文件
    filtered_df.to_excel(output_file, index=False, engine='openpyxl')

    print(f"过滤后的数据已保存为: {output_file}")


def merge():
    # 合并纬度相同的多份文件为一个文件
    merge_xlsx_files([
        "/Users/zkp/Downloads/咸鱼/数据表格19_02_30.xlsx",
        "/Users/zkp/Downloads/咸鱼/数据表格19_03_16.xlsx",
        "/Users/zkp/Downloads/咸鱼/数据表格19_03_42.xlsx",
        "/Users/zkp/Downloads/咸鱼/数据表格19_04_03.xlsx",
        "/Users/zkp/Downloads/咸鱼/数据表格19_04_17.xlsx",
    ], "/Users/zkp/Downloads/咸鱼/merge_out.xlsx")


def compare_and_save_xlsx(file1: str, file2: str, output_file: str, column_name: str = "标题"):
    # 读取两份 Excel 文件
    df1 = pd.read_excel(file1, engine='openpyxl')
    df2 = pd.read_excel(file2, engine='openpyxl')

    # 确保两份文件中都有标题列
    if column_name not in df1.columns or column_name not in df2.columns:
        print(f"错误：找不到列名 '{column_name}' 在其中一个文件中！")
        return

    # 比较标题列的内容，筛选出内容不相等的数据
    # 使用 `isin()` 来判断是否存在相同的标题
    unmatched_df1 = df1[~df1[column_name].isin(df2[column_name])]  # df1 中不在 df2 的标题
    unmatched_df2 = df2[~df2[column_name].isin(df1[column_name])]  # df2 中不在 df1 的标题

    # 合并两份不相等的数据
    result_df = pd.concat([unmatched_df1, unmatched_df2], ignore_index=True)

    # 将结果保存为新的 Excel 文件
    result_df.to_excel(output_file, index=False, engine='openpyxl')

    print(f"不相等的数据已保存为: {output_file}")


def mathc_battery_brand(file_path):
    df = pd.read_excel(file_path)

    # 判断是否存在“电池品牌”列，如果没有则创建
    if '电池品牌' not in df.columns:
        df['电池品牌'] = ''  # 创建一个空的“电池品牌”列

    # 定义多个品牌的匹配关键词
    brand_keywords = {
        '比亚迪': ['比亚迪', 'BYD', 'byd'],
        '宁德时代': ['宁德时代', '宁德', 'CATL', 'Contemporary Amperex Technology Co.', '宁德时代新能源'],
        '鹏辉能源': ['鹏辉能源', 'PEVE', '鹏辉'],
        '国轩高科': ['国轩高科', 'Gotion High-tech', '国轩', 'Gotion'],
        '天能电池': ['天能电池', 'Tianneng', '天能'],
        '亿纬锂能': ['亿纬锂能', 'EVE Energy', '亿纬'],
        '欣旺达': ['欣旺达', 'Sunwoda', '欣旺'],
        '中航锂电': ['中航锂电', 'CALB', '中航'],
        '沃特玛': ['沃特玛', 'VARTA', '沃特'],
        '长电科技': ['长电科技', 'JCET', '长电'],
        '松下': ['松下', 'Panasonic'],
        'LG化学': ['LG化学', 'LG Chem', 'LG', '化学'],
        '三星SDI': ['三星SDI', 'Samsung SDI', '三星', 'SDI'],
        '比克电池': ['比克电池', 'BAK', '比克'],
        '力神电池': ['力神电池', 'Lishen', '力神'],
        '南孚电池': ['南孚电池', 'Nanfu', '南孚'],
        '蜂巢能源': ['蜂巢能源', 'Honeycomb Energy', '蜂巢'],
        '天合光能': ['天合光能', 'Trina Solar', '天合'],
        '华为': ['华为', 'Huawei', '华为电池'],
        '乐鑫电池': ['乐鑫电池', 'Lexin Battery', '乐鑫'],
        '赣锋锂业': ['赣锋锂业', 'Ganfeng Lithium', '赣锋'],
        '捷威动力': ['捷威动力', 'Jay Power', '捷威'],
        '澳洲天合': ['澳洲天合', 'Australian Trina'],
        '赛米控股': ['赛米控股', 'SAMIC'],
        '达博科技': ['达博科技', 'DABO', '达博'],
        '亿嘉科技': ['亿嘉科技', 'Yijia Technology'],
        '骆驼集团': ['骆驼集团', 'Camel Group'],
        '金风科技': ['金风科技', 'Goldwind'],
        '时代新能源': ['时代新能源', 'Time New Energy'],
        '瑞浦电池': ['瑞浦电池', 'Repu Battery'],
        '中科电力': ['中科电力', 'Zhongke Power'],
        '大亚电池': ['大亚电池', 'Daya Battery'],
        '金康新能源': ['金康新能源', 'Jinkang New Energy'],
        '雄滔': ['雄滔电池', 'XiongTao Battery', '雄滔', 'vision', 'Vision', 'VISION'],
        '楚能': ['楚能新能源', '楚能', 'CORNEX', 'cornex', 'Cornex'],
        '瑞浦兰钧': ['瑞浦', '兰钧', 'REPT', 'rept', 'Rept'],
        '纳新': ['纳新'],
        'ATL': ['Amperex Technology Limited', '新能源科技有限公司', 'ATL', 'atl'],
        '航天': ['航天锂电科技（江苏）有限公司', '航天'],
        '波士顿': ['波士顿'],
        '塔菲尔': ['塔菲尔'],
        '海盈': ['海盈'],
        '海辰': ['海辰'],
        '中聚': ['中聚'],
        '海基': ['海基'],
        '多氟多': ['多氟多'],
        '光宇': ['光宇'],
        '金砖': ['金砖'],
        '启辰': ['启辰'],
        '江铃': ['江铃'],
        '天鑫': ['天鑫'],
        '小米': ['小米'],
        '长安': ['长安'],
        '桑顿': ['桑顿'],
        '东芝': ['东芝'],
        '兰均': ['兰均'],
        '星恒': ['星恒'],
        '利信': ['利信'],
        '北汽': ['北汽'],
        '哪吒': ['哪吒'],
        '瑞普': ['瑞普'],
        '海四达': ['海四达'],
        '上汽大通': ['上汽大通'],
        '益佳通': ['益佳通'],
        '万向': ['万向'],
        '远东': ['远东'],
        '孚能': ['孚能'],
    }

    # 根据关键词匹配填充“电池品牌”列
    for brand, keywords in brand_keywords.items():
        for keyword in keywords:
            # 使用str.contains来匹配关键词，并在“电池品牌”列中填入对应品牌名称
            df.loc[df['描述'].str.contains(keyword, case=False, na=False), '电池品牌'] = brand

    # 保存修改后的文件
    df.to_excel(file_path, index=False)  # 保存到新的Excel文件


if __name__ == '__main__':
    # # 合并
    # merge()
    # # 去重
    # remove_duplicates_by_column("/Users/zkp/Downloads/咸鱼/merge_out.xlsx",
    #                             "/Users/zkp/Downloads/咸鱼/merge_out_filter.xlsx", "标题")

    delete_matching_rows("/Users/zkp/Downloads/咸鱼/merge_out_filter_副本.xlsx",
                         "/Users/zkp/Downloads/咸鱼/merge_out_filter_副本.xlsx")

    # 过滤出"配件"的数据
    filter_pei_jian("/Users/zkp/Downloads/咸鱼/merge_out_filter_副本.xlsx", "/Users/zkp/Downloads/咸鱼/pj.xlsx")

    # 过滤出"非配件"的数据
    compare_and_save_xlsx("/Users/zkp/Downloads/咸鱼/merge_out_filter_副本.xlsx", "/Users/zkp/Downloads/咸鱼/pj.xlsx",
                          "/Users/zkp/Downloads/咸鱼/dc.xlsx")

    # 获取电池品牌
    mathc_battery_brand("/Users/zkp/Downloads/咸鱼/dc.xlsx")
