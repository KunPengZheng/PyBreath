import os
import shutil


def open_demo():
    f = open("/Users/ykwl/Desktop/foo.txt", "w")
    f.close()
    pass


# 检验权限模式
def access_demo():
    open_demo()

    # 测试path是否存在
    f_ok = os.access("/Users/ykwl/Desktop/foo.txt", os.F_OK)
    # 测试path是否可读
    r_ok = os.access("/Users/ykwl/Desktop/foo.txt", os.R_OK)
    # 测试path是否可写
    w_ok = os.access("/Users/ykwl/Desktop/foo.txt", os.W_OK)
    # 测试path是否可执行
    x_ok = os.access("/Users/ykwl/Desktop/foo.txt", os.X_OK)
    print("access：", f_ok, r_ok, w_ok, x_ok)
    pass


def chdir_demo():
    # 查看当前工作目录
    getcwd = os.getcwd()
    print("当前工作目录为 %s" % getcwd)
    os.chdir(getcwd + "/folder1")
    getcwd = os.getcwd()
    print("目录修改成功 %s" % getcwd)
    pass


def replace_demo():
    path = 'google.txt'
    # 创建文件
    getcwd = os.getcwd()
    t = open(getcwd + "/" + path, "w")
    t.close()
    # 将文件或目录 src 重命名为 dst，如果 dst 是非空目录，则会引发 OSError。如果 dst 存在并且是一个文件，如果用户有权限，它将被替换。
    os.replace(getcwd + "/" + path, getcwd + "/" + 'gg.txt')
    pass


if __name__ == '__main__':
    # access_demo()
    # chdir_demo()
    # print("获取当前文件所在目录的路径:", os.path.dirname(os.path.realpath(__file__)))
    # print("获取当前文件的路径:", os.path.realpath(__file__))
    replace_demo()
    pass
