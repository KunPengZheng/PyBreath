import operator


# 算数运算符
def arithmetic_demo():
    print(2 ** 3)  # 返回x的y次平方
    # // 对商向下取整， 得到的并不一定是整数类型的数，它与分母分子的数据类型有关系。
    print(7 // 2)  # 3
    print(7.0 // 2)  # 3.0
    print(7 // 2.0)  # 3.0


# 赋值运算符
def assign_demo():
    str = "abc"
    # ":=" 是 python3.8 的新特性，该符号又称为"海象运算符"。就是语法糖
    # :=可将值分配给变量，又作为表达式的一部分，使赋值和判断，两步合成一步，让代码变得更简洁。
    if n := len(str) > 5:
        print(n)
    # 👆的写法相当于下面
    n1 = len(str)
    if n1 > 5:
        print(n1)


# 逻辑运算符
def logic_demo():
    a = True
    b = False
    print(a and b)
    print(a or b)
    print(not a)


# 成员运算符
def in_demo():
    list1 = [1, 2, 3, 4, 5]
    # in 一般用于序列，在序列中能找到指定的元素，则返回True，反之False
    print(1 in list1)
    # not in 一般用于序列，指定的元素是否不在序列中，不在则返回True，反之False
    print(1 not in list1)


# 身份运算符
def is_demo():
    a = 20
    b = 20
    # is 是判断两个标识符是不是引用自一个对象，即内存地址是否相同
    # is not 是判断两个标识符是不是引用自不同对象
    if a is b:
        print("内存地址一样")
    else:
        print("内存地址不一样")
    # 从 python 3.8 开始，使用 is 和 is not 运算符时，会抛出 SyntaxWarning 语句警告信息,将对应语句中is/is not用== 和 != 代替
    print(a == b)
    #  id() 函数用于获取对象内存地址
    print(id(a))


def operator_module():
    """
    Python2.x 版本中，使用 cmp() 函数来比较两个列表、数字或字符串等的大小关系。
    Python 3.X 的版本中已经没有 cmp() 函数，如果你需要实现比较功能，需要引入 operator 模块，适合任何对。

    更多的函数：https://www.runoob.com/python3/python-operator.html
    """
    # 数字
    x = 10
    y = 20
    print("x:", x, ", y:", y)
    print("operator.lt(x,y): ", operator.lt(x, y))  # 与 a < b 相同
    print("operator.gt(y,x): ", operator.gt(y, x))  # 与 a > b 相同
    print("operator.eq(x,x): ", operator.eq(x, x))  # 与 a == b 相同
    print("operator.ne(y,y): ", operator.ne(y, y))  # 与 a != b 相同
    print("operator.le(x,y): ", operator.le(x, y))  # 与 a <= b 相同
    print("operator.ge(y,x): ", operator.ge(y, x))  # 与 a >= b 相同

    # 初始化变量
    a = 4
    b = 3

    # 使用 add() 让两个值相加
    print("add() 运算结果 :", end="")
    print(operator.add(a, b))
    # 使用 sub() 让两个值相减
    print("sub() 运算结果 :", end="")
    print(operator.sub(a, b))
    # 使用 mul() 让两个值相乘
    print("mul() 运算结果 :", end="")
    print(operator.mul(a, b))
    pass


if __name__ == '__main__':
    # arithmetic_demo()
    # assign_demo()
    # logic_demo()
    # in_demo()
    is_demo()
    operator_module()
    pass
