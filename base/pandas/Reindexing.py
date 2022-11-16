import pandas as pd  # as是别名的意思，相当于kotlin的as、
import numpy as np

"""
重新索引：
1. 根据指定的行列标签，筛选数据并根据行标签的元素顺序和列标签的元素顺序重新排序 （ 其实也叫重命名轴索引）
2. 在无数据但有标签的位置插入缺失值（NA）标记
"""


def reindex_demo():
    dictionary = {'Site': [1, 2, 3], 'Age': [10, 12, 13]}
    data_frame = pd.DataFrame(dictionary)

    reindex = data_frame.reindex(index=[0, 2], columns=["Age", "Site"])
    print("reindex根据行列标签筛选并排序数据:\n", reindex)

    # DataFrame.reindex() 还支持 “轴样式”调用习语，可以指定单个 labels 参数，并指定应用于哪个 axis。
    reindex = data_frame.reindex([0, 1], axis='index')  # 指定行的下标
    print("轴样式语法，指定索引的axis并指定其labels:\n", reindex)
    reindex = data_frame.reindex(["Site"], axis='columns')  # 指定列的key
    print("轴样式语法，指定索引的axis并指定其labels:\n", reindex)

    reindex = data_frame.reindex(index=[3], columns=["Age", "Site"])
    print("reindex新行标签插入确实值（NA）:\n", reindex)
    reindex = data_frame.reindex(index=[0, 2], columns=["Address"])
    print("reindex新列标签插入确实值（NA）:\n", reindex)
    reindex = data_frame.reindex(index=[3], columns=["Address"])
    print("reindex新行列标签插入确实值（NA）:\n", reindex)
    pass


def reindex_like_demo():
    df1 = pd.DataFrame({"A": [1, 5, 3, 4, 2],
                        "B": [3, 2, 4, 3, 4],
                        "C": [2, 2, 7, 3, 4],
                        "D": [4, 3, 6, 12, 7]},
                       index=["A1", "A2", "A3", "A4", "A5"])
    df2 = pd.DataFrame({"A": [10, 11, 7, 8, 5],
                        "B": [21, 5, 32, 4, 6],
                        "C": [11, 21, 23, 7, 9],
                        "D": [1, 5, 3, 8, 6]},
                       index=["A1", "A3", "A4", "A7", "A8"])
    # reindex_like的作用为生成一个横纵索引完全与参数列表一致的DataFrame，元素数据用的是调用者DataFrame的
    like = df1.reindex_like(df2)
    print("reindex_like()函数查找匹配的索引:\n", like)
    pass


if __name__ == '__main__':
    reindex_demo()
    reindex_like_demo()
    pass
