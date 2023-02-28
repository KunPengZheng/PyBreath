import matplotlib.pyplot as plt
import matplotlib
import numpy as np

"""
https://www.runoob.com/matplotlib/matplotlib-tutorial.html

Matplotlib 是 Python 的绘图库(画图工具)，它能让使用者很轻松地将数据图形化，并且提供多样化的输出格式。
"""


def simple_demo():
    # 确定起点和终点的x，y坐标
    xpoints = np.array([1, 2, 6, 8])
    ypoints = np.array([3, 8, 1, 10])
    """
    x, y参数：点或线的节点，x 为 x 轴数据，y 为 y 轴数据，数据可以列表或数组。
    fmt参数：'[marker标记][line线条][color颜色]'。可选
        > 颜色：'b' 蓝色，'m' 洋红色，'g' 绿色，'y' 黄色，'r' 红色，'k' 黑色，'w' 白色，'c' 青绿色，'#008000' RGB 颜色符串。
          多条曲线不指定颜色时，会自动选择不同颜色。
        > 线型：'‐' 实线，'‐‐' 破折线，'‐.' 点划线，':' 虚线。
        > 标记（两端的样式）：'.' 点标记，',' 像素标记(极小点)，'o' 实心圈标记，'v' 倒三角标记，'^' 上三角标记，'>' 右三角标记，'<' 左三角标记...等等。
    """
    plt.plot(xpoints, ypoints, "r--o")
    plt.show()


def marker_demo():
    ypoints = np.array([6, 2, 13, 10])
    """
    自定义标记的大小与颜色，使用的参数分别是：
        > markersize，简写为 ms：定义标记的大小。
        > markerfacecolor，简写为 mfc：定义标记内部的颜色。
        > markeredgecolor，简写为 mec：定义标记边框的颜色。
    """
    plt.plot(ypoints, marker='o', ms=20, mec='r', mfc='#4CAF50')
    plt.show()


def linestyle_demo():
    """
    线的类型可以使用 linestyle 参数来定义，简写为 ls。
    线的颜色可以使用 color 参数来定义，简写为 c
    线的宽度可以使用 linewidth 参数来定义，简写为 lw，值可以是浮点数，如：1、2.0、5.67 等。
    """
    ypoints = np.array([6, 2, 13, 10])
    plt.plot(ypoints, ls='-', c='#8FBC8F', lw='12.5')
    plt.show()


def mult_line():
    """
    多线条，内部自动会用不同的颜色区分
    """
    x1 = np.array([0, 1, 2, 3])
    y1 = np.array([3, 7, 5, 9])
    x2 = np.array([0, 1, 2, 3])
    y2 = np.array([6, 2, 13, 10])
    plt.plot(x1, y1, x2, y2)
    plt.show()


def axis_label_title_font():
    # Matplotlib 默认情况不支持中文，所以需要引入指定的中文字体，fname 为字体的路径；size 参数设置字体大小
    zhfont1 = matplotlib.font_manager.FontProperties(fname="/Users/zkp/Downloads/SourceHanSansSC-Bold.otf", size=22)
    font_css = {'color': 'blue', 'size': 20}
    x = np.array([1, 2, 3, 4])
    y = np.array([1, 4, 9, 16])
    plt.plot(x, y)
    # 使用 xlabel() 和 ylabel() 方法来设置 x 轴和 y 轴的标签。
    # fontproperties设置字体
    # fontdict 可以使用 css 来设置字体样式
    # xlabel() 方法提供了 loc 参数来设置 x 轴显示的位置，可以设置为: 'left', 'right', 和 'center'， 默认值为 'center'。
    plt.xlabel("x轴", fontproperties=zhfont1, fontdict=font_css, loc="left")
    # ylabel() 方法提供了 loc 参数来设置 y 轴显示的位置，可以设置为: 'bottom', 'top', 和 'center'， 默认值为 'center'。
    plt.ylabel("y轴", fontproperties=zhfont1, loc="bottom")
    # 使用 title() 方法来设置标题
    # title() 方法提供了 loc 参数来设置标题显示的位置，可以设置为: 'left', 'right', 和 'center'， 默认值为 'center'。
    plt.title("标题", fontproperties=zhfont1, loc="center")
    plt.show()

    # # 获取系统字体
    # a = sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])
    # print("打印系统字体:\n", a)
    # # 应用系统字体
    # plt.rcParams['font.family'] = ['PingFang HK']
    # x = np.array([1, 2, 3, 4])
    # y = np.array([1, 4, 9, 16])
    # plt.plot(x, y)
    # plt.xlabel("x轴")
    # plt.ylabel("x轴")
    # plt.title("标题")
    # plt.show()


