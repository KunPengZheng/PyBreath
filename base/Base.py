"""
Python 中的变量不需要声明类型。每个变量在使用前都必须赋值，变量赋值以后该变量才会被创建。
在 Python 中，变量就是变量，它没有类型，我们所说的"类型"是变量所指的内存中的对象的类型。
等号（=）用来给变量赋值。
等号（=）运算符左边是一个变量名,等号（=）运算符右边是存储在变量中的值。
"""


def print_data_type():
    int_var = 1  # 整型变量
    float_var = 1.0  # 浮点型变量
    str_var = "字符串"  # 字符串
    print(int_var)
    print(float_var)
    print(str_var)


"""
Python3 有 int、float、bool、complex（复数）等基本类型。
赋值，Python允许你同时为多个变量赋值（赋值对象）
"""


def assignment():
    a = b = c = 1
    a1, b1, c1 = 1, 2.0, "runoob"


class A:
    pass


class B(A):
    pass


"""
isinstance 和 type 的区别在于：
1. type()不会认为子类是一种父类类型。type() 函数可以用来查询变量所指的对象类型
2. isinstance()会认为子类是一种父类类型。
"""


def type_isinstance():
    # true
    print(isinstance(B(), A))
    # false
    print(type(B()) == A)


"""
del语句删除单个或多个对象的引用
"""


def deleteReference():
    var1 = 10
    del var1
    # UnboundLocalError: local variable 'var1' referenced before assignment 未绑定的本地错误，表示使用变量前之前要赋值
    print(var1)


"""
1. 列表是有序的对象集合，字典是无序的对象集合。两者之间的区别在于：字典当中的元素是通过键来存取的，而不是通过偏移存取。
2. 字典的关键字必须为不可变类型，且不能重复。
3. 字典是一种映射类型，它的元素是键值对。
4. 创建空字典使用 { }。
"""


def dictionary_demo():
    dic1 = {}  # 空字典
    dic1["1"] = "1"
    dic1[2] = 2
    print(dic1)
    dic2 = {"1": 1, 2: 2}
    print(dic2)
    print(dic2["1"])  # 获取key为"1"的value
    print(dic2[2])  # 获取key为2的value
    print(dic2.keys())  # 获取所有的key
    print(dic2.values())  # 获取所有的value


if __name__ == '__main__':
    # print_data_type()
    # assignment()
    # deleteReference()
    # type_isinstance()
    # number_demo()
    # string_demo()
    # list_demo()
    # tuple_demo()
    # set_demo()
    dictionary_demo()
