"""
迭代器
1. 也可以用于遍历，但一般用for即可，Python的序列（字符、列表、元组、字典）都已经实现了迭代器协议，所以才能使用 for in 语句进行迭代遍历。
    for in 循环体在遇到 StopIteration 异常时，便终止迭代和遍历。
2. 把一个类作为一个迭代器使用需要在类中实现两个方法 __iter__() 与 __next__()
3. __iter__() 方法返回一个特殊的迭代器对象， 这个迭代器对象实现了 __next__() 方法并通过 StopIteration 异常 表示 迭代的完成。
4. StopIteration 异常用于标识迭代的完成，防止出现无限循环的情况
5. 使用了 yield 的函数被称为生成器（generator），生成器就是一个迭代器，也是用于遍历。
    > 每次执行到有yield的时候，会返回yield后面的值 并且函数会暂停，直到下次调用或迭代终止；
    > yield后面可以加多个数值（可以是任意类型），但返回的值是元组类型的。
"""
import sys


def iter_demo():
    list1 = [1, 2, 3, 4]
    #
    for i in list1:
        print(i)
    iter12 = iter(list1)
    while True:
        try:
            print(next(iter12))
        except StopIteration:
            sys.exit()
            pass


# 自定义迭代器类
class CustomIter:
    a = 0

    def __iter__(self):
        return self

    def __next__(self):
        x = self.a
        self.a += 1
        return x


def gene_demo():
    index = 0
    li = [1, 2, 3, 4, 5]
    yield li[index]
    index += 1


def gene_demo2():
    m = 0
    n = 2
    l = ['s', 1, 3]
    k = {1: 1, 2: 2}
    p = ('2', 's', 't')
    while True:
        m += 1
        yield m
        yield m, n, l, k, p


if __name__ == '__main__':
    # iter_demo()
    # 实例化
    # custom_iter = CustomIter()
    # iter1 = iter(custom_iter)

    # 调用函数后，会返回一个生成器对象，然后对该生成器对象，使用 next() 逐一返回。
    gene = gene_demo()
    print(next(gene))

    gene2 = gene_demo2()
    print(next(gene2))  # 1
    tuple1 = next(gene2)
    print(f"{tuple1},{type(tuple1)}")  # (1, 2, ['s', 1, 3], {1: 1, 2: 2}, ('2', 's', 't'))
    print(next(gene2))  # 2
