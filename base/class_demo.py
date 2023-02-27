"""
Python从设计之初就已经是一门面向对象的语言（因为有类的存在）

类的专有方法：
__init__ : 构造函数，在生成对象时调用
__del__ : 析构函数，释放对象时使用
__repr__ : 打印，转换
__setitem__ : 按照索引赋值
__getitem__: 按照索引获取值
__len__: 获得长度
__cmp__: 比较运算
__call__: 函数调用
__add__: 加运算
__sub__: 减运算
__mul__: 乘运算
__truediv__: 除运算
__mod__: 求余运算
__pow__: 乘方
__bool__: 判断对象是否为真，默认为真，除非这个类对__bool__或者__len__函数有自己的实现。如果不存在__bool__方法，
          那么bool(x)会尝试调用x.__len__（　）。若返回0，则bool会返回False；否则返回True。

"""

from dataclasses import dataclass


class Speaker:
    topic = ''
    name = ''

    def __init__(self, n, t):
        self.name = n
        self.topic = t

    def speak(self):
        print("我叫 %s，我是一个演说家，我演讲的主题是 %s" % (self.name, self.topic))


class People:
    # 定义基本属性，在类内部调用基本属性或者私有属性，都需要通过 self.属性名
    name = ''
    age = 0
    # 两个下划线开头，声明该属性为私有，不能在类的外部被使用或直接访问
    __weight = 0

    # __init__() 是构造方法，该方法在类实例化时会自动调用
    def __init__(self, n, a, w):
        self.name = n
        self.age = a
        self.__weight = w

    # 两个下划线开头声明的私有方法，不能在类的外部被使用或直接访问
    def __private_method(self):
        print("我是私有方法")

    # 类的方法与普通的函数只有一个特别的区别，类方法必须有一个额外的第一个参数名称, 按照惯例它的名称是 self（也可以是其他命名）。
    # self代表类的实例，而非类，代表当前对象的地址。self.变量名 = 变量值
    def speak(self):
        #  self.class 则指向类
        print(self.__class__)
        print("%s 说: 我 %d 岁。" % (self.name, self.age))


# 单继承示例，必须与父类定义在一个作用域内。
class Student(People):
    grade = ''

    def __init__(self, n, a, w, g):
        # 如果显示定义构造函数，需要手动显示调用父类的构造方法。
        People.__init__(self, n, a, w)
        self.grade = g

    # 覆写父类的方法
    def speak(self):
        # 下面几种方式都能调用到父类的方法
        # People.speak(self)
        # super(Student, self).speak()
        # super().speak()
        print("%s 说: 我 %d 岁了，我在读 %d 年级" % (self.name, self.age, self.grade))


# 多重继承
class Sample(Speaker, Student):
    def __init__(self, n, a, w, g, t):
        Student.__init__(self, n, a, w, g)
        Speaker.__init__(self, n, t)


# dataclass注解，同kotlin的数据类作用一致，强调数据（即属性）在构造的时候就应该确定值
@dataclass
class DataClassDemo:
    x: int
    y: int

    # 普通方法，默认有个self参数，且只能被对象调用。
    def add(self):
        print("普通方法:", self.x + self.y)

    # 用 @staticmethod 装饰的不带 self 参数的方法叫做静态方法，类的静态方法可以没有参数，可以直接使用类名调用。
    @staticmethod
    def static_method():
        print("静态方法")

    # 类方法: 默认有个 cls 参数，可以被类和对象调用，需要加上 @classmethod 装饰器。
    @classmethod
    def cls_method(cls):
        print("类方法:", cls)


# 全局变量
global_num = 1

def global_demo():
    """
    global关键字可以用在任何地方，包括最上层函数和嵌套函数中，即使之前未定义该变量，global修饰后也可以直接使用
    global关键字修饰变量后标识该变量是全局变量，对该变量进行修改就是修改全局变量
    """

    # local variable 'global_num' referenced before assignment。
    # 局部作用域引用错误，因为 global_demo 函数中的 global_num 使用的是局部，未定义，无法修改。
    # global_num = global_num + 1

    # 解决：1.将global_num声名为局部变量并在使用前赋值； 2. 在变量前使用global关键字（当内部作用域想修改外部作用域的变量时）
    global global_num
    global_num = global_num + 1
    print(global_num)


def nonlocal_demo():
    """
    nonlocal关键字只能用于嵌套函数中，并且外层函数需定义了相应的局部变量（外层中的同名变量若是全局变量也会报错），否则会发生错误。
    nonlocal关键字修饰变量后标识该变量是上一级函数中的局部变量，一般在嵌套函数中使用。对该变量进行修改也会同时修改其引用的上一级函数的局部变量。
    如果上一级函数中不存在该局部变量，nonlocal位置会发生错误（最上层的函数使用nonlocal修饰变量必会报错）
    """

    nonlocal_num = 10

    def inner_demo():
        nonlocal nonlocal_num
        nonlocal_num = 5

    print("nonlocal_num:", nonlocal_num)
    inner_demo()
    print("nonlocal_num:", nonlocal_num)


if __name__ == '__main__':
    sample = Sample("Tim", 25, 80, 4, "Python")
    sample.speak()  # 方法名同，默认调用的是在括号中参数位置排前父类的方法

    student = Student("Tim", 25, 80, 4)
    student.speak()
    # super调用父类的方法
    super(Student, student).speak()

    dataClassDemo = DataClassDemo(1, 2)
    # 对象调用普通方法
    dataClassDemo.add()
    # 对象或类调用类方法
    dataClassDemo.cls_method()
    DataClassDemo.cls_method()
    # 类名调用静态方法
    DataClassDemo.static_method()

    global_demo()
    nonlocal_demo()
    pass
