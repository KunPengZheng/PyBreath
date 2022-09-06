"""
迭代器
1. 也可以用于遍历，但一般用for即可
"""
import sys


def iter_demo():
    list1 = [1, 2, 3, 4]
    iter1 = iter(list1)
    # for i in iter1:
    #     print(i)

    while True:
        try:
            print(next(iter1))
        except StopIteration:
            sys.exit()
            pass


if __name__ == '__main__':
    iter_demo()
