"""

"""
import sys


def try_catch():
    try:
        result = 1 / 0
    except ZeroDivisionError as err:
        print('Handling run-time error:', err)
    except ValueError:
        print("多个except语块")
    except:
        # 最后一个except子句可以忽略异常的名称，它将被当作通配符使用。你可以使用这种方法打印一个错误信息，然后再次把异常抛出。
        # 如果不知道逻辑会抛出什么异常，可以直接使用这种方式，相当于会捕获所有异常
        print("Unexpected error:", sys.exc_info()[0])
    pass


def try_catch1():
    try:
        result = 1 / 0
    except (RuntimeError, TypeError, NameError, ZeroDivisionError) as err:
        # 一个except子句可以同时处理多个异常，这些异常将被放在一个括号里成为一个元组
        print('Handling run-time error:', err)


def try_catch_else():
    try:
        result = 1 / 1
    except:
        print("Unexpected error:", sys.exc_info()[0])
    else:
        # else语块在try块没有发生异常的时候会被执行
        print("try块没有发生异常的时候会执行")


def try_catch_else_finally():
    try:
        result = 1 / 1
    except:
        print("Unexpected error:", sys.exc_info()[0])
    else:
        print("try块没有发生异常的时候会执行")
    finally:
        print("try块没有发生异常的时候会执行")


def raise_demo():
    # 使用 raise 语句抛出一个指定的异常
    raise Exception("使用raise抛出一个异常")
    pass


def raise_custom_demo():
    raise MyError("使用raise抛出一个自定义异常")
    pass


# 用户自定义异常，异常类继承自 Exception 类
class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


if __name__ == '__main__':
    # try_catch()
    # try_catch1()
    # try_catch_else()
    # raise_demo()
    raise_custom_demo()
    pass
