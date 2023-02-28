import pandas as pd
import numpy as np


def single_index_demo():
    dictionary = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
    data_frame = pd.DataFrame(dictionary)

    """
    1.loc中能传入的只有布尔列表和索引子集构成的列表
    2.iloc中接收的参数只能为整数或整数列表或布尔列表
    3.一般来说，[]操作符常用于列选择或布尔选择，尽量避免行的选择
    """
    # 返回指定行索引的Series。
    print("loc返回指定的行(返回Series类型):\n", data_frame.loc[0])
    print("区间运算符选择多行(返回DataFrame类型):\n", data_frame[0:2])
    print("loc返回所有行的指定的列(返回Series类型):\n", data_frame.loc[:, "Age"])
    print("loc提取指定的行和列的内容（返回元素的类型）:\n", data_frame.loc[0, "Site"])
    print("loc指定多个行索引返回多行(返回DataFrame类型):\n", data_frame.loc[[0, 1]])
    print("loc返回指定多列的所有行(返回DataFrame类型):\n", data_frame.loc[:, ["Site", "Age"]])
    print("loc返回指定列的指定多行(返回DataFrame类型):\n", data_frame.loc[[0, 1], ["Site"]])
    print("loc区间返回多行和多列(返回DataFrame类型):\n", data_frame.loc[0:1, "Site":"Age"])
    print("loc步长区间索引(返回DataFrame类型):\n", data_frame.loc[0:2:2, "Site":"Age"])
    print("loc函数式（lambda表达式）索引(返回DataFrame类型):\n",
          data_frame.loc[lambda x: x["Age"] >= 13])  # x参数就是data_frame
    print("loc函数式索引(返回DataFrame类型):\n", data_frame.loc[inner_demo])
    print("loc布尔索引(返回DataFrame类型):\n", data_frame.loc[data_frame["Age"].isin([13])])

    # 返回指定列索引的Series。
    print("返回指定的列:\n", data_frame["Site"])
    # 返回多个指定列索引的DataFrame
    print("返回多列:\n", data_frame[["Site", 'Age']])

    data_frame2 = pd.DataFrame({"x": [1, 2, 3, 4], "y": [5, 6, 7, 8], "z": [9, 10, 11, 12]}, index=["a", "b", "c", "d"])
    # 通过 data_frame2["x"] > 2 筛选出只有cd行符合，ab行不符合。所以输出内容只有cd行
    print("单条件筛选:\n", data_frame2[data_frame2["x"] > 2])
    # 使用逻辑运算符 &（与）和 |（或）来链接多个条件语句
    print("多条件筛选:\n", data_frame2[(data_frame2["x"] > 2) & (data_frame2["y"] > 7)])

    s_int = pd.Series([1, 2, 3, 4], index=[1, 3, 5, 6])
    s_float = pd.Series([1, 2, 3, 4], index=[1., 3., 5., 6.])
    print("int角标，区间选择（直接获取start-end的角标，不匹配index）:\n", s_int[2:])  # 不推荐[i,j]的索引行为，推荐使用loc
    # 请不要在行索引为浮点时使用[]操作符，因为在Series中[]的浮点切片并不是进行位置比较，而是值比较，非常特殊
    print("float角标，区间选择:\n", s_float[2:])

    data_frame3 = pd.DataFrame({"x": [1, 2, 3, 4], "y": ["5", "6", "7", "8"], "z": [True, True, False, False]},
                               index=["a", "b", "c", "d"])
    data_frame3 = data_frame3.select_dtypes(include=["int", "bool"])
    print("根据数据的类型选择列:\n", data_frame3)
    print("快速标量索引at:", data_frame3.at["a", "x"])  # 当只需要取一个元素时，at和iat方法能够提供更快的实现：
    print("快速标量索引iat:", data_frame3.iat[0, 0])  # 按整数位置获取行/列 对应的单个元素

    # #closed参数可选'left''right''both''neither'，默认左开右闭
    interval_range = pd.interval_range(0, 5)
    print("区间索引1:\n", interval_range)
    # periods参数控制区间个数，freq控制步长
    pd_interval_range = pd.interval_range(start=0, periods=8, freq=5)
    print("区间索引2:\n", pd_interval_range)


