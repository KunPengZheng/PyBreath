import pandas as pd  # as是别名的意思，相当于kotlin的as
import numpy as np
import openpyxl


def create_demo():
    """
      DataFrame 是一个表格型的数据结构（包含 rows（行） 和 columns（列），二维数据结构），它含有一组有序的列，每列可以是不同的
      值类型（数值、字符串、布尔型值）。DataFrame 既有行索引也有列索引，它可以被看做由 Series 组成的字典（共同用一个索引）。
      """
    # list创建方式
    row_data = [['Google', 10], ['Runoob', 12], ['Wiki', 13]]
    column_index = ['Site', 'Age']
    data_frame1 = pd.DataFrame(row_data, columns=column_index)
    print("data_frame1:\n", data_frame1)

    # 列表的元素是字典的创建方式
    list_dic = [{'a': 1, 'b': 2}, {'a': 5, 'b': 10, 'c': 20}]
    data_frame2 = pd.DataFrame(list_dic)
    # 没有对应的部分数据为 NaN
    print("data_frame2:\n", data_frame2)
    # 以字典的键重新指定列索引，新的dataframe的列长度以列索引的数据长度为准
    data_frame2_1 = pd.DataFrame(list_dic, index=['first', 'second'], columns=['a', 'b'])
    print("data_frame2_1:\n", data_frame2_1)
    # 使用字典键以外的列索引创建DataFrame，使用NaN填写空白区域
    data_frame2_2 = pd.DataFrame(list_dic, index=['first', 'second'], columns=['a', 'b1'])
    print("data_frame2_2:\n", data_frame2_2)

    # 字典创建，key就是列头，value就是列值
    dictionary = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
    column_index_list = ["day1", "day2", "day3"]
    data_frame3 = pd.DataFrame(dictionary, index=column_index_list)
    print("data_frame3:\n", data_frame3)

    # 字典的value是Series 创建 DataFrame
    series_dictionary = {
        "one": pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        'two': pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
    }
    data_frame4 = pd.DataFrame(series_dictionary)
    print("data_frame4:\n", data_frame4)


def read_demo():
    dictionary = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
    data_frame = pd.DataFrame(dictionary)

    # 返回指定行索引的Series。
    print("loc返回指定的行:\n", data_frame.loc[0])
    print("loc提取指定的行和列的内容:\n", data_frame.loc[0, "Site"])
    # 返回指定多个行索引的DataFrame。iloc的参数只能是整数
    print("iloc返回多行:\n", data_frame.iloc[[0, 1]])
    print("loc返回多个指定行和列的内容:\n", data_frame.loc[[0, 1], ["Site"]])
    # 可以使用:运算符选择多行
    print("运算符选择多行:\n", data_frame[0:2])

    # 返回指定列索引的Series。
    print("返回指定的列:\n", data_frame["Site"])
    # 返回多个指定列索引的DataFrame
    print("返回多列:\n", data_frame[["Site", 'Age']])

    data_frame2 = pd.DataFrame({"x": [1, 2, 3, 4], "y": [5, 6, 7, 8], "z": [9, 10, 11, 12]}, index=["a", "b", "c", "d"])
    # 通过 data_frame2["x"] > 2 筛选出只有cd行符合，ab行不符合。所以输出内容只有cd行
    print("条件筛选:\n", data_frame2[data_frame2["x"] > 2])
    # 使用逻辑运算符 &（与）和 |（或）来链接多个条件语句
    print("条件筛选:\n", data_frame2[(data_frame2["x"] > 2) & (data_frame2["y"] > 7)])

    data_frame3 = pd.DataFrame({"x": [1, 2, 3, 4], "y": ["5", "6", "7", "8"], "z": [True, True, False, False]},
                               index=["a", "b", "c", "d"])
    data_frame3 = data_frame3.select_dtypes(include=["int", "bool"])
    print("根据数据的类型选择列:\n", data_frame3)


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
    # 堆叠concatO()，就是简单地把多个 DataFrame 堆在一起，拼成一个更大的 DataFrame。默认按行的方向堆叠
    concat = pd.concat([df, df2])
    # df.append(df2) # append()作用相同，但未来版本可能被废除
    print("新增行:\n", concat)

    left = pd.DataFrame({"key": ["K0", "K4", "K5", "K6"], "A": ["A0", "A1", "A2", "A3"], "B": ["B0", "B1", "B2", "B3"]})
    right = pd.DataFrame(
        {"key": ["K0", "K1", "K2", "K3"], "C": ["C0", "C1", "C2", "C3"], "D": ["D0", "D1", "D2", "D3"]})
    # 指定相同的列索引，将多个 DataFrame 合并在一起。
    # left放在前面的DataFrame；right放在后面的DataFrame；on：列索引关键字，how的判断依据
    # how指两个DataFrame存在不重合的key时，取结果的方式。inner：交集；outer：并集；left：左侧取全部，右侧取相同部分；right：和left相反。
    merge = pd.merge(left, right, how="inner", on="key")
    print("共同列，归并:\n", merge)

    left = pd.DataFrame({"A": ["A0", "A1", "A2"], "B": ["B0", "B1", "B2"]}, index=["K0", "K1", "K2"])
    right = pd.DataFrame({"C": ["C0", "C1", "C2"], "D": ["D0", "D1", "D2"]}, index=["K0", "K2", "K3"])
    # 若要把两个表连在一起，然而它们之间没有太多共同的列，可以选择使用.join() 方法。和 .merge() 不同，连接采用索引作为公共的键，而不是某一列。
    join = left.join(right)  # 默认以调用者的索引作为公共的键
    print("连接:\n", join)
    pass


