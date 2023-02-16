"""
处理字符串:
json.dumps(): 对数据进行编码。对象转换为json数据
json.loads(): 对数据进行解码。json数据转换成对象

处理文件:
json.dump()
json.load()
"""
import json
import os


def data_json_demo():
    data = {
        'no': 1,
        'name': 'Runoob',
        'url': 'http://www.runoob.com'
    }
    # Python 字典类型转换为 JSON 对象
    json_str = json.dumps(data)
    print("Python 原始数据：", repr(data))
    print("JSON 对象：", json_str)
    # 将 JSON 对象转换为 Python 字典
    data2 = json.loads(json_str)
    print("data2['name']: ", data2['name'])
    print("data2['url']: ", data2['url'])
    pass


def file_json_dem():
    data = {
        'no': 1,
        'name': 'Runoob',
        'url': 'http://www.runoob.com'
    }

    # os.path.dirname(os.path.realpath(__file__))  获取当前文件所在目录的路径
    path = os.path.dirname(os.path.realpath(__file__)) + "/doc/data.json"

    # 打开指定路径的文件
    with open(path, 'w') as f:
        # 写入数据到指定路径中
        json.dump(data, f)

    with open(path, 'r') as f:
        data2 = json.load(f)
        print(data2, type(data2))


if __name__ == '__main__':
    data_json_demo()
    file_json_dem()
    pass
