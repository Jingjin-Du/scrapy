# -*- coding: UTF-8 -*-
from datetime import datetime
import time
import os
import sys


# 每n秒执行一次
def timer(n):
    for i in range(0, n):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("爬🥧")
        file = ""
        mifengcha = 1
        if mifengcha is True :
            os.system("scrapy crawl mifeng")
            file = 'data.out'
        else:
            os.system("scrapy crawl dmoz")
            file = 'feixiaohao.out'

        with open(file, 'r') as f:
            out = f.read().split(' ')
            if len(out) == 0:
                print("爬取出错，数据为空")
            else:
                for it in out:
                    print(it)
                
        clear = ""
        with open(file, 'w') as f:
            f.write(clear)
        
        print("停🛑")
        #time.sleep(5)


# 时间
timer(1)
