import sys
from folder1.a import f1
import folder2.b
from folder3 import *

"""
1. 模块是一个包含所有你定义的函数和变量的文件，其后缀名是.py。
    > import moduleName 导入一个模块。相当于导入的是一个文件夹，是个相对路径。
       使用示例：模块.函数
    > from modname import name1[, name2[, ... nameN]]从模块中导入一个指定的部分。相当于导入的是一个文件夹中的文件，是个绝对路径。
       使用示例：直接使用函数名使用就可以了
    > from modname import *，这一句里的星号应该是沿用自正则中一样的意义，表示的是全部的意思，文中指出少用这种导入方式，我觉得是如果将一个模
    块的所有函数名导入当前命名空间中，如果不同模块包含了函数名相同的函数，或者是与自己编写得函数名相同将会导致混乱，而且在 debug 时还不容易发现 。
    这种方式进行导入，如果不同模块之间有相同的函数命名，最后导入的会覆盖前面的，也就是说只会调用到最后导入进的函数。  
2. 每个模块都有一个__name__属性，当其值是'__main__'时，表明该模块自身在运行，否则是被引入。
3. dir()命令是获取到一个object的所有属性、方法、类、import的模块名，当传值为空时默认传入的是当前py文件，可以通过这个函数来查看py文件的所有属性
4. 只要是在sys.path中的路径下能被找到的文件， 我们就可以直接使用import引用。
    > 比如我们需要导入另外一个程序的模块，一般要么直接copy过来然后导入；要么做成一个工具包然后导入；要么可以使用sys.path.append("模块所在
      文件夹的绝对路径")然后在导入。
5. 包是一种管理 Python 模块的，目录只有包含一个叫做 __init__.py 的文件才会被认作是一个包
    >  from package import * ，如果要导入一个包所有的模块，那么将包里面所有的模块名字用列表包裹赋值给 __init__.py 的 __all__ 的列表变量。
        但是不推荐这种方式，因为可读性很差，也可能遇到同名覆盖的问题。
"""

if __name__ == '__main__':  # 表示自身模块运行
    print("获取当前文件或者指定文件的成员方法和属性：", dir())
    print("模块的搜索路径：", sys.path)
    print('程序自身在运行')
    # 绝对路径导入指定函数，直接调用该函数即可
    f1()
    # 相对路径导入，模块.函数()调用
    folder2.b.f2()
    # from folder3 import *， 导入包的所有模块。
    c.f3()
    d.f4()
else:  # 自身被其它模块引入调用
    print('我来自另一模块')
