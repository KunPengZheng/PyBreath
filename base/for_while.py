"""
while循环语句
1. 在 Python 中没有 do..while 循环
2. 死循环，通过设置条件表达式永远不为 false 来实现无限循环
3. while 循环使用 else 语句，如果while的条件判断语句为false，那么就执行else中的代码块
4. for 循环使用else语句，在正常遍历结束后就会执行else语句，如果是break的清空下else是不会被执行的
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
    # for i in range(5):
    #     print(i)

    # 在序列中遍历时，索引位置和对应值可以使用 enumerate() 函数
    list1 = [1, 2, 3, 4, 5]
    for i, v in enumerate(list1):
        print(i, v)

    # 遍历获取position和对应的value的另一种方式
    for i in range(len(list1)):
        print(i, list1[i])
        pass

    # 同时遍历两个或更多的序列
    questions = ['name', 'quest', 'favorite color']
    answers = ['lancelot', 'the holy grail', 'blue']
    # zip方法创建字典，然后遍历字典获取key和value
    for q, a in zip(questions, answers):
        # format格式化
        print('What is your {0}?  It is {1}.'.format(q, a))
        # 相当于👆的逻辑
        # print(f'What is your {q}?  It is {a}.')

if __name__ == '__main__':
    while_demo()
    for_demo()
