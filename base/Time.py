import time

import calendar

"""
python中时间日期格式化符号：

%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12）
%M 分钟数（00=59）
%S 秒（00-59）
%a 本地简化星期名称
%A 本地完整星期名称
%b 本地简化的月份名称
%B 本地完整的月份名称
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366）
%p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始
%w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始
%x 本地相应的日期表示
%X 本地相应的时间表示
%Z 当前时区的名称
%% %号本身
"""


def time_demo():
    print("当前时间戳为:", time.time())

    # tm_wday：0 到 6 (0是周一)；tm_yday：一年中的第几天，1 到 366；tm_isdst：是否为夏令时，值有：1(夏令时)、0(不是夏令时)、-1(未知)，默认 -1
    print("本地时间（元组）:", time.localtime(time.time()))  # 参数不传相当于传入time.time()

    # 接受时间元组并返回一个可读的形式为"星期 月份 天 时：分：秒 年 "
    print("获取格式化的本地时间:", time.asctime())  # 参数是元组
    print("获取格式化的本地时间:", time.ctime())  # 参数是浮点

    # 指定格式的格式化日期
    print("格式化日期:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))  # 格式化成2016-03-20 11:45:39形式
    print("格式化日期:", time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))  # 格式化成Sat Mar 28 22:24:24 2016形式

    # 元组的时间转换为时间戳
    print("转换为时间戳:", time.mktime(time.localtime()))

    a = "Sat Mar 28 22:24:24 2016"
    # 参数一：时间字符串；参数二：参数一的格式。将指定格式的时间字符串转换为元组形式
    print(time.strptime(a, "%a %b %d %H:%M:%S %Y"))

    # 推迟调用线程的运行
    # time.sleep(2.0)

    # 返回系统的运行时间，包含整个系统的睡眠时间。由于返回值的基准点是未定义的，所以，只有连续调用的结果之间的差才是有效的。
    print("返回系统运行时间:", time.perf_counter())
    # 返回当前进程执行 CPU 的时间总和，不包含睡眠时间。由于返回值的基准点是未定义的，所以，只有连续调用的结果之间的差才是有效的。
    print("返回进程运行时间:", time.process_time())


def calendar_demo():
    # 返回当前每周的第一天。默认情况下，首次载入 calendar 模块时返回 0，即星期一。
    print("返回当前每周的第一天:", calendar.firstweekday())

    # 是否为闰年
    print("是否为闰年:", calendar.isleap(2023))

    # 返回在Y1，Y2两年之间的闰年总数。
    print("返回在Y1，Y2两年之间的闰年总数:", calendar.leapdays(2020, 2023))

    # 返回元素是List的List，元素List的长度为一个星期的天数。
    # 如果当天是属于本月份那么就显示对应的日期（从1开始），不属于则用0表示
    print("返回指定年份的月份的list:", calendar.monthcalendar(2023, 2))

    # 返回两个整数。第一个是该月的第一天是星期几（星期几是从0（星期一）到6（星期日）），第二个是该月有几天。
    print("获取指定年份的月份有多少天以及第一天是星期几：", calendar.monthrange(2023, 2))

    # 返回指定年份的月份的星期几在这个月是几号
    print("返回给定日期的日期码：", calendar.weekday(2023, 2, 1))

    print("打印日历：")
    # 打印指定年份的月份的日历
    # calendar.prmonth(2023,1) 等同于👇，内部自带print()而已
    print(calendar.month(2023, 1))

    # 打印指定年份的所有月份的日历
    # calendar.prcal(2023)等同于👇，内部自带print()而已
    print(calendar.calendar(2023))

    # 设置每周的起始日期码。0（星期一）到6（星期日）。
    # calendar.setfirstweekday(6)
    # print("返回当前每周的第一天:", calendar.firstweekday())
    pass


if __name__ == '__main__':
    time_demo()
    calendar_demo()
    pass
