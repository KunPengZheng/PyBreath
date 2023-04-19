import urllib.request
import urllib.error
import urllib.parse
import urllib.robotparser
# 导入BeautifulSoup
from bs4 import BeautifulSoup as bf

"""
urllib 库用于操作网页 URL，并对网页的内容进行抓取处理。

urllib.request - 打开和读取 URL。
urllib.error - 包含 urllib.request 抛出的异常。
urllib.parse - 解析 URL。
urllib.robotparser - 解析 robots.txt 文件。
"""


def simple_demo():
    """
    urllib.request 定义了一些打开 URL 的函数和类，包含授权验证、重定向、浏览器 cookies等。
    urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)
    参数说明：
        url：url 地址。
        data：发送到服务器的其他数据对象，默认为 None。
        timeout：设置访问超时时间。
        cafile 和 capath：cafile 为 CA 证书， capath 为 CA 证书的路径，使用 HTTPS 需要用到。
        cadefault：已经被弃用。
        context：ssl.SSLContext类型，用来指定 SSL 设置。
    """

    # urlopen 打开一个 URL，返回响应对象
    myURL = urllib.request.urlopen("https://www.runoob.com/")
    # 然后使用 read() 获取响应体。ead() 是读取整个网页内容，也可以指定读取的长度
    # readline() - 读取文件的一行内容
    # readlines() - 读取文件的全部内容，它会把读取的多行内容赋值给一个列表变量。需要遍历
    print("响应体：", myURL.read())
    print("响应码：", myURL.getcode())


def try_except_demo():
    """
    urllib.error 模块为 urllib.request 所引发的异常定义了异常类。
    > URLError 是 OSError 的一个子类，用于处理程序在遇到问题时会引发此异常（或其派生的异常），包含的属性 reason 为引发异常的原因。
    > HTTPError 是 URLError 的一个子类，用于处理特殊 HTTP 错误。属性code 为 HTTP 的状态码，reason 为引发异常的原因，headers 响应头。
    """
    # 处理异常
    try:
        myURL2 = urllib.request.urlopen("https://www.runoob.com/no.html")
    except urllib.error.HTTPError as e:
        print("异常错误：", e.code, e.reason)


def parse_demo():
    # URL 的编码与解码
    encode_url = urllib.parse.quote("https://www.runoob.com/")  # 编码
    print("URL 编码：", encode_url)
    unencode_url = urllib.parse.unquote(encode_url)  # 解码
    print("URL 解码：", unencode_url)

    o = urllib.parse.urlparse("https://www.runoob.com/?s=python+%E6%95%99%E7%A8%8B")
    # 内容是一个元组，包含 6 个字符串：URL协议，网络位置，路径，参数，查询，片段识别。
    print("解析 URL:", o)


def request_class_config_demo():
    """
    需要添加头部信息，指定请求方式则使用下面的类进行配置
    class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)
    参数说明：
        url：url 地址。
        data：发送到服务器的其他数据对象，默认为 None。
        headers：HTTP 请求的头部信息，字典格式。
        origin_req_host：请求的主机地址，IP 或域名。
        unverifiable：很少用整个参数，用于设置网页是否需要验证，默认是False。。
        method：请求方法， 如 GET、POST、DELETE、PUT等。
    """

    url = 'https://www.runoob.com/?s='  # 菜鸟教程搜索页面
    keyword = 'Python 教程'
    key_code = urllib.parse.quote(keyword)  # 对请求进行编码
    url_all = url + key_code
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }  # 头部信息
    request = urllib.request.Request(url_all, headers=header)
    reponse = urllib.request.urlopen(request).read()
    print("响应体：", reponse)
    pass


def robotparser_demo():
    """
    如果对符合下列条件的网站进行强行数据采集时，会具有法律风险。
        采集的站点有声明禁止爬虫采集时。
        网站通过Robots协议拒绝采集时。

    可爬取协议——Robots协议:
     > robots.txt（统一小写）是一种存放于网站根目录下的 robots 协议，它通常用于告诉搜索引擎对网站的抓取规则。
        该协议有三个属性：
        Uer-agent : 索引擎爬虫的名字，各大搜索引擎都有固定的名字，如百度Baisuspider，如果该项为*(通配符) 表示协议对任何搜索引擎爬虫均有效；
        Disallow :  禁止访问的路径；
        Allow : 允许访问的路径；比Disallow优先级高

        例子：该协议对所有爬虫有效,不允许抓取所有页面,但可以抓取 public 目录
        Uer-agent : *
        Disallow : /
        Allow : /public/


    urllib.robotparser 用于解析 robots.txt 文件
    """
    rp = urllib.robotparser.RobotFileParser()
    # 设置 robots.txt 文件的 URL。
    rp.set_url("http://www.musi-cal.com/robots.txt")
    # 读取 robots.txt URL 并将其输入解析器
    rp.read()
    # 返回上次抓取和分析 robots.txt 的时间。这适用于需要定期检查 robots.txt 文件更新情况的长时间运行的网页爬虫。
    print(rp.mtime)
    # 返回User-Agent是否可以抓取这个 URL
    print(rp.can_fetch("*", "http://www.musi-cal.com/"))
    pass


def smple_crawler():
    """
    爬虫: 一段自动抓取互联网信息的程序
    """

    # 因为现在大部分的网站都是有反爬的，会给你识别到是不是用户访问页面的。这里就需要访问的时候添加headers属性
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }  # 头部信息
    request = urllib.request.Request("http://bjdh.tv/", headers=header)
    # request = urllib.request.Request("http://bjdh.app/", headers=header)
    # request = urllib.request.Request("https://at28uhry.hxaa80.com/#/", headers=header)
    # request = urllib.request.Request("https://at28uhry.hxaa80.com/#/moves/playvideo/29494", headers=header)
    # 请求获取HTML
    html = urllib.request.urlopen(request)
    # 用BeautifulSoup解析html
    obj = bf(html.read(), 'html.parser')
    # 从标签head、title里提取标题
    print("打印标题:", obj.head.title)
    # 获取所有img标签
    for img in obj.find_all('img'):
        # 打印img标签的src属性
        # print(img["src"])
        print(img)


if __name__ == '__main__':
    # simple_demo()
    # try_except_demo()
    # parse_demo()
    # request_class_config_demo()
    # robotparser_demo()
    smple_crawler()
