from xinshili.fs_utils_plus import get_token, insert_col_row, FsConstants, ClientMapConstants, ClientConstants, \
    MapFields, get_data
import pandas as pd


def count_store_accounts(file_path, column_name="店铺账号"):
    # 读取 Excel 文件
    df = pd.read_excel(file_path)

    # 确保该列存在
    if column_name not in df.columns:
        raise ValueError(f"未找到列: {column_name}")

    # 统计相同内容的数量
    count_series = df[column_name].value_counts()

    # 转为字典形式
    result = count_series.to_dict()

    return result


def count_store_accounts(file_path, column_name="店铺账号"):
    # 读取 Excel 文件
    df = pd.read_excel(file_path)

    # 确保该列存在
    if column_name not in df.columns:
        raise ValueError(f"未找到列: {column_name}")

    # 统计相同内容的数量
    count_series = df[column_name].value_counts()

    # 转为字典形式
    result = count_series.to_dict()

    return result


if __name__ == '__main__':
    # token = get_token()
    # insert_col_row(token, FsConstants.xyl_sales_repertory_token,
    #                ClientMapConstants[ClientConstants.xyl_sales_repertory][MapFields.xyl_sku], 5, 6)
    # get_data(token, FsConstants.xyl_sales_repertory_token,
    #          ClientMapConstants[ClientConstants.xyl_sales_repertory][MapFields.xyl_sku], "B:B")

    # 示例用法
    file_path = "/Users/zkp/Downloads/order_120250619100239782_1573179.xlsx"
    result = count_store_accounts(file_path)

    # 输出结果
    for account, count in result.items():
        print(f"{account}: {count}")
