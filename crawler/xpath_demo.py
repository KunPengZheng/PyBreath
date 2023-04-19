from lxml import etree


"""
https://juejin.cn/post/7085675994442366983#heading-4

XPath，全称是 XML Path Language，即 XML 路径语言，它是一门在 XML 文档中查找信息的语言。它最初是用来抽取 XML 文档信息的，但是它
同样适用于 HTML 文档的信息抽取。

XPath 常用规则
    > nodename	选取此节点的所有子节点
    > /	        从当前节点选取直接子节点
    > //	    从当前节点选取子孙节点
    > .	        选取当前节点
    > ..	    选取当前节点的父节点
    > @	        选取属性
"""


def html_demo():
    simple_text = '''
       <div>
           <ul>
                <li class="item-0"><a href="link1.html">first item</a></li>
                <li class="item-1"><a href="link2.html">second item</a></li>
                <li class="item-inactive"><a href="link3.html">third item</a></li>
                <li class="item-1"><a href="link4.html">fourth item</a></li>
                <li class="item-0"><a href="link5.html">fifth item</a>
            </ul>
        </div>
       '''
    html = etree.HTML(simple_text)  # 构造了一个 XPath 解析对象
    # 也可以直接读取文本文件进行解析
    # html = etree.parse('./test.html', etree.HTMLParser())
    result = etree.tostring(html)  # tostring()补全缺失的标签，返回byte类型
    decode = result.decode('utf-8')  # 利用 decode 方法将其转成 str 类型
    print(decode)
    pass


def all_node_demo():
    text = """
    <html>
        <body>
            <div>
                <ul>
                 <li class="item-0"><a href="link1.html">first item</a></li>
                 <li class="item-1"><a href="link2.html">second item</a></li>
                 <li class="item-inactive"><a href="link3.html">third item</a></li>
                 <li class="item-1"><a href="link4.html">fourth item</a></li>
                 <li class="item-0"><a href="link5.html">fifth item</a></li>
                </ul>
            </div>
        </body>
    </html>
    """
    html = etree.HTML(text)
    result = html.xpath('//*')
    print(result)
    pass


if __name__ == '__main__':
    html_demo()
    pass
