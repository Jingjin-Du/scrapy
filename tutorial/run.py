# -*- coding: UTF-8 -*-
from datetime import datetime
import time
import os



# 每n秒执行一次
def timer(n):
    for i in range(0, n):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("爬取一次")
        os.system("scrapy crawl mifeng")
        #os.system("scrapy crawl dmoz")
        time.sleep(5)


# 时间
timer(1)