def change_demo():
    data_frame = pd.DataFrame({"x": [1, 2, 3, 4], "y": [5, 6, 7, 8], "z": [9, 10, 11, 12]}, index=["a", "b", "c", "d"])
    # 将原来的索引保存在一个叫 index 的列中。原数据其实并没有真正的删除，只是在返回值DataFrame才看不见，如果要直接操作原数据，加上 inplace=True 参数
    data_frame = data_frame.reset_index()
    # data_frame.reset_index(inplace=True)  # 相当于👆的逻辑
    print("重制索引，默认为从0开始的数字:\n", data_frame)
    data_frame["id"] = ["id1", "id2", "id3", "id4"]
    # set_index() 方法，将 DataFrame 里的某一列作为索引来用，直接覆盖原来的索引
    data_frame = data_frame.set_index("id")
    print("重制索引，使用某一列作为索引:\n", data_frame)

    # np.nan为缺失值"NaN"
    data_frame2 = pd.DataFrame({"x": [1, np.nan, 3, 4], "y": [5, 6, np.nan, 8]})
    print("缺失值:\n", data_frame2)
    data_frame2_1 = data_frame2.dropna(axis=0)
    print("dropna()指定行活着列删除缺失值:\n", data_frame2_1)
    data_frame2_2 = data_frame2.fillna("缺失值")
    print("fillna()填充缺失值:\n", data_frame2_2)

    # dictionary = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
    # data_frame = pd.DataFrame(dictionary)
    # # 如何修改某一列特定几行元素的值
    # array = data_frame.Unit.isin([1, 2, 3])  # DataFrame.列名 返回的是一个 Pandas Series 数据
    # data_frame.loc[array, "Unit"] = 4  # 修改DataFrame指定列的Series数据
    # print("如何修改某一列特定几行元素的值:\n", data_frame)


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
    # drop的axis=1表示删除列。原数据其实并没有真正的删除，只是在返回值DataFrame才看不见，如果要直接操作原数据，加上 inplace=True 参数
    data_frame = data_frame.drop('three', axis=1)
    # data_frame.drop('three', axis=1, inplace=True)  # 相当于👆的逻辑
    print("删除列:\n", data_frame)

    df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'])
    df2 = pd.DataFrame([[5, 6], [7, 8]], columns=['a', 'b'])
    concat = pd.concat([df, df2])
    print("注意concat的行标签存在相同:\n", concat)
    # drop的axis=0表示删除行
    drop = concat.drop(0, axis=0)
    print("删除行:\n", drop)

    df3 = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]}, index=["a", "b", "c"])
    print("同时删除指定的行和列:\n", df3.drop(index="c", columns="col1"))


