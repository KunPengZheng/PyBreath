import requests
import requests.cookies
import urllib3

"""
requests 模块，该模块主要用来发 送 HTTP 请求

每次调用 requests 请求之后，会返回一个 response 对象，该对象包含了具体的响应信息。响应信息如下：
apparent_encoding	编码方式
close()	关闭与服务器的连接
content	返回响应的内容，以字节为单位
cookies	返回一个 CookieJar 对象，包含了从服务器发回的 cookie
elapsed	返回一个 timedelta 对象，包含了从发送请求到响应到达之间经过的时间量，可以用于测试响应速度。比如 r.elapsed.microseconds 表示响应到达需要多少微秒。
encoding	解码 r.text 的编码方式
headers	返回响应头，字典格式
history	返回包含请求历史的响应对象列表（url）
is_permanent_redirect	如果响应是永久重定向的 url，则返回 True，否则返回 False
is_redirect	如果响应被重定向，则返回 True，否则返回 False
iter_content()	迭代响应
iter_lines()	迭代响应的行
json()	返回结果的 JSON 对象 (结果需要以 JSON 格式编写的，否则会引发错误)
links	返回响应的解析头链接
next	返回重定向链中下一个请求的 PreparedRequest 对象
ok	检查 "status_code" 的值，如果小于400，则返回 True，如果不小于 400，则返回 False
raise_for_status()	如果发生错误，方法返回一个 HTTPError 对象
reason	响应状态的描述，比如 "Not Found" 或 "OK"
request	返回请求此响应的请求对象
status_code	返回 http 的状态码，比如 404 和 200（200 是 OK，404 是 Not Found）
text	返回响应的内容，unicode 类型数据
url	返回响应的 URL

requests 方法如下表：
delete(url, args)	发送 DELETE 请求到指定 url
get(url, params, args)	发送 GET 请求到指定 url
head(url, args)	发送 HEAD 请求到指定 url
patch(url, data, args)	发送 PATCH 请求到指定 url
post(url, data, json, args)	发送 POST 请求到指定 url
put(url, data, args)	发送 PUT 请求到指定 url
request(method, url, args)	向指定的 url 发送指定的请求方法


状态码：requests.codes.xxxx。查看requests包的status_codes.py
"""


def simple_demo():
    # 发送请求
    # x = requests.get('https://www.runoob.com/')
    x = requests.get('https://www.runoob.com/try/ajax/json_demo.json')
    print("返回响应的内容:", x.text)
    print("返回响应的内容（json格式）:", x.json())
    print("响应的状态码:", x.status_code)
    print("响应状态的描述:", x.reason)
    print("返回编码:", x.apparent_encoding)
    pass


def params_headers_demo():
    params = {'s': 'python 教程'}

    # 设置请求头，如果不设置User-Agent，某些网站会发现这不是一个正常的浏览器发起的请求，网站可能会返回异常的结果，导致网页抓取失败。
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

    # params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
    response = requests.get("https://www.runoob.com/", params=params, headers=headers)

    print("查看响应状态码:", response.status_code)
    print("查看响应头部字符编码:", response.encoding)
    print("响应的url地址:", response.url)
    print("查看响应内容:", response.text)


def post_demo():
    myobj = {'fname': 'RUNOOB', 'lname': 'Boy'}
    # 发送请求
    x = requests.post('https://www.runoob.com/try/ajax/demo_post2.php', data=myobj)
    # 返回网页内容
    print("返回网页内容:", x.text)


