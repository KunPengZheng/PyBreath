import os


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
    os.chdir(getcwd + "/temp")
    getcwd = os.getcwd()
    print("目录修改成功 %s" % getcwd)
    pass


if __name__ == '__main__':
    access_demo()
    chdir_demo()
    pass
