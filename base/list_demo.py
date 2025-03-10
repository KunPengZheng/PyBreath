"""
1.列表中元素的类型可以不相同，它支持数字，字符串甚至可以包含列表（所谓嵌套）
2.列表是写在方括号 [] 之间、用逗号分隔开的元素列表。
3.索引规则和字符串一样
3.列表中的元素是可以改变的
4.可以将列表作为堆栈（后进先出），队列（先进先出）等数据结构使用。
"""
import operator


def list_demo():
    list1 = [1, 2, 3.0, "4", "5"]
    list2 = [6, 7, 8, 9]

    print(list1)  # 输出列表
    print("* 运算符:", list1 * 2)  # 星号 * 是重复操作，相当于两个list1使用 + 进行拼接
    print("+ 运算符:", list1 + list2)  # 加号 + 是列表连接运算符，相当于extend()
    print("in:", 1 in list1)  # 元素是否存在于列表中
    print("len:", len(list1))  # 列表长度

    # 迭代
    for ele in list1:
        print(ele)

    print(list1[0])  # 输出列表start元素
    print("start:", list1[0:])  # 输出列表start及其后面的所有元素，相当于list1[0:len(list1) - 1]]
    print("start和end:", list1[1:2])  # 输出start和end之前的元素
    print("start和end和步长:", list1[0:4:2])  # 输出start和end之前的元素，参数3为索引的步长，果第三个参数为负数表示逆向读取（必须配合逆向索引的角标）

    list2[3] = 10  # 修改元素
    print("修改元素:", list2)
    del list2[3]  # 删除元素
    print("删除元素:", list2)
    list2.append(9)  # 添加元素
    print("添加元素:", list2)
    list2.remove(9)  # 移除指定的元素
    print("移除指定的元素:", list2)
    pop = list2.pop(2)  # 移除指定角标的元素并返回该元素，无指定角标则默认最后一个元素
    print("pop移除指定角标的元素并返回该元素:", pop)
    list2.reverse()  # 反向列表中元素
    print("reverse:", list2)
    list2.sort()  # 自然顺序排序
    print("sort:", list2)
    copy = list2.copy()  # 浅拷贝
    print(f"list2的内存地址:{id(list2)}，copy的内存地址:{id(copy)}")
    list2.clear()  # 清空
    print("clear:", list2)

    # 列表比较，比较内容
    a = [1, 2]
    b = [2, 3]
    c = [2, 3]
    print("operator.eq(a,b): ", operator.eq(a, b))
    print("operator.eq(c,b): ", operator.eq(c, b))

    max_min_list = [1, 2, 3, 4]
    # 返回列表元素最大值
    print("返回列表元素最大值:", max(max_min_list))
    # 返回列表元素最小值
    print("返回列表元素最小值:", min(max_min_list))

    # 统计某个元素在列表中出现的次数
    print("统计某个元素在列表中出现的次数:", list1.count("4"))
    # 在列表末尾添加另外一个序列，相当于 + 运算符
    list1.extend(list2)
    # 从列表中找出某个值第一个匹配项的索引位置
    print("从列表中找出某个值第一个匹配项的索引位置:", list1.index(1))
    # 将对象插入列表指定位置
    list1.insert(0, 0)

    del_list = [-1, 1, 66.25, 333, 333, 1234.5]
    del del_list[0]  # 删除指定角标的元素
    del del_list[2:4]  # 删除指定范围的元素
    del del_list[:]  # clean
    del del_list  # 删除变量

    # reversed()反序
    reversed_list = [1, 2, 3]
    r = reversed(reversed_list)
    for i in r:
        print(i)

    # sorted() 函数按照自然顺序返回一个已排序的序列
    sorted_list = [3, 2, 1]
    for f in sorted(sorted_list):
        print(f)


if __name__ == '__main__':
    list_demo()
    pass
