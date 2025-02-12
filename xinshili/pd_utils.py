import pandas as pd


def remove_duplicates_by_column(input_file, output_file, column_name):
    """
    删除指定列中重复的行，仅保留第一条，并覆盖源文件。

    参数：
    - input_file: str，输入文件路径
    - column_name: str，要检查重复的列名
    """
    try:
        # 读取 Excel 文件
        df = pd.read_excel(input_file)
        # 检查列名是否存在
        if column_name not in df.columns:
            raise ValueError(f"列 '{column_name}' 不存在于输入文件中！")
        # 删除指定列的重复项，仅保留第一条
        df_deduplicated = df.drop_duplicates(subset=[column_name], keep='first')
        df_deduplicated.to_excel(output_file, index=False)
    except Exception as e:
        print(f"处理文件时发生错误：{e}")