def subplot_demo():
    """
    subplot()方法来绘制多个子图（多图）。
    """
    # plot 1:
    x = np.array([0, 6])
    y = np.array([0, 100])
    # 参数：
    #  > nrows, ncols：相当于将画布网格化，即划分行列数；然后从左到右，从上到下的顺序对每个子区域进行编号 1...N 。
    #      左上的子区域的编号为 1、右下的区域编号为 N，编号可以通过参数 index 来设置。
    #  > index参数：设置 numRows ＝ 2，numCols ＝ 2，就是将图表绘制成 2x2 的图片区域。
    #    > plotNum ＝ 1, 表示的坐标为(1, 1), 即第一行第一列的子图。
    #    > plotNum ＝ 2, 表示的坐标为(1, 2), 即第一行第二列的子图。
    #    > plotNum ＝ 3, 表示的坐标为(2, 1), 即第二行第一列的子图。
    #    > plotNum ＝ 4, 表示的坐标为(2, 2), 即第二行第二列的子图。
    plt.subplot(2, 2, 1)
    plt.plot(x, y)
    plt.title("plot 1")
    # plot 2:
    x = np.array([1, 2, 3, 4])
    y = np.array([1, 4, 9, 16])
    plt.subplot(2, 2, 2)
    plt.plot(x, y)
    plt.title("plot 2")
    # plot 3:
    x = np.array([1, 2, 3, 4])
    y = np.array([3, 5, 7, 9])
    plt.subplot(2, 2, 3)
    plt.plot(x, y)
    plt.title("plot 3")
    # plot 4:
    x = np.array([1, 2, 3, 4])
    y = np.array([4, 5, 6, 7])
    plt.subplot(2, 2, 4)
    plt.plot(x, y)
    plt.title("plot 4")

    plt.suptitle("RUNOOB subplot Test")
    plt.show()
    pass


def subplots_demo():
    """
    subplot() 和 subplots() 方法来绘制多个子图（多图）。
    """
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([1, 2, 3, 4, 5])

    x1 = np.array([6, 7, 8, 9, 10])
    y1 = np.array([6, 7, 8, 9, 10])

    x2 = np.array([11, 12, 13, 14, 15])
    y2 = np.array([11, 12, 13, 14, 15])

    x3 = np.array([16, 17, 18, 19, 20])
    y3 = np.array([16, 17, 18, 19, 20])

    # subplots() 设置子图的配置，是返回一个元组，包含了 figure 对象(画布)和 axes 对象 或者 axes数组 (控制绘图，坐标之类的)
    # 参数：
    #  > nrows, ncols：相当于将画布网格化，即划分行列数；然后从左到右，从上到下的顺序对每个子区域进行编号 1...N 。
    #      左上的子区域的编号为 1、右下的区域编号为 N，编号可以通过参数 index 来设置。
    #  > sharex、sharey：设置子图的x，y轴是否共享，可设置为 'none（False）'、'all（True）'、'row' 或 'col'
    #       > none或者False，表示每个子图都有自己的x，y轴
    #       > all或者True，表示每个子图共享x，y轴
    #       > 'row' 每个子图行共享一个 x 轴或 y 轴
    #       > 'col' 每个子图列共享一个 x 轴或 y 轴
    fig, ax = plt.subplots(2, 2, sharex="none", sharey="none")
    print("ax打印:\n", ax)
    ax[0, 0].plot(x, y, color='r')
    ax[0, 1].plot(x1, y1, color='b')
    ax[1, 0].plot(x2, y2, color='g')
    ax[1, 1].plot(x3, y3, color='r')

    ax[0, 0].set_title('title 1')
    ax[0, 1].set_title('title 2')
    ax[1, 0].set_title('title 3')
    ax[1, 1].set_title('title 4')

    """
    subplots_adjust 设置间距:
        > left, bottom, right, top这四个参数的每个参数的取值范围通常都在0-1之间。与其说是“间距”，倒不如说是图像边缘的“坐标”更确切。
          使用这四个参数时，将画布左下角视为坐标原点，画布的宽和高都视为1。如果参数取值大于1，则可能会出现图像的损失，图像会移动到画布之外，
          而不会报错。且left不能大于等于right，bottom不能大于等于top，如果违反这一点则会发生报错。
        > wspace和 hspace则分别表示水平方向上图像间的距离和垂直方向上图像间的距离。其的取值是可以取得大于1，具体的则具体情形自行
          调试选出合适的。这两个参数用于画布有多个子图时。  
    """
    plt.subplots_adjust(wspace=1, hspace=1)
    # 设置超级标题
    plt.suptitle("RUNOOB subplot Test")
    plt.show()
    pass


