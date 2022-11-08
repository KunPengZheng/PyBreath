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


if __name__ == '__main__':
    series_demo()
