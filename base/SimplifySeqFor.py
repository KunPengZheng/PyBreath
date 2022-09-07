"""
推导式就是一个数据序列构建成另一个新的序列。简单说就是for遍历加自定义逻辑的语法糖简化写法，构建新的序列。

1.Sequence可以是任何类型的序列
2.生成的序列类型是根据推导式来的，只有tuple推导式返回的是生成器对象，需要借助tuple(生成器对象)转换；其余都是返回对应类型
3.推倒式格式就只有最外层的符号不同而已，其余相同
4.推导式可以使用复杂表达式或嵌套函数
"""

"""
列表推导式格式为：
1. [expression for item in Sequence] 
2. [expression for item in Sequence if conditional]

参数解析：
expression：列表的元素的表达式，可以是有返回值的函数。（步骤3）
for item in Sequence：迭代 Sequence 将 item 传入到 expression 表达式中。（步骤1）
if condition：条件语句，可以过滤列表中不符合条件的值。（步骤2）
"""


def list_simplify():
    list1 = ['Bob', 'Tom', 'alice', 'Jerry', 'Wendy', 'Smith']
    list2 = [ele.upper() for ele in list1 if len(ele) > 3]
    print(list2)

    # 同时for两个列表的示例
    vec1 = [2, 4, 6, 7]
    vec2 = [4, 3, -9]
    print([x * y for x in vec1 for y in vec2])
    # 相当于👇的逻辑
    # for x in vec1:
    #     for y in vec2:
    #         print(x * y)

    #


"""
元组推导式格式为：
1.(expression for item in Sequence )
2.(expression for item in Sequence if conditional)

元组推导式和列表推导式的用法也完全相同，只是元组推导式是用 () 圆括号将各部分括起来，而列表推导式用的是中括号 []，另外元组推导式返
回的结果是一个生成器对象。
"""


def tuple_simplify():
    tuple1 = ('Bob', 'Tom', 'alice', 'Jerry', 'Wendy', 'Smith')
    tuple2 = (ele.upper() for ele in tuple1 if len(ele) > 3)
    print(tuple2)  # 返回的是生成器对象
    print(tuple(tuple2))  # 使用 tuple() 函数，可以直接将生成器对象转换成元组


"""
set集合推导式格式为：
1.{ expression for item in Sequence }
2.{ expression for item in Sequence if conditional }
"""


def set_simplify():
    set1 = {1, 2, 3}
    set2 = {ele ** 2 for ele in set1}
    print(set2)  # 返回的是生成器对象


"""
{ key_expr: value_expr for value in collection }
{ key_expr: value_expr for value in collection if condition }
"""


def dictionary_simplify():
    list1 = ['Google', 'Runoob', 'Taobao']
    # 使用字符串和字符串的长度组成键值对
    dictionary1 = {ele: len(ele) for ele in list1}
    print(dictionary1)

    # 以三个数字为键，三个数字的平方为值来创建字典
    dictionary2 = {ele: ele ** 2 for ele in (1, 2, 3)}
    print(dictionary2)
    pass


if __name__ == '__main__':
    list_simplify()
    # tuple_simplify()
    # set_simplify()
    # dictionary_simplify()
