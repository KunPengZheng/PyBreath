"""
Python 中的变量不需要声明类型。每个变量在使用前都必须赋值，变量赋值以后该变量才会被创建。
在 Python 中，变量就是变量，它没有类型，我们所说的"类型"是变量所指的内存中对象的类型。
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


# 赋值
def assignment():
    # Python允许你同时为多个变量赋值
    a = b = c = 1
    # 为多个对象指定多个变量
    a1, b1, c1 = 1, 2.0, "runoob"


"""
Python3 支持 int、float、bool、complex（复数）。
在Python 3里，只有一种整数类型 int，表示为长整型，没有 python2 中的 Long。
像大多数语言一样，数值类型的赋值和计算都是很直观的。
内置的 type() 函数可以用来查询变量所指的对象类型。
"""


def number():
    a, b, c, d = 20, 5.5, True, 4 + 3j
    print(type(a), type(b), type(c), type(d))
    # isinstance 和 type 的区别在于：
    # 1. type()不会认为子类是一种父类类型。
    # 2. isinstance()会认为子类是一种父类类型。
    print(isinstance(a, int))

    print(type(A()) == A)
    print(type(A()) == A)


class A:
    pass


class B(A):
    pass


if __name__ == '__main__':
    print_data_type()