def figures_demo():
    """
    figure()参数：
        > figsize	tuple	figure.figsize	图像的长和宽（英寸）
        > dpi	    int	    figure.dpi	分辨率（点/英寸）
        > facecolor	tuple	figure.facecolor	绘制区域背景色
        > edgecolor	tuple	figure.edgecolor	绘图区域边缘的颜色
        > frameon	bool	True	是否绘制图像边缘
    """
    # 创建一个宽12，高6的空白图像区域(figsize * dpi)
    fig = plt.figure(figsize=(12, 6))

    # rect可以设置子图的位置与大小
    rect1 = [0.10, 0.55, 0.65, 0.35]  # [左, 下, 宽, 高] 规定的矩形区域 （全部是0~1之间的数，表示比例）
    rect2 = [0.10, 0.10, 0.65, 0.35]
    rect3 = [0.80, 0.10, 0.15, 0.80]

    # 在fig中添加子图ax，并赋值位置rect
    ax1 = plt.axes(rect1)
    ax2 = plt.axes(rect2)
    ax3 = plt.axes(rect3)

    plt.show()
    plt.close()
    pass


def grid():
    x = [1, 2, 3, 4]
    y = [1, 4, 9, 16]

    plt.title("RUNOOB grid() Test")
    plt.xlabel("x - label")
    plt.ylabel("y - label")
    plt.plot(x, y)
    """
    grid(b=None, which='major', axis='both')，设置图表中的网格线
        > b：可选，默认为 None，可以设置布尔值，true 为显示网格线，false 为不显示，如果设置 **kwargs 参数，则值为 true。
        > which：可选，可选值有 'major'、'minor' 和 'both'，默认为 'major'，表示应用更改的网格线。
        > axis：可选，设置显示哪个方向的网格线，可以是取 'both'（默认），'x' 或 'y'，分别表示两个方向，x 轴方向或 y 轴方向。
        > **kwargs：可选，设置网格样式，可以是 color='r', linestyle='-' 和 linewidth=2，分别表示网格线的颜色，样式和宽度。
    """
    plt.grid(axis="both", color='r', linestyle='--', linewidth=0.5)
    plt.show()
    pass


def scatter():
    x = [1, 2, 3, 4, 5, 6, 7, 8]
    y = [1, 4, 9, 16, 7, 11, 23, 18]
    """
    散点图，也叫 X-Y 图
    
    参数说明：
    x，y：长度相同的数组，也就是我们即将绘制散点图的数据点，输入数据。
    s：点的大小，默认 20，也可以是个数组，数组每个参数为对应点的大小。
    c：点的颜色，默认蓝色 'b'，也可以是个 RGB 或 RGBA 数组。
    marker：点的样式，默认小圆圈 'o'。
    cmap：Colormap，默认 None，标量或者是一个 colormap 的名字，只有 c 是一个浮点数数组的时才使用。
    alpha：透明度设置，0-1 之间，默认 None，即不透明。
    linewidths：散点标记的边界的宽度。
    """
    sizes = np.array([20, 50, 100, 200, 500, 1000, 60, 90])

    colors = np.array(["red", "green", "black", "orange", "purple", "beige", "cyan", '#88c999'])
    plt.scatter(x, y, s=sizes, c=colors, alpha=0.5, linewidths=10)

    # colors = np.array([10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0])
    # # Matplotlib 模块内置列很多颜色条。 颜色条就像一个颜色列表，传入范围从 0 到 100 的值获取颜色条中对应的颜色值
    # # 更多内置的颜色条：https://www.runoob.com/matplotlib/matplotlib-scatter.html
    # plt.scatter(x, y, s=sizes, c=colors, cmap='afmhot_r')
    # plt.colorbar()  # 显示颜色条

    plt.show()
    pass


