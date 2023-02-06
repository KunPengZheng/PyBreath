"""
1. 列表是有序的对象集合，字典是无序的对象集合。两者之间的区别在于：字典当中的元素是通过键来存取的，而不是通过偏移存取。
2. 字典的关键字必须为不可变类型，且不能重复。键必须不可变，所以可以用数字，字符串或元组充当，而用列表就不行
3. 字典是一种映射类型，它的元素是键值对。
4. 创建空字典使用 { }。
"""


def dictionary_demo():
    dic1 = {}  # 空字典
    dic1["1"] = "1"  # 添加
    dic1[2] = 2
    dic1[3] = 3
    del dic1["1"]  # 删除元素
    print(dic1)
    print(dic1.pop(2))  # 删除字典 key（键）所对应的值，返回被删除的值。
    print(dic1.popitem())  # 删除并返回字典中的最后一对键和值。

    dic2 = {"1": 1, 2: 2}
    print(dic2)

    # 如果关键字只是简单的字符串，使用关键字参数指定键值对有时候更方便
    print(dict(sape=4139, guido=4127, jack=4098))

    print(dic2["1"])  # 获取key为"1"的value，相当于dict.get(key, default=None)
    print(dic2.get("1"))
    print(dic2.setdefault("3", 2))  # 和get()类似, 但如果键不存在于字典中，将会添加键并将值设为default

    print(dic2.keys())  # 获取所有的key，以列表返回一个视图对象
    print(dic2.values())  # 获取所有的value，以列表返回一个视图对象
    print(dic2.items())  # 以列表返回一个视图对象
    print(dic2.fromkeys((1, 2, 3, 4)))  # 创建一个新字典，以序列seq中元素做字典的键，val为字典所有键对应的初始值

    dic3 = {"a": 1, "b": 2}
    dic4 = {"c": 3, "d": 4}
    dic3.update(dic4)  # 把字典dict2的键/值对更新到dict里。相当于列表的"+"操作运算符
    print(dic3)

    # 遍历获取key和value
    for k, v in dic3.items():
        print(k, v)


def convert_demo():
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
    dictionary_demo()
    convert_demo()
