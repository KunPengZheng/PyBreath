import pickle
import pprint

"""
输入和输出
"""


# 读取键盘输入
def input_demo():
    input_str = input("请输入：")
    print("你输入的内容是: ", input_str)
    pass


# 写入内容到指定路径的文件中
# 如果要写入一些不是字符串的东西, 那么将需要先进行转换
def write_demo():
    # 打开一个文件，👇的路径是在mac上面的路径，username需要替换为你这台mac设置的账号
    # 参数一：文件路径
    # 参数二：mode：决定了打开文件的模式：只读，写入，追加等。所有可取值见如下的完全列表。这个参数是非强制的，默认文件访问模式为只读(r)。
    f = open("/Users/ykwl/Desktop/foo.txt", "w")
    f.write("Python 是一个非常好的语言。\n是的，的确非常好!!\n")
    # 关闭打开的文件
    # 在文本文件中 (那些打开文件的模式下没有 b 的), 只会相对于文件起始位置进行定位。当你处理完一个文件后, 调用 f.close() 来关闭
    # 文件并释放系统的资源，如果尝试再调用该文件，则会抛出异常。不过一般无论模式是不是b都调用close
    f.close()


# 读取指定路径的文件中的内容
def read_demo():
    f = open("/Users/ykwl/Desktop/foo.txt", "r")

    # read(size), 这将读取一定数目的数据, 然后作为字符串或字节对象返回。
    # size 是一个可选的数字类型的参数。 当 size 被忽略了或者为负, 那么该文件的所有内容都将被读取并且返回。
    # read_str = f.read()
    # print(read_str)

    # f.readline() 会从文件中读取单独的一行。换行符为 '\n'。f.readline() 如果返回一个空字符串, 说明已经已经读取到最后一行。
    read_str = f.readline()
    # f.tell() 返回文件对象当前所处的位置, 它是从文件开头开始算起的字节数。
    tell = f.tell()
    print("读取: " + read_str + ", tell: " + str(tell))

    # f.readlines() 将返回该文件中包含的所有行的数组。如果设置可选参数 sizehint, 则读取指定长度的字节, 并且将这些字节按行分割。
    # read_str = f.readlines()
    # print(read_str)

    # 迭代一个文件对象然后读取每行
    # for line in f:
    #     print(line, end='')

    f.close()


"""
f.seek()：改变文件指针当前的位置 

参数二whence： 0 表示开头（默认值）, 1 表示当前位置, 2 表示文件的结尾，例如：
    seek(x,0) ： 从起始位置即文件首行首字符开始移动 x 个字符
    seek(x,1) ： 表示从当前位置往后移动x个字符
    seek(-x,2)： 表示从文件的结尾往前移动x个字符

"""


def seek_demo():
    # 注意这里的模式是有b的，所以可以不用close
    f = open("/Users/ykwl/Desktop/foo.txt", "rb+")
    f.write(b'0123456789abcdef')
    # 移动到角标5的字节
    seek = f.seek(5)
    read = f.read(1)
    # 打印结果：seek: 5, read: b'5'
    print("seek: " + str(seek) + ", read: " + str(read))
    seek = f.seek(-3, 2)  # 移动到文件的倒数第三字节
    read = f.read(1)
    # 打印结果：seek: 13, read: b'd'
    print("seek: " + str(seek) + ", read: " + str(read))


# with as ：自动关闭文件
def with_as_demo():
    with open("/Users/ykwl/Desktop/foo.txt", "r") as f:
        read_data = f.read()


"""
python的pickle模块实现了基本的数据序列和反序列化。
通过pickle模块的序列化操作我们能够将程序中运行的对象信息保存到文件中去，永久存储。
通过pickle模块的反序列化操作，我们能够从文件中创建上一次程序保存的对象。
"""


def pickle_demo():
    # 序列化
    data1 = {'a': [1, 2.0, 3, 4 + 6j],
             'b': ('string', u'Unicode string'),
             'c': None}
    f = open('/Users/ykwl/Desktop/data.pkl', 'wb')
    pickle.dump(data1, f)
    f.close()

    # 反序列化
    f = open('/Users/ykwl/Desktop/data.pkl', 'rb')
    data2 = pickle.load(f)
    # Pretty-print，打印 流的 Python 对象
    pprint.pprint(data2)
    pass


if __name__ == '__main__':
    # input_demo()

    # write_demo()
    # read_demo()

    # seek_demo()

    # with_as_demo()

    pickle_demo()
    pass
