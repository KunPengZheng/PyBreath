import pandas as pd  # as是别名的意思，相当于kotlin的as、
import numpy as np

"""
函数应用：不管是为 Pandas 对象应用自定义函数，还是应用第三方函数，都离不开以下三种方法(简单的说就是👇三种函数都能接受外部的自定义
或者第三方函数作为参数传入)。用哪种方法取决于操作的对象是DataFrame，还是 Series ；是行、列，还是元素（根据操作对象的不同选择下面的函数）。
    1.表级函数应用：pipe()，可以通过将函数和适当数量的参数作为管道参数来执行自定义操作，从而对整个DataFrame执行操作。
    2.行列级函数应用： apply()，行列批量处理，它与描述性统计方法一样使用一个可选的axis参数。
    3.元素级函数应用：applymap()，和Series上的map()类似，接受任何Python函数，该函数要求能够接受单个值并返回单个值。
"""


def adder(ele1, ele2):
    return ele1 + ele2


def pipe_demo():
    dictionary = {'Site': [1, 2, 3], 'Age': [10, 12, 13]}
    data_frame = pd.DataFrame(dictionary)
    # adder有两个参数，参数1默认传递的是DataFrame的元素，参数2是外部传入的
    pipe = data_frame.pipe(adder, 2)
    print("pipe:\n", pipe)


def apply_demo():
    dictionary = {'Site': [1, 2, 3], 'Age': [10, 12, 13]}
    data_frame = pd.DataFrame(dictionary)
    # axis默认为0，计算列；如果为1则计算行
    apply = data_frame.apply(np.sum, axis=1)
    print("apply:\n", apply)
    pass


def map_demo():
    dictionary = {'Site': [1, 2, 3], 'Age': [10, 12, 13]}
    data_frame = pd.DataFrame(dictionary)
    site__map = data_frame['Site'].map(lambda x: x * 100)
    print("map:\n", site__map)
    applymap = data_frame.applymap(lambda x: x * 100)
    print("applymap:\n", applymap)
    pass


if __name__ == '__main__':
    pipe_demo()
    apply_demo()
    map_demo()
    pass
