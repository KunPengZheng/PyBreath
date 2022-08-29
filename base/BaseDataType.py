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


def number_demo():
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
def string_demo():
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


"""
1.列表中元素的类型可以不相同，它支持数字，字符串甚至可以包含列表（所谓嵌套）
2.列表是写在方括号 [] 之间、用逗号分隔开的元素列表。
3.索引规则和字符串一样
3.列表中的元素是可以改变的
"""


def list_demo():
    list1 = [1, 2, 3.0, "4", "5"]
    list2 = [6]
    print(list1)  # 输出列表
    print(list1 * 2)  # 输出列表两次，星号 * 是重复操作
    print(list1 + list2)  # 加号 + 是列表连接运算符
    print(list1[0])  # 输出列表start元素
    print(list1[0:])  # 输出列表start及其后面的所有元素，相当于list1[0:len(list1) - 1]]
    print(list1[1:2])  # 输出start和end之前的元素
    print(list1[0:4:2])  # 输出start和end之前的元素，参数3为索引的步长，果第三个参数为负数表示逆向读取（必须配合逆向索引的角标）
    list2[0] = 7  # 修改元素
    print(list2)


"""
1. 元组（tuple）与列表类似，不同之处在于元组的元素不能修，虽然tuple的元素不可改变，但它可以包含可变的对象，比如list列表
2. 元组写在小括号 () 里，元素之间用逗号隔开。
3. 元组中的元素类型也可以不相同
4. string、list 和 tuple 都属于 sequence（序列）。
"""


def tuple_demo():
    tuple1 = (1, 2.0, "3")
    tuple2 = ()  # 空元组
    tuple3 = (20,)  # 一个元素，需要在元素后添加逗号
    # Tuples don't support item assignment
    # tuple3[0] = 1


"""
1.元素不重复（和java的set是一样的）
2.可以使用大括号 { } 或者 set() 函数创建集合，()创建的集合只能包含一个元素
3.创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典。
"""


def set_demo():
    set1 = {1, 2.0, "3"}
    set2 = set("2")  # ()创建的集合只能包含一个元素
    set3 = set()  # 空集合
    print(set1)
    print(set3)
    # 使用in关键字测试元素是否在指定set中
    if 'Runoob' in set1:
        print('Runoob 在集合中')
    else:
        print('Runoob 不在集合中')
    # set可以进行集合运算
    a = set('abracadabra')
    b = set('alacazam')
    print(a - b)  # a 和 b 的差集
    print(a | b)  # a 和 b 的并集
    print(a & b)  # a 和 b 的交集
    print(a ^ b)  # a 和 b 中不同时存在的元素


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
