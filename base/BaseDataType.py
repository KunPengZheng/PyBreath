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
    # Python允许你同时为多个变量赋值（赋值对象）
    a = b = c = 1
    a1, b1, c1 = 1, 2.0, "runoob"


class A:
    pass


class B(A):
    pass


"""
isinstance 和 type 的区别在于：
1. type()不会认为子类是一种父类类型。
2. isinstance()会认为子类是一种父类类型。
"""


def type_isinstance():
    # true
    print(isinstance(B(), A))
    # false
    print(type(B()) == A)


# del语句删除单个或多个对象
def deleteReference():
    var1 = 10
    del var1
    # UnboundLocalError: local variable 'var1' referenced before assignment 未绑定的本地错误，表示使用变量前之前要赋值
    print(var1)


"""
Python3 支持 int、float、bool、complex（复数）。
在Python 3里，只有一种整数类型 int，表示为长整型，没有 python2 中的 Long。
像大多数语言一样，数值类型的赋值和计算都是很直观的。
内置的 type() 函数可以用来查询变量所指的对象类型。
"""


def number():
    a, b, c, d = 20, 5.5, True, 4 + 3j
    # <class 'int'> <class 'float'> <class 'bool'> <class 'complex'>
    print(type(a), type(b), type(c), type(d))
    print(isinstance(a, int))

    # 在 Python2 中是没有布尔型的，它用数字 0 表示 False，用 1 表示 True。
    # Python3 中，bool 是 int 的子类，True 和 False 可以和数字相加， True==1、False==0 会返回 True
    # 从 python 3.8 开始，使用 is 和 is not 运算符时，会抛出 SyntaxWarning 语句警告信息,将对应语句中is/is not用== 和 != 代替
    issubclass(bool, int)
    print(True == 1)
    print(False == 0)

    # 当你指定一个值时，Number 对象就会被创建，您也可以使用del语句删除一些对象引用。
    var1 = 1
    var2 = 10
    print(var1)
    print(var2)
    del var1, var2

    # 数值的除法包含两个运算符：/ 返回一个浮点数，// 返回一个整数。
    print(2 / 4)  # 0.5
    print(2 // 4)  # 0

    # 数值的乘法包含两个运算符：* 表示乘法，**表示乘方
    print(3 * 7)  # 21
    print(2 ** 5)  # 32


# 注意，Python 没有单独的字符类型，一个字符就是长度为1的字符串。
def string():
    # Python中的字符串用单引号' 或双引号 " 括起来，同时使用反斜杠 \ 转义特殊字符。
    # Python 字符串不能被改变。向一个索引位置赋值，比如str[0] = 'm'会导致错误。
    str = 'Runoob'
    # 字符串的截取的语法格式如下：变量[头下标:尾下标]，索引值以 0 为从左向右的开始位置，-1 为从右向左的开始位置。
    print(str[0:6])  # 和java一样，包头不包尾
    print(str[0:-1])  # 只有end可以是负数，str[-1,-6]无效
    print(str[0:])  # 从0开始到所有结束，相当于[0,str的字符串长度]
    print(str * 2)  # 输出字符串两次，也可以写成 print (2 * str)
    print(str + "TEST")  # 连接字符串
    print('Ru\noob')  # 使用反斜杠 \ 转义特殊字符
    print(r'Ru\noob')  # 如果你不想让反斜杠发生转义，可以在字符串前面添加一个 r，表示原始字符串


if __name__ == '__main__':
    # print_data_type()
    # assignment()
    # deleteReference()
    type_isinstance()
    number()
    string()
