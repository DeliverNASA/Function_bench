from functools import wraps
import time
import os
from threading import Thread

TIME_LIMIT = 6

def set_time_limit():
    def auto_quit():
        '''此为控制进程超时退出的线程函数'''
        time.sleep(TIME_LIMIT)
        # print("time out {}".format(t1))
        os._exit(1) #此函数专门用于线程控制主进程退出，有兴趣的可以看一下和sys.exit()的区别
    def decorator(f):
        '''此函数用于传入被装饰函数f'''
        @wraps(f)
        def wrapper(*args,**kwargs):
            '''装饰器内部遵循的逻辑是：
            1.auto_quit先执行完，进程结束
            2.被修饰函数f先执行完，auto_quit函数停止执行
            3.被修饰函数执行完，下面的代码才能运行
            '''
            # t1：时间监督函数
            # t2：目标执行函数
            t1=Thread(target=auto_quit,)  #此处的t是set_time_limit函数的形参，是auto_quit函数的实参
            t2=Thread(target=f,args=args,kwargs=kwargs)
            t1.setDaemon(True) #满足第2点
            t1.start()
            t2.start()
            t2.join() #满足第3点
        return wrapper
    return decorator