"""
1. Python 中的变量不需要声明类型。每个变量在使用前都必须赋值，变量赋值以后该变量才会被创建。
2. 在 Python 中，变量就是变量，它没有类型，我们所说的"类型"是变量所指的内存中的对象的类型。
    > 类型属于对象，对象有不同类型的区分，变量是没有类型的(仅仅是一个对象的引用（一个指针）)。
3. 等号（=）用来给变量赋值。左边是一个变量名，右边是存储在变量中的值。
4. strings, tuples, 和 numbers 是不可更改的对象(immutable)，而 list,dict，set 则是可以修改的对象(mutable)。
    > 不可变类型：变量赋值 a=5 后再赋值 a=10，这里实际是新生成一个 int 值对象 10，再让 a 指向它，而 5 被丢弃，不是改变 a 的值，相当于新生成了 a。
    > 可变类型：变量赋值 la=[1,2,3,4] 后再赋值 la[2]=5 则是将 list la 的第三个元素值更改，本身la没有动，只是其内部的一部分值被修改了。
5. python 函数的参数传递：
    > 不可变类型：类似 C++ 的值传递，如整数、字符串、元组。如 fun(a)，传递的只是 a 的值，没有影响 a 对象本身。如果在 fun(a) 内部修改 a 的值，则是新生成一个 a 的对象。
    > 可变类型：类似 C++ 的引用传递，如 列表，字典。如 fun(la)，则是将 la 真正的传过去，修改后 fun 外部的 la 也会受影响
"""


def print_data_type():
    int_var = 1  # 整型变量
    float_var = 1.0  # 浮点型变量
    str_var = "字符串"  # 字符串
    print(int_var)
    print(float_var)
    print(str_var)


def mutable_immutable():
    # 不可变类型，修改后内存地址发生改变
    a = "1"
    print(id(a))
    a = "2"
    print(id(a))

    # 可变类型，修改后内存地址不发生改变
    list1 = [1, 2, 3]
    print(id(list1))
    list1.append(4)
    print(id(list1))

    set1 = {1, 2, 3}
    print(id(set1))
    set1.add(4)
    print(id(set1))
    pass


"""
Python3 有 int、float、bool、complex（复数）等基本类型。
赋值，Python允许你同时为多个变量赋值（赋值对象）
"""


def assignment():
    a = b = c = 1
    a1, b1, c1 = 1, 2.0, "runoob"


class A:
    # pass是空语句，是为了保持程序结构的完整性。pass 不做任何事情，一般用做占位语句。
    pass


class B(A):
    pass


"""
isinstance 和 type 的区别在于：
1. type()不会认为子类是一种父类类型。type() 函数可以用来查询变量所指的对象的类型
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
条件语句
1、每个条件后面要使用冒号":" ，表示接下来是满足条件后要执行的语句块。
2、使用缩进来划分语句块，相同缩进数的语句在一起组成一个语句块。
3、在Python中没有switch – case语句。
4、 Python 中用 elif 代替了 else if，简化写法
"""


def if_else():
    ele = 3
    if ele > 0:
        print(">0")
    elif ele < 0:
        print("<0")
    else:
        print("==0")


def line_break():
    """
    换行，表达式太长想要换行，如果直接换行会报错。使用以下方式表示连接
    1.加反斜杠（推荐）
    2.添加括号()
    """
    c = "aaaaaa{}" \
        .format("1")
    print(c, type(c))
    c = ("aaaaaa{}"
         .format("2"))
    print(c, type(c))
    pass


if __name__ == '__main__':
    # print_data_type()
    # assignment()
    # deleteReference()
    # type_isinstance()
    # if_else()
    # mutable_immutable()
    line_break()
    pass
