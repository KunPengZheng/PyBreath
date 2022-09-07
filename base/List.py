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
    print(list1 * 2)  # 星号 * 是重复操作，相当于两个list1使用 + 进行拼接
    print(list1 + list2)  # 加号 + 是列表连接运算符
    print(1 in list1)  # 元素是否存在于列表中
    print(len(list1))  # 列表长度

    # 迭代
    for ele in list1:
        print(ele)

    print(list1[0])  # 输出列表start元素
    print(list1[0:])  # 输出列表start及其后面的所有元素，相当于list1[0:len(list1) - 1]]
    print(list1[1:2])  # 输出start和end之前的元素
    print(list1[0:4:2])  # 输出start和end之前的元素，参数3为索引的步长，果第三个参数为负数表示逆向读取（必须配合逆向索引的角标）

    list2[3] = 10  # 修改元素
    print(list2)
    del list2[3]  # 删除元素元素
    print(list2)
    list2.append(9)  # 添加元素
    print(list2)
    list2.remove(9)  # 移除指定的value项
    pop = list2.pop(2)  # 移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
    print(pop)
    list2.reverse()  # 反向列表中元素
    print(list2)
    list2.sort()
    copy = list2.copy()
    print(f"list2的内存地址:{id(list2)}，copy的内存地址:{id(copy)}")
    list2.clear()

    # 列表比较
    a = [1, 2]
    b = [2, 3]
    c = [2, 3]
    print("operator.eq(a,b): ", operator.eq(a, b))
    print("operator.eq(c,b): ", operator.eq(c, b))

    # 返回列表元素最大值
    print(max(list1))
    # 返回列表元素最小值
    print(min(list1))
    # 统计某个元素在列表中出现的次数
    print(list1.count("4"))
    # 在列表末尾添加另外一个序列
    print(list1.extend(list2))
    # 从列表中找出某个值第一个匹配项的索引位置
    print(list1.index(1))
    # 将对象插入列表指定位置
    print(list1.insert(0, 0))


if __name__ == '__main__':
    list_demo()
    pass
