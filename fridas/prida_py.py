import os

import frida
import time
import sys

from past.builtins import raw_input


def my_message_handler(message, payload):  # 定义消息处理
    print('message:', message)
    print('payload:', payload)
    if message["type"] == "send":
        payload_ = message["payload"] + "_suffix"
        script.post({"my_data": payload_})


# 获取启动frida-server的安卓机，如果是虚拟机也可以使用get_remote_device
device = frida.get_usb_device()

# 启动`demo02`这个app
pid = device.spawn(["com.zkp.breath"])
device.resume(pid)
time.sleep(1)

# 连接指定pid的进程
process = device.attach(pid)

# os.path.dirname(os.path.realpath(__file__))  获取当前文件所在目录的路径
path = os.path.dirname(os.path.realpath(__file__)) + "/fridaJs.js"

# 加载指定脚本
with open(path) as f:
    script = process.create_script(f.read())
script.on("message", my_message_handler)  # 注册消息处理函数，参数一是事件的名称，表示脚本接收到消息时触发的事件。
script.load()  # 加载脚本

# 等待 Frida 脚本执行完毕，确保脚本已经加载并且执行了对应的导出函数。
time.sleep(2)

#  Script.exports 未来的版本可以能会变成异步的，所以建议使用exports_sync进行替换
result = script.exports_sync.rpc1()  # 执行rpc导出的函数
print("Result:", result)

# raw_input() 会让程序在用户输入之前暂停。
raw_input("Press Enter to exit...")
