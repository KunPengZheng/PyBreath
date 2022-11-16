"""
1. 元组（tuple）与列表类似，不同之处在于元组的元素不能修改，虽然tuple的元素不可改变（包括删除），但它可以包含可变的对象，比如list列表
2. 元组写在小括号 () 里，元素之间用逗号隔开。
3. 元组中的元素类型也可以不相同
4. string、list 和 tuple 都属于 sequence（序列）。
"""


def tuple_demo():
    tuple1 = (1, 2.0, "3")
    tuple2 = ()  # 空元组
    tuple3 = (20,)  # 一个元素，需要在元素后添加逗号，表示类型为元组
    tuple3 = (20,)  # 不加逗号，类型为整型
    # Tuples don't support item assignment
    # tuple3[0] = 1


if __name__ == '__main__':
    tuple_demo()
    pass