def inner_demo(df):
    print("参数是DataFrame：", df)
    return [0, 1]


def mult_index_demo():
    """
     https://www.jianshu.com/p/d30fdfbeb312
     多级索引:指数据在一个轴上（行或者列）拥有多个（两个以上）索引级别。它可以使用户能以低维度形式处理高维度数据。
     """

    def from_tuples_demo():
        # n层索引就像是n+1层索引的概括
        tuples = [("Python", "期中"), ("Python", "期末"), ("Java", "期中"), ("Java", "期末")]  # 直接创建元组
        tuples = [["Python", "期中"], ["Python", "期末"], ["Java", "期中"], ["Java", "期末"]]  # 通过Array创建
        tuples = list(zip(('Python', 'Python', 'Java', 'Java'), ('期中', '期末', '期中', '期末')))  # 利用zip创建元组
        # 创建多级索引， names：索引列名
        from_tuples = pd.MultiIndex.from_tuples(tuples, names=('Subjects', 'Time'))
        data_frame = pd.DataFrame({"A": [1, 2, 3, 4], "B": [5, 6, 7, 8], "C": [9, 10, 11, 12]}, index=from_tuples)
        print("from_tuples创建多级索引:\n", data_frame)
        print("from_tuples使用loc单层索引:\n", data_frame.loc["Python"])
        # 相当于data_frame.loc["Python"].loc["期中"]
        print("from_tuples使用loc多层索引:\n", data_frame.loc["Python", "期中"])
        print("from_tuples使用loc区间索引1（必须排序）:\n", data_frame.sort_index().loc[("Java", "期末"): ("Python", "期中")])
        print("from_tuples使用loc区间索引2（必须排序）:\n", data_frame.sort_index().loc[("Java", "期末"): "Python"])
        print("from_tuples使用loc选择某几个元素（必须排序）:\n", data_frame.sort_index().loc[[("Java", "期末"), ("Python", "期中")]])# 由元组构成列表
        print("xs()获取到多级索引中某些特定级别的数据:\n", data_frame.xs("期中", level="Time"))  # 获取到多级索引中某些特定级别的数据

        L1, L2 = ['A', 'B', 'C'], ['a', 'b', 'c']
        mul_index1 = pd.MultiIndex.from_product([L1, L2], names=('Upper', 'Lower'))
        L3, L4 = ['D', 'E', 'F'], ['d', 'e', 'f']
        mul_index2 = pd.MultiIndex.from_product([L3, L4], names=('Big', 'Small'))
        df_s = pd.DataFrame(np.random.rand(9, 9), index=mul_index1, columns=mul_index2)
        print("行列都是多层索引:\n", df_s)
        # 多层索引中的slice对象
        idx = pd.IndexSlice
        # df_s.sum()默认为对列求和，因此返回一个长度为9的数值列表
        print("索引Slice的使用非常灵活:\n", df_s.loc[idx['B':, df_s['D']['d'] > 0.3], idx[df_s.sum() > 4]])

    def from_product_demo():
        l1 = ['Python', 'Java']
        l2 = ['期中', '期末']
        # 两两相乘
        from_tuples = pd.MultiIndex.from_product([l1, l2], names=('Subjects', 'Time'))
        data_frame = pd.DataFrame({"A": [1, 2, 3, 4], "B": [5, 6, 7, 8], "C": [9, 10, 11, 12]}, index=from_tuples)
        print("from_product创建多级索引:\n", data_frame)
        pass

    def set_index_demo():
        data_frame = pd.DataFrame({"A": [1, 2, 3, 4], "B": [5, 6, 7, 8], "C": [9, 10, 11, 12],
                                   "Subjects": ["Python", "Python", "Java", "Java"],
                                   "Time": ["期中", "期末", "期中", "期末"]})
        data_frame.set_index(['Subjects', 'Time'], inplace=True)
        print("set_index()创建多级索引:\n", data_frame)
        pass

    from_tuples_demo()
    # from_product_demo()
    # set_index_demo()


if __name__ == '__main__':
    # single_index_demo()
    mult_index_demo()
