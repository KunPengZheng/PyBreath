"""

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

"""


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


if __name__ == '__main__':
    sample = Sample("Tim", 25, 80, 4, "Python")
    sample.speak()  # 方法名同，默认调用的是在括号中参数位置排前父类的方法

    student = Student("Tim", 25, 80, 4)
    student.speak()
    # super调用父类的方法
    super(Student, student).speak()
    pass
