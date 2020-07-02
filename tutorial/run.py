# -*- coding: UTF-8 -*-
from datetime import datetime
import time
import os
import sys


# 每n秒执行一次
def timer(n):
    for i in range(0, n):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("爬取一次")
        os.system("scrapy crawl mifeng")
        #os.system("scrapy crawl dmoz")
        time.sleep(5)

        with open('data.out', 'r') as f:
            out = f.read().split(' ')
            for it in out:
                print(it)


# 时间
timer(1)
