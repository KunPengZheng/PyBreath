import mplfinance as mpf
import stock.stock_db as sdb
import pandas as pd

"""
mplfinance 里面提供的函数，其实封装了 pyplot 库，本质上是 pyplot 库 k 线的定制版。
"""

if __name__ == '__main__':
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
