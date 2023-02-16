"""
迭代器
1. 也可以用于遍历，但一般用for即可，Python的序列（字符、列表、元组、集合、字典）都已经实现了迭代器协议，所以才能使用 for in 语句进行迭代遍历。
    for in 循环体在遇到 StopIteration 异常时，便终止迭代和遍历。
2. 把一个类作为一个迭代器使用需要在类中实现两个方法 __iter__() 与 __next__()
3. __iter__() 方法返回一个特殊的迭代器对象， 这个迭代器对象实现了 __next__() 方法并通过 StopIteration 异常 表示 迭代的完成。
4. StopIteration 异常用于标识迭代的完成，防止出现无限循环的情况
5. 使用了 yield 的函数被称为生成器（generator）
    > 生成器就是一个迭代器，也是用于遍历，可以使用for或者next()进行遍历。
    > 既然是迭代器，也是需要定义 __iter__() 与 __next__()
    > yield就是专门给生成器用的return
    > 生成器函数调用yield，生成器函数会暂停执行，所有变量的值和下一行代码位置会被记录，直到再次调用next()。
      一旦next()再次被调用，会从之前记录的代码位置恢复执行。如果永远不调用next()，yield保存的状态就被无视了。
    > 如果生成器函数调用了return，或者执行到函数的末尾，会出现一个StopIteration异常，这是通知next()的调用者这个生成器没有下一个值了(这就是普通迭代器的行为)。
      因此，这个while循环是用来确保生成器函数永远也不会执行到函数末尾的，只要调用next()这个生成器就会生成一个值。这是一个处理无穷序列的常见方法（这类生成器也是很常见的）。
    > yield后面可以加多个数值（可以是任意类型），但返回的值是元组类型的。
"""
import math
import sys


def iter_demo():
    list1 = [1, 2, 3, 4]

    # for遍历
    for i in list1:
        print(i)

    # iter生成迭代器
    iter12 = iter(list1)
    while True:
        try:
            print(next(iter12))
        except StopIteration:
            # break停止
            break


# 自定义迭代器类
class CustomIter:
    a = 0

    def __iter__(self):
        return self

    def __next__(self):
        x = self.a
        self.a += 1
        return x


def simple_gene_demo():
    yield 1
    yield 2
    yield 3
    pass


class InfiniteRange:
    """
    无穷序列的问题：如果将无穷序列放入到list中，那么内存一定会爆；同理，一次性返回符合条件的值也会爆内存
    """

    def is_prime(self, number):
        """
          因数是指整数a除以整数b(b≠0) 的商正好是整数而没有余数，我们就说b是a的因数。
          质数(也叫素数)是指在大于1的自然数中，除了1和它本身以外不再有其他因数的自然数。
          """
        if number > 1:
            if number == 2:
                return True
            if number % 2 == 0:
                return False
            for current in range(3, int(math.sqrt(number) + 1), 2):
                if number % current == 0:
                    return False
            return True
        return False

    def get_primes(self, number):
        while True:
            if self.is_prime(number):
                yield number
            number += 1

    def enter_function(self):
        total = 2
        # get_primes是一个生成器也就是迭代器，所以可以使用for，而for就相当于调用了next()函数。
        for next_prime in self.get_primes(3):
            print("next_prime:", next_prime)
            if next_prime < 2000000:
                total += next_prime
            else:
                print(total)
                return


def gene_demo2():
    m = 0
    n = 2
    l = ['s', 1, 3]
    k = {1: 1, 2: 2}
    p = ('2', 's', 't')
    while True:
        m += 1
        yield m
        # yield后面可以加多个数值（可以是任意类型），但返回的值是元组类型的。
        yield m, n, l, k, p


if __name__ == '__main__':
    iter_demo()
    # 实例化
    custom_iter = CustomIter()
    iter1 = iter(custom_iter)

    # for遍历生成器
    for value in simple_gene_demo():
        print("for遍历生成器：", value)

    # next()方法遍历
    simple_gene = simple_gene_demo()
    print("next()遍历生成器1：", next(simple_gene))
    print("next()遍历生成器2：", next(simple_gene))
    print("next()遍历生成器3：", next(simple_gene))
    # 如果生成器函数调用了return，或者执行到函数的末尾，会出现一个StopIteration异常。 这会通知next()的调用者这个生成器没有下一个值了(这就是普通迭代器的行为)。
    # print("next()遍历生成器4：", next(simple_gene))

    # 处理无穷序列的示例
    # infinite_range = InfiniteRange()
    # infinite_range.enter_function()

    gene2 = gene_demo2()
    print(next(gene2))  # 1
    tuple1 = next(gene2)
    print(f"{tuple1},{type(tuple1)}")  # (1, 2, ['s', 1, 3], {1: 1, 2: 2}, ('2', 's', 't'))
    print(next(gene2))  # 2
