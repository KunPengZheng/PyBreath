import pandas as pd  # as是别名的意思，相当于kotlin的as


def series_demo():
    """
    Pandas Series 是pandas中的一维数据结构，类似表中的一个列（类似于python中的列表Numpy中的Ndarray对象），可以保存任何数据类型。
    """

    list1 = [1, 2, 3]
    # 没有指定索引，索引值就从 0 开始
    series1 = pd.Series(list1)
    print(series1)

    list2 = ["Google", "Runoob", "Wiki"]
    list2_index = ["x", "y", "z"]
    # 指定角标
    series2 = pd.Series(list2, list2_index)
    print(series2)
    print(series2["y"])  # 根据索引值读取数据
    print(series2[:2])  # 获取前两个元素
    print(series2[["x", "y"]])  # 使用索引获取多个元素

    dictionary = {1: "Google", 2: "Runoob", 3: "Wiki"}
    # 字典来创建 Series
    series3 = pd.Series(dictionary)
    print(series3)
    # 如果只需要字典中的一部分数据，只需要指定需要数据的索引即可
    series4 = pd.Series(dictionary, [1, 2])
    print(series4)
    # 按照索引排列，当索引对应的value不存在则为NaN
    series5 = pd.Series(dictionary, [3, 1, 2, 4])
    print(series5)
    # 设置 Series 名称参数
    series6 = pd.Series(dictionary, [1, 2], name="RUNOOB-Series-TEST")
    print(series6)
    pass


def date_frame_demo():
    """
    DataFrame 是一个表格型的数据结构（包含 rows（行） 和 columns（列），二维数据结构），它含有一组有序的列，每列可以是不同的
    值类型（数值、字符串、布尔型值）。DataFrame 既有行索引也有列索引，它可以被看做由 Series 组成的字典（共同用一个索引）。
    """

    row_list = [['Google', 10], ['Runoob', 12], ['Wiki', 13]]
    column_list = ['Site', 'Age']
    data_frame1 = pd.DataFrame(row_list, columns=column_list)
    print("data_frame1:\n", data_frame1)

    list_dic = [{'a': 1, 'b': 2}, {'a': 5, 'b': 10, 'c': 20}]
    data_frame2 = pd.DataFrame(list_dic)
    # 没有对应的部分数据为 NaN
    print("data_frame2:\n", data_frame2)

    dictionary = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
    # 字典创建，key就是列头，value就是列值
    data_frame3 = pd.DataFrame(dictionary)
    print("data_frame3:\n", data_frame3)
    # loc 属性返回指定行的数据，如果没有设置索引则第一行索引为 0。注意：返回结果其实就是一个 Pandas Series 数据。
    print("返回第一行:\n", data_frame3.loc[0])
    # 返回多行数据，参数是一个列表，列表的元素则是行的索引。注意：返回结果其实就是一个 Pandas Series 数据。
    print("返回多行:\n", data_frame3.loc[[0, 1]])
    # 返回指定的列
    print("返回指定的列:\n", data_frame3["Site"])
    # 返回多列
    print("返回多列:\n", data_frame3[["Site", 'Age']])

    column_index_list = ["day1", "day2", "day3"]
    # 指定行的索引值
    data_frame4 = pd.DataFrame(dictionary, index=column_index_list)
    print("data_frame4:\n", data_frame4)
    pass


if __name__ == '__main__':
    series_demo()
    date_frame_demo()
    # long_series = pd.Series(np.random.randn(1000))
    # head = long_series.head()
    # print(head)