def api_demo():
    dictionary = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
    data_frame = pd.DataFrame(dictionary)
    # info函数返回有哪些列、有多少非缺失值、每列的类型
    print(data_frame.info())
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

    series = pd.Series(['Google', 'Runoob', 'Wiki'])
    to_frame = series.to_frame()
    print("to_frame()将Series转换为DataFrame:\n", to_frame)

    data_frame2 = pd.DataFrame({
        'company': ['A', 'A', 'C', 'B', 'B'],
        'salary': [13, 14, 15, 16, 17],
        'age': [21, 22, 23, 24, 25],
    })
    # 根据指定的列标签进行分组，相同的列值为一组
    groupby = data_frame2.groupby("company")
    print("分组的平均值:\n", groupby.mean())
    print("分组的次数:\n", groupby.count())
    # 计数、平均数、标准差、最小值、25% 50% 75% 位置的值、最大值。自行选择分位数 percentiles=[.05, .25, .75, .95]
    print("分组的数据描述:\n", groupby.describe())
    # transpose() 方法获得一个竖排的格式
    print("分组的数据描述的竖排的格式:\n", groupby.describe().transpose())

    data_frame3 = pd.DataFrame({"col": [444, 555, 666, 444, np.nan]})
    print("不重复的值:\n", data_frame3["col"].unique())
    print("不重复值的个数:\n", data_frame3["col"].nunique())
    print("返回不重复的值及其个数:\n", data_frame3["col"].value_counts())
    # 注意：表格变成按 col 列的值从小到大排序。要注意的是，表格的索引 index 还是对应着排序前的行，并没有因为排序而丢失原来的索引数据。
    print("sort_values() 将整个表按某一列的值进行排序:\n", data_frame3.sort_values("col"))
    print("查找空值，对应位置返回布尔值（True/False）表示原 DataFrame 中对应位置的数据是否是空值:\n", data_frame3.isnull())

    lambda1 = lambda a: a + 10
    data_frame4 = pd.DataFrame({"col": [2, 3, 4, 5]}, index=["a", "b", "c", "d"])
    print("apply()应用自定义函数，进行数据处理:\n", data_frame4["col"].apply(lambda1))
    print("columns获取列名List及其数据类型:\n", data_frame4.columns)
    print("columns获取行名List及其数据类型:\n", data_frame4.index)

    data_frame5 = pd.DataFrame({"col": [2, 3, 4, 5]}, index=["a", "b", "c", "d"])
    data_frame5 = data_frame5.rename(index={"a": "aa"}, columns={"col": "coll"})
    print("rename()修改行或列名:\n", data_frame5)

    df1 = pd.DataFrame({'A': [1, 2, 3]}, index=[1, 2, 3])
    df2 = pd.DataFrame({'A': [1, 2, 3]}, index=[3, 1, 2])
    # 索引对齐特性，算术运算中会获取相同的列和行索引进行运算
    print("索引对齐特性:\n", df1 - df2)

    data_frame2 = pd.DataFrame({"x": [1, 2, 3, 4], "y": [5, 6, 7, 8], "z": [9, 10, 11, 12]}, index=["a", "b", "c", "d"])
    print("idxmax()返回最大值所在索引1:\n", data_frame2.idxmax())  # idxmin()功能类似
    print("idxmax()返回最大值所在索引2:\n", data_frame2["x"].idxmax())
    print("nlargest()返回前几个大的元素值1:\n", data_frame2.nlargest(2, columns=["x"]))  # nsmallest()功能类似
    print("nlargest()返回前几个大的元素值2:\n", data_frame2["x"].nlargest(2))
    print("clip()是指低于指定的lower用lower替换，高于指定的upper用upper替换:\n", data_frame2["x"].clip(lower=1, upper=3))
    print("replace()是对某些值进行替换:\n", data_frame2["x"].replace([1, 2], [5, 5]))
    pass


def mult_index():
    """
    https://www.jianshu.com/p/d30fdfbeb312
    多级索引:指数据在一个轴上（行或者列）拥有多个（两个以上）索引级别。它可以使用户能以低维度形式处理高维度数据。
    """
    tuples = [("Python", "期中"), ("Python", "期末"), ("Java", "期中"), ("Java", "期末")]
    # names：索引列名
    from_tuples = pd.MultiIndex.from_tuples(tuples, names=('Subjects', 'Time'))
    data_frame = pd.DataFrame({"A": [1, 2, 3, 4], "B": [5, 6, 7, 8], "C": [9, 10, 11, 12]}, index=from_tuples)
    print("data_frame:\n", data_frame)
    print("data_frame:\n", data_frame.loc["Python"])  # 要获取多级索引中的数据，还是用到 .loc[]
    print("data_frame:\n", data_frame.loc["Python"].loc["期中"])  # 然后再用一次.loc[]，获取下一层的数据，不能直接获取第二层的数据
    print("data_frame:\n", data_frame.xs("期中", level="Time"))  # 获取到多级索引中某些特定级别的数据


def read_write_csv():
    data_frame = pd.DataFrame({"x": [1, 2, 3, 4], "y": [5, 6, 7, 8], "z": [9, 10, 11, 12]}, index=["a", "b", "c", "d"])
    # 参数 index=False 参数是因为不希望 Pandas 把行索引也存到文件中
    data_frame.to_csv("CVS_DataFrame", index=False)

    csv = pd.read_csv("CVS_DataFrame")
    print("读取csv文件:\n", csv)
    pass


def read_write_excel():
    data_frame = pd.DataFrame({"x": [1, 2, 3, 4], "y": [5, 6, 7, 8], "z": [9, 10, 11, 12]}, index=["a", "b", "c", "d"])
    # 参数 index=False 参数是因为不希望 Pandas 把行索引也存到文件中
    data_frame.to_excel("Excel_DataFrame.xlsx", sheet_name="Sheet1", index=False)

    excel = pd.read_excel("Excel_DataFrame.xlsx", sheet_name="Sheet1")
    print("读取excel文件:\n", excel)
    pass


if __name__ == '__main__':
    create_demo()
    read_demo()
    add_demo()
    del_demo()
    change_demo()
    mult_index()
    api_demo()
    # read_write_csv()
    # read_write_excel()
