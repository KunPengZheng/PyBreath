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


if __name__ == '__main__':
    pass