def bar():
    """
    柱形图

    参数说明：
        x：x 轴数据的数组。
        height：浮点型数组，柱形图的高度。
        width：浮点型数组，柱形图的宽度。
        bottom：浮点型数组，底座的 y 坐标，默认 0。
        align：柱形图与 x 坐标的对齐方式，'center' 以 x 位置为中心，这是默认值。 'edge'：将柱形图的左边缘与 x 位置对齐。
               要对齐右边缘的条形，可以传递负数的宽度值及 align='edge'。
        **kwargs：其他参数。
    """
    x = np.array(["Runoob-1", "Runoob-2", "Runoob-3", "C-RUNOOB"])
    y = np.array([12, 22, 6, 18])
    plt.bar(x, y)
    plt.show()
    pass


def pie():
    """
    饼图，默认情况下，第一个扇形的绘制是从 x 轴开始并逆时针移动。

    参数说明：
        x：浮点型数组，表示每个扇形的面积。
        explode：数组，表示各个扇形之间的间隔，默认值为0。值越大，距离中心越远
        labels：列表，各个扇形的标签，默认值为 None。
        colors：数组，表示各个扇形的颜色，默认值为 None。
        autopct：设置饼图内各个扇形百分比显示格式，%d%% 整数百分比，%0.1f 一位小数， %0.1f%% 一位小数百分比， %0.2f%% 两位小数百分比。
        labeldistance：标签标记的绘制位置，相对于半径的比例，默认值为 1.1，如 <1则绘制在饼图内侧。
        pctdistance：类似于 labeldistance，指定 autopct 的位置刻度，默认值为 0.6。
        shadow：布尔值 True 或 False，设置饼图的阴影，默认为 False，不设置阴影。
        radius：设置饼图的半径，默认为 1。
        startangle：起始绘制饼图的角度，默认为从 x 轴正方向逆时针画起，如设定 =90 则从 y 轴正方向画起。
        counterclock：布尔值，设置指针方向，默认为 True，即逆时针，False 为顺时针。
        wedgeprops ：字典类型，默认值 None。参数字典传递给 wedge 对象用来画一个饼图。例如：wedgeprops={'linewidth':5} 设置 wedge 线宽为5。
        textprops ：字典类型，默认值为：None。传递给 text 对象的字典参数，用于设置标签（labels）和比例文字的格式。
        center ：浮点类型的列表，默认值：(0,0)。用于设置图标中心位置。
        frame ：布尔类型，默认值：False。如果是 True，绘制带有表的轴框架。
        rotatelabels ：布尔类型，默认为 False。如果为 True，旋转每个 label 到指定的角度。
    """
    x = np.array([35, 25, 25, 15])
    plt.pie(x,
            labels=['A', 'B', 'C', 'D'],  # 设置饼图标签
            colors=["#d5695d", "#5d8ca8", "#65a479", "#a564c9"],  # 设置饼图颜色
            explode=(0, 0.1, 0, 0),  # 第二部分突出显示，值越大，距离中心越远
            autopct='%.2f%%',  # 格式化输出百分比
            )
    plt.title("RUNOOB Pie Test")
    plt.show()
    pass


if __name__ == '__main__':
    # simple_demo()
    # marker_demo()
    # linestyle_demo()
    # mult_line()
    # axis_label_title_font()
    # subplot_demo()
    # subplots_demo()
    # figures_demo()
    # grid()
    # scatter()
    # bar()
    # pie()
    pass
