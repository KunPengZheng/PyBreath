"""
1. 注意，Python 没有单独的字符类型，一个字符就是长度为1的字符串。
2. 在Python3中，所有的字符串都是Unicode字符串。在Python2中，普通字符串是以8位ASCII码进行存储的，而Unicode字符串则存储为16位unicode
   字符串，这样能够表示更多的字符集。使用的语法是在字符串前面加上前缀 u。
"""


def string_demo():
    # Python中的字符串用单引号' 或双引号 " 括起来，同时使用反斜杠 \ 转义特殊字符。
    # Python 字符串不能被改变。向一个索引位置赋值，比如str[0] = 'm'会导致错误。
    str1 = 'Runoob'
    # 字符串的截取的语法格式如下：变量[头下标:尾下标]，索引值以 0 为从左向右的开始位置，-1 为从右向左的开始位置。
    print(str1[0:6])  # 和java一样，包头不包尾
    print(str1[:6])  # 和java一样，包头不包尾
    print("end为负数，表示不包括最后多少位角标对应的内容", str1[0:-1])  # 只有end可以是负数，表示裁剪掉最后几位角标的内容，str[-1,-6]无效
    print("::步长取数据", str1[::-1])  # 以多少步长取数据，负数表示倒序取数。如果是[::2]的话，则是以步长2一次取数据
    print("::步长取数据", str1[2::-1])  # 相当于[0,2,-1]，默认start为0，end则为指定的2，步长为-1
    print(str1[0:])  # 从0开始到所有结束，相当于[0,str的字符串长度]
    print(str1[0])  # 获取指定index的元素
    print("a" in str1)  # 成员运算符  in ：如果字符串中包含给定的字符返回 True。not in：如果字符串中不包含给定的字符返回 True
    print(str1 * 2)  # 输出字符串两次，也可以写成 print (2 * str)
    print(str1 + "TEST")  # 连接字符串

    print('Ru\noob')  # 使用反斜杠 \ 转义特殊字符
    print(r'Ru\noob')  # 如果你不想让反斜杠发生转义，可以在字符串前面添加一个 r或者R，表示原始字符串

    print("我叫 %s 今年 %d 岁!" % ('小明', 10))  # 字符串格式化符号 和 格式化操作符辅助指令
    print("我叫 {} 今年 {} 岁!".format('小明', 10))  # 字符串格式化符号 和 格式化操作符辅助指令
    name = 'Runoob'
    # f-string python3.6 之后版本添加的，称之为字面量格式化字符串，是新的格式化字符串的语法。相当于kotlin的${}
    # f-string 格式化字符串以 f 开头，后面跟着字符串，字符串中的表达式用大括号 {} 包起来，它会将变量或表达式计算后的值替换进去。
    print(f"Hello {name}")
    print(f"{1 + 2}")
    w = {'name': 'Runoob', 'url': 'www.runoob.com'}
    print(f'{w["name"]}: {w["url"]}')
    print(f'{1+1=}')  # 在 Python 3.8 的版本中可以使用 = 符号来拼接运算表达式与结果。

    # """或者'''三引号允许一个字符串跨多行，"所见即所得"。
    # 一个典型的用例是，当你需要一块HTML或者SQL时，这时用字符串组合以及特殊字符串转义将会非常的繁琐。
    err_html = '''
    <HTML><HEAD><TITLE>
    Friends CGI Demo</TITLE></HEAD>
    <BODY><H3>ERROR</H3>
    <B>%s</B><P>
    <FORM><INPUT TYPE=button VALUE=Back
    ONCLICK="window.history.back()"></FORM>
    </BODY></HTML>
    '''
    print(err_html)


