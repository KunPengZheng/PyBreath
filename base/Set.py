"""
1.元素不重复（和java的set是一样的）
2.可以使用大括号 { } 或者 set() 函数创建集合，set()创建的集合只能包含一个元素
3.创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典。
4.set的元素是唯一的，即哈希表类型(hashable)类型，因此元素必须是不可变类型
"""


def set_demo():
    set1 = {1, 2.0, "3"}
    set2 = set("2")  # ()创建的集合只能包含一个元素
    set3 = set()  # 空集合
    print(set1)
    print(set2)
    print(set3)

    # 使用in关键字测试元素是否在指定set中
    if 'Runoob' in set1:
        print('Runoob 在集合中')
    else:
        print('Runoob 不在集合中')

    for x in set1:
        print("for遍历:", x)

    # set可以进行集合运算
    a = set('abracadabra')
    b = set('alacazam')
    print("差集:", a - b)  # a 和 b 的差集，difference()；difference_update()会将符合结果的元素在目标集合集合中移除
    print("并集:", a | b)  # a 和 b 的并集，union()
    print("交集:", a & b)  # a 和 b 的交集，intersection()；intersection_update()
    print("不同时存在的元素:", a ^ b)  # a 和 b 中不同时存在的元素，symmetric_difference()；symmetric_difference_update()

    # 添加元素
    set1.add("4")
    # 添加元素2，参数可以是列表，元组，字典等，即序列。
    set1.update("x")
    # 移除元素，移除后获取不存在的元素会发生错误
    set1.remove("4")
    # 移除元素2，移除后获取不存在的元素会发生错误
    set1.discard("x")
    # 随机删除集合中的一个元素，pop 方法会对集合进行无序的排列，然后将这个无序排列集合的左边第一个元素进行删除。（这方法鸡肋）
    set1.pop()
    # 清空集合
    set1.clear()

    # 两个集合没有包含相同元素则返回true，否则返回false
    set1.isdisjoint(set2)
    # 用于判断集合(调用者)的所有元素是否都包含在指定集合（参数）中，如果是则返回 True，否则返回 False。
    set1.issubset(set2)
    # 用于判断集合(参数)的所有元素是否都包含在指定集合（调用者）中，如果是则返回 True，否则返回 False。
    set1.issuperset(set2)


if __name__ == '__main__':
    set_demo()
    pass
