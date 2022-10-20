
"""
File(文件) 方法
open() 方法用于打开一个文件，并返回文件对象。
"""


def common_demo():
    f = open("/Users/ykwl/Desktop/foo.txt", "wb")

    """
      flush() 方法是用来刷新缓冲区的，即将缓冲区中的数据立刻写入文件，同时清空缓冲区，不需要是被动的等待输出缓冲区写入。
      一般情况下，文件关闭后会自动刷新缓冲区，但有时你需要在关闭前刷新它，这时就可以使用 flush() 方法。
    """
    f.flush()

    """
      fileno() 方法返回一个整型的文件描述符(file descriptor FD 整型)，可用于底层操作系统的 I/O 操作。
    """
    fno = f.fileno()
    print("文件描述符为: ", fno)

    """
    方法检测文件是否连接到一个终端设备，如果是返回 True，否则返回 False。
    """
    ret = f.isatty()
    print("返回值 : ", ret)

    f.close()
    pass


def write_demo():
    f = open("/Users/ykwl/Desktop/foo.txt", "w")
    f.write("www.one.com\n")
    f.write("www.two.com\n")
    f.write("www.three.com\n")
    f.close()


def writelines_demo():
    """
    向文件写入一个序列字符串列表，如果需要换行则要自己加入每行的换行符。
    """
    f = open("/Users/ykwl/Desktop/foo.txt", "w")
    list1 = ["www.one.com\n", "www.two.com\n", "www.three.com\n"]
    f.writelines(list1)
    f.close()


# 读取指定路径的文件中的内容
def read_demo():
    write_demo()

    # 默认是文本模式
    f = open("/Users/ykwl/Desktop/foo.txt", "r")
    """
    read() 方法用于从文件读取指定的字符数（文本模式 t）或字节数（二进制模式 b），如果未给定参数 size 或 size 为负数则读取文件所有内容。
    """
    read_str = f.read(10)  # 因为是文本模式，所以这里的10表示10个字符
    print(read_str)
    f.close()


def readline_demo():
    write_demo()

    # 默认是文本模式
    f = open("/Users/ykwl/Desktop/foo.txt", "r")
    """
    readline() 方法用于从文件读取整行，包括 "\n" 字符。如果指定了一个非负数的参数，则返回指定大小的字节数或者字符数，包括 "\n" 字符。
    """
    read_str = f.readline(3)
    print(read_str)
    f.close()
    pass


def readlines_demo():
    write_demo()

    # 默认是文本模式
    f = open("/Users/ykwl/Desktop/foo.txt", "r")
    """
    readlines() 读取所有行并返回列表，若给定sizeint>0，返回总和大约为sizeint字节的行, 实际读取值可能比 sizeint 较大, 因为需要填充缓冲区。
    """
    for line in f.readlines():
        print(line)
    f.close()


def truncate_demo():
    write_demo()

    # 默认是文本模式
    f = open("/Users/ykwl/Desktop/foo.txt", "r+")
    """
    truncate() 方法用于从文件的首行首字节开始截断，截断文件为 size 个字节，无 size 表示从当前位置截断。作用
    相当于指定读取的范围，相当于字符串的截取，然后配合read使用
    """
    f.truncate()
    read = f.read()
    print(read)
    f.close()


if __name__ == '__main__':
    # common_demo()

    # read_demo()
    # readline_demo()
    # readlines_demo()

    # truncate_demo()

    # writelines_demo()
    pass
