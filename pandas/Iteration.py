import pandas as pd  # as是别名的意思，相当于kotlin的as、
import numpy as np

"""
迭代：Series 迭代时被视为数组，基础迭代生成值。DataFrame 则遵循字典式习语，用对象的 key 实现迭代操作。
    1. 基础迭代（for i in object）生成：
        Series ：值
        DataFrame：列标签
    2. iteritems()迭代生成(key，value)对，列标签作为key，series作为value（行标签作为key，元素作为value），可以认为是逐列遍历
    3. iterrows()迭代生成(key，value)对，行标签作为key，series作为value（其中列标签作为key，元素作为value），可以认为是逐行遍历
    3. itertuples()返回元组，第一个元素是行的相应索引值（Index=行索引），其余元素是行值（列索引=列对应的行值）。
"""


def reindex_demo():
    df = pd.DataFrame({"A": [1, 5, 3, 4, 2],
                       "B": [3, 2, 4, 3, 4],
                       "C": [2, 2, 7, 3, 4],
                       "D": [4, 3, 6, 12, 7]},
                      index=["A1", "A2", "A3", "A4", "A5"])
    # 基础迭代
    for col in df:
        print("迭代DataFrame获取列名:", col)

    # iteritems迭代
    for key, value in df.iteritems():
        print("列标签作为key，series作为value（其中行标签作为key，元素作为value）:\n", f"key:{key}\n", value)

    # iterrows迭代
    for key, value in df.iterrows():
        print("行标签作为key，series作为value（其中列标签作为key，元素作为value）:\n", f"key:{key}\n", value)

    # itertuples迭代
    for ele in df.itertuples():
        print("返回元组，第一个元素是行的相应索引值（Index=行索引），其余元素是行值（列索引=列对应的行值）:\n", ele)
    pass


if __name__ == '__main__':
    reindex_demo()
    pass