def api_demo():
    str1 = 'runoob'
    print(str1.capitalize())  # 将字符串的第一个字符转换为大写
    print(str1.swapcase())  # 将字符串中大写转换为小写，小写转换为大写
    # 返回一个指定的宽度 width 居中的字符串，如果 width 小于字符串宽度直接返回字符串，否则使用 fillchar （默认是空格）去填充。
    print(str1.center(8, "*"))
    # 返回一个原字符串右对齐,并使用空格填充至长度 width 的新字符串。如果指定的长度小于字符串的长度则返回原字符串
    print(str1.rjust(8, "*"))
    print(str1.zfill(8))  # 返回长度为 width 的字符串，原字符串右对齐，前面填充0
    print(str1.count("o", 0, len(str1)))
    # encode() 方法以指定的编码格式编码字符串。errors参数可以指定不同的错误处理方案。
    # errors -- 设置不同错误的处理方案。默认为 'strict',意为编码错误引起一个UnicodeError。 其他可能得值有 'ignore', 'replace',
    # 'xmlcharrefreplace', 'backslashreplace' 以及通过 codecs.register_error() 注册的任何值。
    print(str1.encode('UTF-8', 'strict'))
    print(str1.endswith("ob", 0, len(str1)))
    print(str1.startswith("ob", 0, len(str1)))
    # 把字符串 string 中的 tab 符号转为 指定数量的空格，tab 符号默认的空格数是 8 。
    print("\tTab".expandtabs(10))
    print(str1.find("o", 0, len(str1)))  # 找到第一个符合的元素的角标
    print(str1.rfind("o", 0, len(str1)))  # 类似于 find()函数，不过是从右边开始查找
    print(str1.index("o", 0, len(str1)))  # 跟find()方法一样，只不过如果str不在字符串中会报一个异常。
    print(str1.rindex("o", 0, len(str1)))  # 类似于 index()，不过是从右边开始.
    # 如果字符串至少有一个字符并且所有字符都是字母或数字则返 回 True，否则返回 False
    print(str1.isalnum())
    # 如果字符串至少有一个字符并且所有字符都是字母或中文字则返回 True, 否则返回 False
    print(str1.isalpha())
    # 如果字符串只包含数字则返回 True 否则返回 False..
    print(str1.isdigit())  # 数字只是阿拉伯数字
    # isnumeric() 方法检测字符串是否只由数字组成，数字可以是： Unicode 数字，全角数字（双字节），罗马数字，汉字数字。 指数类似 ² 与分数类似 ½ 也属于数字。
    print(str1.isnumeric())  # 数字的范围更广

    print(str1.islower())  # 都是小写的则返回True
    print(str1.isupper())  # 都是大写的则返回True
    print(str1.upper())  # 转换字符串中的小写字母为大写
    print(str1.lower())  # 转换字符串中的大写字母为小写

    print(" ".isspace())  # 如果字符串中只包含空白，则返回 True，否则返回 False.
    print(str1.istitle())  # 检测字符串中所有的单词拼写首字母是否为大写，且其他字母为小写。
    print(str1.title())  # 返回"标题化"的字符串,就是说所有单词都是以大写开始，其余字母均为小写
    print("-".join(("r", "u", "n", "o", "o", "b")))  # 将序列中的元素（参数二）以指定的字符（参数一）连接生成一个新的字符串
    print(" trip".lstrip())  # 截掉字符串左边的空格或指定字符。
    print("trip ".rstrip())  # 删除字符串右边的空格或指定字符。
    print(" trip ".strip())  # 在字符串上执行 lstrip()和 rstrip()
    print(max("abc"))  # 返回字符串 str 中最大的字母。
    print(min("abc"))  # 返回字符串 str 中最小的字母。

    print("abc".replace("a", "A"))  # 把 将字符串中的 old 替换成 new,如果 max 指定，则替换不超过 max 次。

    # 根据参数一指定的字符串分割，分割的次数根据参数二（默认为 -1, 即分隔所有）。
    # 如果参数1只出现一次，那么参数二设置>1也只会有两份。
    print(str1.split("o"))
    print(str1.rsplit("o"))
    # 按照行('\r', '\r\n', \n')分隔，返回一个包含各行作为元素的列表，如果参数 keepends 为 False，不包含换行符，如果为 True，则保留换行符。
    print(str1.splitlines())
    pass


if __name__ == '__main__':
    string_demo()
    api_demo()
    pass
