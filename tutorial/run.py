# -*- coding: UTF-8 -*-
from datetime import datetime
import time
import os
import sys
from bs4 import BeautifulSoup

file = 'data.out'

def getData():
    with open(file, 'r') as f:
        out = f.read().split(' ')
        if len(out) == 0:
            print("爬取出错，数据为空")
            return
        line = []
        for it in out:
            if len(it) == 0:
                continue
            line.append(it)
        data = []
        data.append(line[-1])   #最后一个，市场总值
        data.append(line[1])    #市值排名        
        data.append(line[10])   #24H交易量
        data.append(line[7])    #24H涨幅
        data.append(line[8])    #7D涨幅
        data.append(line[9])    #今年来涨幅
        print(data)
        return data

def change(data):
    import os
    from bs4 import BeautifulSoup #引入BeautifulSoup
    
    fp = open("项目详情页.html",'r+',encoding="utf-8")
    soup = BeautifulSoup(fp, 'lxml')
    #获取所有label
    label_all = soup.findAll(class_="item-label")#搜索class为name的tag
    label_0_2 = []
    label_0_2.append(label_all[0])
    label_0_2.append(label_all[2])
    print(label_0_2)
    print(len(label_0_2))

    labels = soup.findAll(class_="ok-ui-pop-placement")#搜索class为name的tag
    print(labels)
    print(len(labels))

    #获取所有值
    value = soup.findAll(class_="item-value")#搜索class为name的tag
    print(value)
    print(len(value))

    #修改数据
    for i in range(0, 6):
        if i == 0 or i ==2:
            label_all[i].string = data[i].split(':')[0]
        elif i == 1 :
            labels[i-1].string = data[i].split(':')[0]
        else:
            labels[i-2].string = data[i].split(':')[0]
        value[i].string = data[i].split(':')[1]

    fp.seek(0,os.SEEK_SET)#移动到文件头
    fp.write(str(soup))#重写整个文件
    fp.close()


# 总共执行几次
def pa(n):
    for i in range(0, n):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("爬🥧")
        
        mifengcha = 0
        if mifengcha is True :
            os.system("scrapy crawl mifeng")
        else:
            os.system("scrapy crawl dmoz")

        with open(file, 'r') as f:
            out = f.read().split(' ')
            if len(out) == 0:
                print("爬取出错，数据为空")
            else:
                for it in out:
                    print(it)

        data = getData()
        change(data)
        
        clear = ""
        with open(file, 'w') as f:
            f.write(clear)
        
        print("停🛑")
        #time.sleep(5)

# 时间
pa(1)
#data = getData()
#change(data)