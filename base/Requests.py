import requests

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
"""

if __name__ == '__main__':
    # 发送请求
    # x = requests.get('https://www.runoob.com/')
    x = requests.get('https://www.runoob.com/try/ajax/json_demo.json')
    print("返回响应的内容:", x.text)
    print("返回响应的内容（json格式）:", x.json())
    print("响应的状态码:", x.status_code)
    print("响应状态的描述:", x.reason)
    print("返回编码:", x.apparent_encoding)

    pass
