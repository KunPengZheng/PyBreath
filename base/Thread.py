import threading
import time


# 从 threading.Thread 继承创建一个新的线程子类，记得定义run方法。
class MyThread(threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        print("开始线程：" + self.name)
        print_time(self.name, self.delay, 5)
        print("退出线程：" + self.name)


exitFlag = 0


def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1


def simple_use():
    try:
        thread1 = MyThread(1, "Thread-1", 1)
        thread2 = MyThread(2, "Thread-2", 2)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        print("退出主线程")
    except:
        print("Error: 无法启动线程")


class MyThread2(threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        print("开启线程： " + self.name)
        # 获取锁，用于线程同步
        threadLock.acquire()
        print_time(self.name, self.delay, 3)
        # 释放锁，开启下一个线程
        threadLock.release()


threadLock = threading.Lock()
threads = []


def print_time2(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1


def sync_thread():
    try:
        # 创建新线程
        thread1 = MyThread2(1, "Thread-1", 1)
        thread2 = MyThread2(2, "Thread-2", 2)

        # 开启新线程
        thread1.start()
        thread2.start()

        # 添加线程到线程列表
        threads.append(thread1)
        threads.append(thread2)

        # 等待所有线程完成
        for t in threads:
            t.join()
        print("退出主线程")
    except:
        print("Error: 无法启动线程")


def song(a, b, c):
    print(a, b, c)
    for i in range(5):
        print("song")
        time.sleep(1)


if __name__ == '__main__':
    # simple_use()
    # sync_thread()

    # 1、使用元组传递 threading.Thread(target=方法名，args=（参数1,参数2, ...）)
    threading.Thread(target=song, args=(1, 2, 3)).start()
    # 2、使用字典传递 threading.Thread(target=方法名, kwargs={"参数名": 参数1, "参数名": 参数2, ...})
    threading.Thread(target=song, kwargs={"a": 1, "c": 3, "b": 2}).start()  # 参数顺序可以变
    # 3、混合使用元组和字典 threading.Thread(target=方法名，args=（参数1, 参数2, ...）, kwargs={"参数名": 参数1,"参数名": 参数2, ...})
    threading.Thread(target=song, args=(1,), kwargs={"c": 3, "b": 2}).start()
    pass
