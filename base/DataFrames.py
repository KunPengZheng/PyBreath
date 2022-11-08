import pandas as pd  # as是别名的意思，相当于kotlin的as


def create_demo():
    """
      DataFrame 是一个表格型的数据结构（包含 rows（行） 和 columns（列），二维数据结构），它含有一组有序的列，每列可以是不同的
      值类型（数值、字符串、布尔型值）。DataFrame 既有行索引也有列索引，它可以被看做由 Series 组成的字典（共同用一个索引）。
      """
    # list创建方式
    row_list = [['Google', 10], ['Runoob', 12], ['Wiki', 13]]
    column_list = ['Site', 'Age']
    data_frame1 = pd.DataFrame(row_list, columns=column_list)
    print("data_frame1:\n", data_frame1)

    # 字典的创建方式
    list_dic = [{'a': 1, 'b': 2}, {'a': 5, 'b': 10, 'c': 20}]
    data_frame2 = pd.DataFrame(list_dic)
    # 没有对应的部分数据为 NaN
    print("data_frame2:\n", data_frame2)
    # 使用与字典键相同的列索引创建的
    data_frame2_1 = pd.DataFrame(list_dic, index=['first', 'second'], columns=['a', 'b'])
    # 使用字典键以外的列索引创建DataFrame，使用NaN填写空白区域
    data_frame2_2 = pd.DataFrame(list_dic, index=['first', 'second'], columns=['a', 'b1'])
    print("data_frame2_1:\n", data_frame2_1)
    print("data_frame2_2:\n", data_frame2_2)

    dictionary = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
    # 字典创建，key就是列头，value就是列值
    data_frame3 = pd.DataFrame(dictionary)
    print("data_frame3:\n", data_frame3)

    # 字典的value是Series 创建 DataFrame
    series_dictionary = {
        "one": pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        'two': pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
    }
    data_frame4 = pd.DataFrame(series_dictionary)
    print("data_frame4:\n", data_frame4)

    column_index_list = ["day1", "day2", "day3"]
    # 指定行的索引值
    data_frame5 = pd.DataFrame(dictionary, index=column_index_list)
    print("data_frame5:\n", data_frame5)


def read_demo():
    dictionary = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
    data_frame3 = pd.DataFrame(dictionary)

    # loc 属性返回指定行的数据，如果没有设置索引则第一行索引为 0。注意：返回结果其实就是一个 Pandas Series 数据。
    print("loc返回指定的行:\n", data_frame3.loc[0])
    # 返回多行数据，参数是一个列表，列表的元素则是行的索引。注意：返回结果其实就是一个 Pandas Series 数据。
    print("loc返回多行:\n", data_frame3.iloc[[0, 1]])
    # iloc()纯粹基于整数位置的索引，用于按位置进行选择。(loc是可以指定的且不一定为整数，而iloc是不能指定的且一定为整数（默认0开始）)
    print("iloc返回指定的行:\n", data_frame3.iloc[0])
    # 可以使用:运算符选择多行
    print("运算符选择多行:\n", data_frame3[0:2])

    # 返回指定的列
    print("返回指定的列:\n", data_frame3["Site"])
    # 返回多列
    print("返回多列:\n", data_frame3[["Site", 'Age']])


def add_demo():
    dictionary = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
    data_frame = pd.DataFrame(dictionary)
    # 新增列，value是列表
    data_frame['Unit'] = [1, 2, 3]
    # 新增列，value是Series
    data_frame["Floor"] = pd.Series([1, 2, 3])
    # 新增列，value是Unit列和three列的和
    data_frame["Number"] = data_frame["Unit"] + data_frame["Floor"]
    print("新增列:\n", data_frame)

    df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'])
    df2 = pd.DataFrame([[5, 6], [7, 8]], columns=['a', 'b'])
    # append新增行
    df = df.append(df2)
    print("新增行:\n", df)
    pass


def change_demo():
    dictionary = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
    data_frame = pd.DataFrame(dictionary)
    # 如何修改某一列特定几行元素的值
    array = data_frame.Unit.isin([1, 2, 3])  # DataFrame.列名 返回的是一个 Pandas Series 数据
    data_frame.loc[array, "Unit"] = 4  # 修改DataFrame指定列的Series数据
    print("如何修改某一列特定几行元素的值:\n", data_frame)


def del_demo():
    series_dictionary = {
        'one': pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        'two': pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd']),
        'three': pd.Series([10, 20, 30], index=['a', 'b', 'c'])
    }
    data_frame = pd.DataFrame(series_dictionary)

    # pop移除列
    data_frame.pop("two")
    # del移除列
    del data_frame["one"]
    print(data_frame)

    df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'])
    df2 = pd.DataFrame([[5, 6], [7, 8]], columns=['a', 'b'])
    df = df.append(df2)
    print("注意标签:\n", df)
    # drop删除行。如果标签重复，则会删除多行。
    df = df.drop(0)
    print("drop删除:\n", df)


def api_demo():
    dictionary = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
    data_frame = pd.DataFrame(dictionary)
    # T (转置)
    print("T交换行和列:\n", data_frame.T)
    # axes返回行轴标签和列轴标签列表
    print("axes返回行轴标签和列轴标签列表:\n", data_frame.axes)
    print("empty表示对象是否为空:\n", data_frame.empty)
    print("ndim返回对象的维数:\n", data_frame.ndim)  # 一维还是二维
    print("shape返回对象的行数和列数的元组:\n", data_frame.ndim)
    print("size 返回 DataFrame 中的元素个数（行数 x 列数）:\n", data_frame.size)
    # 最外层是一个list，内部的元素也是list，内部元素list的元素是行数据
    print("values 将DataFrame中的实际数据作为NDarray返回:\n", data_frame.values)
    print("head()返回前n行(观察索引值)。默认数量为5，可以传递自定义数值。:\n", data_frame.head())
    print("tail()返回最后n行(观察索引值)。默认数量为5，可以传递自定义数值。:\n", data_frame.tail())
    pass


if __name__ == '__main__':
    # create_demo()
    # read_demo()
    # add_demo()
    # del_demo()
    # change_demo()
    api_demo()
