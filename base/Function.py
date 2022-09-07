"""
函数

格式如下：
def 函数名（参数列表）:
    函数体

1. 以 def 关键词开头
2. 函数的第一行语句可以选择性地使用文档字符串，用于存放函数说明
3. return [表达式] 结束函数，选择性地返回一个值给调用方，不带表达式的 return 相当于返回 None。
4. 调用的时候可以使用 参数名 = 参数值进行传递
5. 函数定义的时候支持默认参数
6. 支持不定长参数，一般放在最后，如果没放在最后，那么在调用的时最后的参数需要使用 "参数名 = 参数值进行传递" 表示。
   > 加了星号 * 的参数会以元组(tuple)的形式导入，存放所有未命名的变量参数，如果在函数调用时没有指定参数，它就是一个空元组。
   > 加了两个星号 ** 的参数会以字典的形式导入。
7. 匿名函数，使用lambda 来创建匿名函数。格式：lambda [arg1 [,arg2,.....argn]]:expression
    > 所谓匿名，意即不再使用 def 语句这样标准的形式定义一个函数。lambda 只是一个表达式，函数体比 def 简单很多。
    > lambda 的主体是一个表达式，而不是一个代码块。
    > lambda 函数拥有自己的命名空间，且不能访问自己参数列表之外或全局命名空间里的参数。
8. 以将匿名函数封装在一个函数内，这样可以使用同样的代码来创建多个匿名函数（retrun返回的就是匿名函数）。
9. 强制位置参数。形参语法 / 用来指明在/之前的函数形参必须使用指定位置参数的形似，不能使用关键字参数的形式。
"""


def return_demo():
    return 1


def none_demo():
    print("1")


def params_name(s="默认"):
    print(s)


def variable_params_tuple(s, *ss, sss):
    print(s)
    print(ss)
    print(sss)


def variable_params_dic(s, **ss):
    print(s)
    print(ss)


def lamda_demo():
    lambda1 = lambda a: a + 10
    print(lambda1(5))


# 以将匿名函数封装在一个函数内，这样可以使用同样的代码来创建多个匿名函数（retrun返回的就是匿名函数）。
def lambda_return_demo(n):
    return lambda a: a * n


# 强制位置参数。形参语法 / 用来指明在/之前的函数形参必须使用指定位置参数的形似，不能使用关键字参数的形式。
def forced_position_params(a, b, /, c, d):
    print(a, b, c, d)


if __name__ == '__main__':
    params_name(s="参数名")
    variable_params_tuple(1, 2, 3, 4, sss=5)
    variable_params_dic(1, a=2, b=3)  # 默认key为字符串
    lamda_demo()

    # 传递函数的参数，获取lambda表达式
    lambda_return = lambda_return_demo(2)
    # 调用lambda表达式，传递lambda的参数
    print(lambda_return(11))

    forced_position_params(1, 2, c=3, d=4)
