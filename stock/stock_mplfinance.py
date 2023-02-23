import mplfinance as mpf
import stock.stock_db as sdb
import pandas as pd
import matplotlib as mpl
import stock_constant as sc

"""
mplfinance 里面提供的函数，其实封装了 pyplot 库，本质上是 pyplot 库 k 线的定制版。
"""


def simple_demo():
    # 设置marketcolors
    # up:设置K线线柱颜色，up意为收盘价大于等于开盘价
    # down:与up相反，这样设置与国内K线颜色标准相符
    # edge:K线线柱边缘颜色(i代表继承自up和down的颜色)，下同。详见官方文档)
    # wick:灯芯(上下影线)颜色
    # volume:成交量直方图的颜色
    # inherit:是否继承，选填
    mc = mpf.make_marketcolors(
        up='red',
        down='green',
        edge='in',
        wick='in',
        volume='in',
        inherit=True)

    # 设置图形风格
    # gridaxis:设置网格线位置
    # gridstyle:设置网格线线型
    # y_on_right:设置y轴位置是否在右
    m_style = mpf.make_mpf_style(
        gridaxis='both',
        gridstyle='-.',
        figcolor='(0.82, 0.83, 0.85)',
        gridcolor='(0.82, 0.83, 0.85)',
        y_on_right=False,
        marketcolors=mc)

    df = sdb.stock_daily("600000", "1999-11-10", "2001-12-14")
    # 您的索引不是正确的数据类型。需要使用以下方法对其进行转换：
    # df.index = pd.to_datetime(df.index)
    mpf.plot(df.iloc[0:100], style=m_style, type='candle', volume=True)


def custom_style_demo():
    # 设置marketcolors
    # up:设置K线线柱颜色，up意为收盘价大于等于开盘价
    # down:与up相反，这样设置与国内K线颜色标准相符
    # edge:K线线柱边缘颜色(i代表继承自up和down的颜色)，下同。详见官方文档)
    # wick:灯芯(上下影线)颜色
    # volume:成交量直方图的颜色
    # inherit:是否继承，选填
    mc = mpf.make_marketcolors(
        up='red',
        down='green',
        edge='in',
        wick='in',
        volume='in',
        inherit=True)

    # 设置图形风格
    # gridaxis:设置网格线位置
    # gridstyle:设置网格线线型
    # y_on_right:设置y轴位置是否在右
    m_style = mpf.make_mpf_style(
        gridaxis='both',
        gridstyle='-.',
        figcolor='(0.82, 0.83, 0.85)',
        gridcolor='(0.82, 0.83, 0.85)',
        y_on_right=False,
        marketcolors=mc)

    # 获取figure对象，以便对Axes对象和figure对象的自由控制
    fig = mpf.figure(style=m_style, figsize=(12, 8),
                     facecolor=(0.82, 0.83, 0.85))
    # 主图相对figure 底部 0.06，0.25，宽（0.88）、高（0.60）
    ax1 = fig.add_axes([0.06, 0.25, 0.88, 0.60])
    # 指标图 sharex 关键字指明与ax1在x轴上对齐，且共用x轴
    ax2 = fig.add_axes([0.06, 0.15, 0.88, 0.10], sharex=ax1)
    # macd
    ax3 = fig.add_axes([0.06, 0.05, 0.88, 0.10], sharex=ax1)
    # 设置y轴标签
    ax1.set_ylabel('price')
    ax2.set_ylabel('volume')
    ax3.set_ylabel('macd')

    # 下载的字体路径
    zhfont = mpl.font_manager.FontProperties(fname=sc.text_font)
    # 标题格式，字体为中文字体，颜色为黑色，粗体，水平中心对齐
    title_font = {'fontproperties': zhfont,
                  'size': '16',
                  'color': 'black',
                  'weight': 'bold',
                  'va': 'bottom',
                  'ha': 'center'}
    # 红色数字格式（显示开盘收盘价）粗体红色24号字
    large_red_font = {'fontproperties': zhfont,
                      'size': '24',
                      'color': 'red',
                      'weight': 'bold',
                      'va': 'bottom'}
    # 绿色数字格式（显示开盘收盘价）粗体绿色24号字
    large_green_font = {'fontproperties': zhfont,
                        'size': '24',
                        'color': 'green',
                        'weight': 'bold',
                        'va': 'bottom'}
    # 小数字格式（显示其他价格信息）粗体红色12号字
    small_red_font = {'fontproperties': zhfont,
                      'size': '12',
                      'color': 'red',
                      'weight': 'bold',
                      'va': 'bottom'}
    # 小数字格式（显示其他价格信息）粗体绿色12号字
    small_green_font = {'fontproperties': zhfont,
                        'size': '12',
                        'color': 'green',
                        'weight': 'bold',
                        'va': 'bottom'}
    # 标签格式，可以显示中文，普通黑色12号字
    normal_label_font = {'fontproperties': zhfont,
                         'size': '12',
                         'color': 'black',
                         'va': 'bottom',
                         'ha': 'right'}
    # 普通文本格式，普通黑色12号字
    normal_font = {'fontproperties': zhfont,
                   'size': '12',
                   'color': 'black',
                   'va': 'bottom',
                   'ha': 'left'}

    # 获取数据
    df = sdb.stock_daily("600000", "1999-11-10", "2001-12-14")

    N = [5, 10, 20, 60]
    for i in N:
        df['MA' + str(i)] = ta.EMA(df['Close'], timeperiod=i)

    # 通过金融库 talib 生成MACD指标，
    short_win = 12  # 短期EMA平滑天数
    long_win = 26  # 长期EMA平滑天数
    macd_win = 9  # DEA线平滑天数
    macd_tmp = ta.MACD(df['Close'], fastperiod=short_win, slowperiod=long_win, signalperiod=macd_win)
    DIF = macd_tmp[0][start_index:end_index]
    DEA = macd_tmp[1][start_index:end_index]
    MACD = macd_tmp[2][start_index:end_index]
    pass


if __name__ == '__main__':
    simple_demo()
    pass
