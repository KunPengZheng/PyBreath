"""
while循环语句
1. 在 Python 中没有 do..while 循环
2. 死循环，通过设置条件表达式永远不为 false 来实现无限循环
3. while 循环使用 else 语句，如果while的条件判断语句为false，那么就执行else中的代码块
4. while循环体中只有一条语句，你可以将该语句与while写在同一行中。如：while (flag): print ('欢迎')
5. python也有break和continue关键字
"""


def while_demo():
    x = 10
    while x < 15:
        x += 1
        print(x, end=",")  # 参数end可以指定输出的末尾字符，默认是'\n'

    count = 0
    while count < 5:
        count = count + 1
    else:
        print(count, " 大于或等于 5")


"""
for 循环可以遍历任何可迭代对象，如一个列表或者一个字符串。
"""


def for_demo():
    # 一个参数，表示end
    # 两个参数，表示start和end
    # 两个参数，表示start和end，还有步长
    for i in range(5):
        print(i)


if __name__ == '__main__':
    while_demo()
    for_demo()
