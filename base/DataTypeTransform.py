"""
数据类型转换：
1.隐式类型转换 - 自动完成
2.显式类型转换 - 需要使用类型函数来转换
"""
from datetime import datetime


class DataTypeClass:
    def __repr__(self):
        return "重写DataTypeClass的__repr__方法"


def hide_transform():
    num_int = 1
    num_float = 1.0
    print(num_int + num_float)
    pass


def show_transform():
    # int() 强制转换为整型
    float_to_int = int(1.0)
    str_to_int = int("1")
    print(float_to_int)
    print(str_to_int)

    # float() 强制转换为浮点型
    int_to_float = float(1)
    str_to_float = float("1")
    print(int_to_float)
    print(str_to_float)

    # str() 强制转换为字符串类型
    int_to_str = str(1)
    float_to_str = str(1.0)
    print(int_to_str)
    print(float_to_str)

    # repr调用的其实就对象所属类的专有方法__repr__
    # 1. str()和repr()输出的都是 str 类型，但repr()对str的处理不同，repr外层多了一层引号。
    # 2. print方法也会调用到对象所属类的专有方法__repr__
    # 3. str一般用于给人看的，而repr是给解析器也就是机器看的。一般用于打印日志的时使用str
    print(repr("1"))
    print(repr(1))
    now = datetime.now()
    print(str(now))
    print(repr(now))
    print(repr(DataTypeClass()))
    print(DataTypeClass())

    # eval() 函数用来执行一个字符串表达式，并返回表达式的值
    eval1 = eval("2+2")
    x = 7
    eval2 = eval("2 * x")
    y = "ss"
    eval3 = eval("2 * y")  # y是字符串，连续输出两次
    print(eval1)
    print(eval2)
    print(eval3)

    list1 = [1, 2.0, "3"]
    tuple1 = (1, 2.0, "3")
    set1 = {1, 2.0, "3"}
    dic1 = {"1": 1, "2": 2}

    # list，tuple，set用法相似
    seq_to_list = list("Hello World")
    list_to_list = list(list1)
    tuple_to_list = list(tuple1)
    set_to_list = list(set1)
    dic_to_list = list(dic1)
    print(seq_to_list)
    print(list_to_list)
    print(tuple_to_list)
    print(set_to_list)
    print(dic_to_list)  # 输出的是key

    # 空字典
    empty_dict = dict()
    # 只使用关键字参数创建字典。虽然报红，但是可以运行
    kwargs_dict = dict(a=1, b=2)
    print(kwargs_dict)
    # 使用可迭代对象创建字典(推荐)
    zip_demo()
    z = zip(['one', 'two', 'three'], [1, 2, 3])
    print(dict(z))
    # 使用映射来创建字典。映射类型（Mapping Types）是一种关联式的容器类型，它存储了对象与对象之间的映射关系。(推荐)
    pair1 = ('one', 1)  # Pair是映射类型
    pair2 = ('two', 2)
    pair3 = ('three', 3)
    tuple_pair = (pair1, pair2, pair3)
    print(dict(tuple_pair))

    # 转换为不可变的set。返回一个冻结的集合，冻结后集合不能再添加或删除任何元素。
    f = frozenset(set1)

    # chr() 用一个范围在 (0～255，可以是10进制也可以是16进制的形式的数字）整数作参数，返回一个对应的ASCII 字符。
    int_to_char = chr(100)
    # 和chr相反
    char_to_int = ord(int_to_char)
    print(int_to_char)
    print(char_to_int)

    # 将一个整数转换为一个十六进制字符串
    print(hex(10))
    # 将一个整数转换为一个八进制字符串
    print(oct(10))

    pass


def zip_demo():
    """
    zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象，这样做的好处是节约了不少的内存。
    可以使用 list() 转换来输出列表。
    如果各个迭代器的元素个数不一致，则返回列表长度与最短的对象相同，利用 * 号操作符，可以将元组解压为列表。
    """
    a = [1, 2, 3]
    b = [4, 5, 6]
    c = [4, 5, 6, 7, 8]
    print(list(zip(a, b)))  # 打包为元组的列表
    print(list(zip(a, c)))  # 元素个数与最短的列表一致
    a1, a2 = zip(*zip(a, b))  # 与 zip 相反，zip(*) 可理解为解压，返回二维矩阵式
    print(list(a1))
    print(list(a2))
    pass


if __name__ == '__main__':
    hide_transform()
    show_transform()
