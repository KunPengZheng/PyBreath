import random

"""
Python 支持三种不同的数值类型：
1.整型(int)：
            Python3 整型是没有限制大小的，可以当作 Long 类型使用，所以 Python3 没有 Python2 的 Long 类型；
            布尔(bool)是整型的子类，在 Python2 中是没有布尔型的，它用数字 0 表示 False，用 1 表示 True。
            可以使用十六进制和八进制来代表整数。
2.浮点型(float)：浮点型也可以使用科学计数法表示（2.5e2 = 2.5 x 100 = 250。注意：在不同的机器上浮点运算的结果可能会不一样。
3.复数(complex)：复数由实数部分和虚数部分构成，可以用a + bj，或者complex(a,b)表示， 复数的实部a和虚部b都是浮点型。
"""


def number_demo():
    a, b, c, d = 20, 5.5, True, 4 + 3j

    # Python3 中，bool 是 int 的子类，True 和 False 可以和数字相加， True为1、False为0
    issubclass(bool, int)
    print(True == 1)
    print(False == 0)


# 随机函数
def random_demo():
    # 从序列的元素中随机挑选一个元素
    print(random.choice("abcd"))
    # 按照步长step从start到end中，随机获取一个元素。只能获取int类型
    print(random.randrange(1, 100, 2))
    # 随机生成下一个实数，它在[0,1)范围内。
    print(random.random())
    # 随机生成下一个实数，它在[x,y]范围内。
    print(random.uniform(1, 10))
    # 将可变序列的所有元素随机排序
    list1 = [1, 2, 3, 4]
    random.shuffle(list1)
    print(list1)


if __name__ == '__main__':
    # number_demo()
    random_demo()
