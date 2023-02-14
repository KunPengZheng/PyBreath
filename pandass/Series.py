import pandas as pd  # as是别名的意思，相当于kotlin的as
import numpy as np

"""
pandas 是基于NumPy 的一种工具，该工具是为了解决数据分析任务而创建的。简单地说，你可以把 Pandas 看作是 Python 版的 Excel。
"""


def series_demo():
    """
     Series 是pandas中的一维数据结构，类似表中的一个列（类似于python中的列表，Numpy中的Ndarray对象），可以保存任何数据类型。
    """

    list1 = [1, 2, 3]
    # 没有指定索引，索引值就从 0 开始
    series1 = pd.Series(list1)
    print("没有指定索引，索引值就从 0 开始:\n", series1)

    # python list创建Series
    list2 = ["Google", "Runoob", "Wiki"]
    list2_index = ["x", "y", "z"]
    # 参数：指定索引；参数3： 设置 Series 名称
    series2 = pd.Series(list2, list2_index)
    print(series2)
    print("根据索引值读取数据:", series2["y"])  # 根据索引值读取数据
    print("根据索引截取元素:\n", series2[:2])  # 根据索引截取元素
    print("使用索引获取多个元素:\n", series2[["x", "y"]])  # 使用索引获取多个元素

    # 从python dict创建Series
    dictionary = {1: "Google", 2: "Runoob", 3: "Wiki"}
    # 当索引对应的value不存在则为NaN。dict的方式配置新索引不会检查长度问题，而list方式会检查数据和索引的长度是否一致
    series3 = pd.Series(dictionary, [3, 1, 2, 4])
    print(series3)

    # 从numpy ndarray创建Series
    np_arr = np.array([1, 2, 3])
    series4 = pd.Series(np_arr)
    print(series4)

    # 如果数据是标量值，则必须提供索引。将重复该值以匹配索引的长度。
    series5 = pd.Series(5, index=["a", "b", "c", "d", "e"])
    print(series5)

    series6 = pd.Series([1, 2, 3, 4], ["a", "b", "c", "d"])
    series7 = pd.Series([5, 6, 7, 8], ["a", "e", "c", "f"])
    # 对 Series 进行算术运算操作，Pandas 将会根据索引 index，对响应的数据进行计算，结果将会以浮点数的形式存储，以避免丢失精度。 如果 Pandas
    # 在两个 Series 里找不到相同的 index，对应的位置就返回一个空值 NaN。
    print(series6 - series7)
    pass


if __name__ == '__main__':
    series_demo()