def cookie_demo():
    def get_cookie():
        r = requests.get('https://www.baidu.com')
        print("RequestCookieJar:", r.cookies)
        for key, value in r.cookies.items():
            print("获取网站的cookie：", key + '=' + value)

    def upload_cookie():
        """
        上传cookie
            > 1.直接放在headers中，'Cookie':"xxxxxx"
            > 2.放在RequestsCookieJar容器中，key-value存储
        """
        cookies = '_octo=GH1.1.1849343058.1576602081; _ga=GA1.2.90460451.1576602111; __Host-user_session_same_site=nbDv62kHNjp4N5KyQNYZ208waeqsmNgxFnFC88rnV7gTYQw_; _device_id=a7ca73be0e8f1a81d1e2ebb5349f9075; user_session=nbDv62kHNjp4N5KyQNYZ208waeqsmNgxFnFC88rnV7gTYQw_; logged_in=yes; dotcom_user=Germey; tz=Asia%2FShanghai; has_recent_activity=1; _gat=1; _gh_sess=your_session_info'
        # cookie容器
        jar = requests.cookies.RequestsCookieJar()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
        for cookie in cookies.split(';'):
            key, value = cookie.split('=', 1)
            jar.set(key, value)
        r = requests.get('https://github.com/', cookies=jar, headers=headers)
        print(r.text)

    get_cookie()
    upload_cookie()


def session_demo():
    """
    如果用requests请求两个同源的接口，实际也是不同的Session，相当于两个浏览器打开不同的页面。
    解决方案：
        1.设置相同的Cookies
        2.设置相同的Session。利用 Session，可以做到模拟同一个会话而不用担心 Cookie 的问题。
    """
    s = requests.Session()  # 如果注销这句代码，那么返回数据的cookies是空的
    s.get('https://httpbin.org/cookies/set/number/123456789')
    r = s.get('https://httpbin.org/cookies')
    print(r.text)
    pass


def ssl_verify():
    """
    现在都要求使用 HTTPS 协议，但是有些网站可能并没有设置好 HTTPS 证书，或者网站的 HTTPS 证书可能并不被 CA 机构认可。这时候
    可能就会出现 SSL 证书错误的提示：requests.exceptions.SSLError

    解决方案：
    1.使用 verify 参数控制是否验证证书，如果将其设置为 False，在请求时就不会再验证证书是否有效。加上之后会报警告，它建议我们给它指定证书，
     可以通过设置忽略警告的方式来屏蔽这个警告：urllib3.disable_warnings()
    2. 也可以指定一个本地证书用作客户端证书，这可以是单个文件（包含密钥和证书）或一个包含两个文件路径的元组，另外注意，本地私有证书的 key
      必须是解密状态，加密状态的 key 是不支持的。
      response = requests.get('https://ssr2.scrape.center/', cert=('/path/server.crt', '/path/server.key'))
    """
    # 如果verify不设置为False将会报错requests.exceptions.SSLError
    urllib3.disable_warnings()
    response = requests.get('https://ssr2.scrape.center/', verify=False)
    print(response.status_code)
    pass


def timeout_demo():
    """
    在本机网络状况不好或者服务器网络响应太慢甚至无响应时，我们可能会等待特别久的时间才可能收到响应，甚至到最后收不到响应而报错。为了防止
    服务器不能及时响应，应该设置一个超时时间，即超过了这个时间还没有得到响应，那就报错。这需要用到 timeout 参数。
    """
    # 实际上请求分为两个阶段：connect和read， timeout 是二者的总和。
    # 如果要分别指定，就可以传入一个元组timeout=(10, 10)
    # 如果想永久等待，可以直接将 timeout 设置为 None，或者不设置直接留空，因为默认是 None。
    r = requests.get('https://httpbin.org/get', timeout=1)
    print(r.status_code)
    pass


def proxies_demo():
    """
    对于某些网站，在测试的时候请求几次，能正常获取内容。但是一旦开始大规模爬取，对于大规模且频繁的请求，网站可能会弹出验证码，或者跳转到
    登录认证页面，更甚者可能会直接封禁客户端的 IP，导致一定时间段内无法访问。
    解决：使用代理地址生成一个新的ip
    """
    # 只是demo，没有效果的
    proxies = {
        'http': 'http://127.0.0.1:9981',
        'https': 'http://127.0.0.1:9981',
    }
    requests.get('https://httpbin.org/get', proxies=proxies)
    print(get.text)
    pass


if __name__ == '__main__':
    # simple_demo()
    # params_headers_demo()
    # post_demo()
    # print("状态码:", requests.codes.ok)
    # print("状态码:", requests.codes.not_found)
    # cookie_demo()
    # session_demo()
    # ssl_verify()
    # timeout_demo()
    proxies_demo()
    pass
