import pandas as pd  # as是别名的意思，相当于kotlin的as、
import numpy as np

"""
极客教程: https://geek-docs.com/pandas/pandas-tutorials/pandas-tutorial.html
"""


def statistics_demo():
    data = {
        'Name': pd.Series(
            ['Tom', 'James', 'Ricky', 'Vin', 'Steve', 'Minsu', 'Jack', 'Lee', 'David', 'Gasper', 'Betina', 'Andres']),
        'Age': pd.Series([25, 26, 25, 23, 30, 29, 23, 34, 40, 30, 51, 46]),
        'Rating': pd.Series([4.23, 3.24, 3.98, 2.56, 3.20, 4.6, 3.8, 3.78, 2.98, 4.80, 4.10, 3.65])
    }
    df = pd.DataFrame(data)
    print("默认情况下axis=0，返回所有数值列轴的值的总和:\n", df.sum())  # 默认只计算数字的列
    print("axis=1，返回所请求数值行轴的值的总和:\n", df.sum(1))
    print("默认情况下axis=0，返回所有数值列轴的平均值，:\n", df.mean())
    print("默认情况下axis=0，返回数值列的Bressel标准偏差，:\n", df.std())
    # include参数，默认是number：
    # object – 汇总字符串列
    # number – 汇总数字列
    # all – 将所有列汇总在一起(不应将其作为列表值传递)
    print("describe()函数是用来计算有关 数字列 列的统计信息的摘要:\n", df.describe())
    pass


def adder(ele1, ele2):
    return ele1 + ele2


def pipe_demo():
    dictionary = {'Site': [1, 2, 3], 'Age': [10, 12, 13]}
    data_frame = pd.DataFrame(dictionary)
    # 通过将函数和适当数量的参数作为管道参数来执行自定义操作，从而对整个DataFrame(所有元素)执行操作。
    # adder有两个参数，参数1默认传递的是DataFrame的元素，参数2是外部传入的
    pipe = data_frame.pipe(adder, 2)
    print("默认情况下axis=0，返回数值列的Bressel标准偏差，:\n", pipe)
    # apply = data_frame.apply(data_frame.mean)
    # print(apply)

    apply = data_frame.apply(np.sum)
    print(apply)
    pass


if __name__ == '__main__':
    # statistics_demo()
    pipe_demo()
    pass
