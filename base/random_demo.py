import random

"""
random 模块主要用于生成随机数。
函数说明：https://www.runoob.com/python3/python-random.html
"""

if __name__ == '__main__':
    # 返回 [0.0, 1.0) 范围内的下一个随机浮点数。
    print("生成随机数：", random.random())
    # 返回 指定step 在[start, stop) 范围内的下一个随机整数。
    print("randrange()：", random.randrange(0, 10, 2))
    # 返回随机整数 N 满足 a <= N <= b。
    print("randint()：", random.randint(0, 10))
    # 从非空序列 seq 返回一个随机元素(包头包尾)。 如果 seq 为空，则引发 IndexError。
    print("choice()：", random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]))
    # 将序列 x 随机打乱位置
    shuffleList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(shuffleList)
    print("shuffle()：", shuffleList)

    # seed() 随机数种子，同样的数值能够使得抽样的结果一致。这个种子（参数）相当于一把钥匙，对应了指定的随机数
    random.seed(1)
    print("随机数种子1_1：", random.random())
    random.seed(1)
    print("随机数种子1_2：", random.random())
    random.seed(2)
    print("随机数种子2：", random.random())

    pass
