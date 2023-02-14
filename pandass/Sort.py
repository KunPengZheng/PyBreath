import pandas as pd  # as是别名的意思，相当于kotlin的as、
import numpy as np

"""
排序：
    sort_index：
        1. 参数ascending为bool类型，True为升序，False为降序，默认为True
        2. 参数axis，0表示对行标签排序，1表示对列标签排序，默认为0
    sort_values：
            
"""


def sort_index_demo():
    df = pd.DataFrame(
        {"B": [3, 2, 4, 3, 4],
         "A": [1, 5, 3, 4, 2],
         "D": [4, 3, 6, 12, 7],
         "C": [2, 2, 7, 3, 4]},
        index=["1", "4", "3", "5", "2"])
    index = df.sort_index()
    print("默认情况下，按照升序对行标签进行排序:\n", index)
    index = df.sort_index(ascending=False)
    print("ascending为false表示降序:\n", index)
    index = df.sort_index(axis=1)
    print("sort_index:\n", index)
    pass


def sort_values_demo():
    df = pd.DataFrame({"A": [1, 5, 3, 4, 2],
                       "B": [3, 2, 4, 3, 4],
                       "C": [2, 2, 7, 3, 4],
                       "D": [4, 3, 6, 12, 7]},
                      index=["A1", "A2", "A3", "A4", "A5"])
    print("df:\n", df)
    values = df.sort_values(by='A')
    print("sort_values:\n", values)
    pass


if __name__ == '__main__':
    # sort_index_demo()
    sort_values_demo()
    pass
