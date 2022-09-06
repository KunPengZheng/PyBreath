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


if __name__ == '__main__':
    dictionary_demo()
