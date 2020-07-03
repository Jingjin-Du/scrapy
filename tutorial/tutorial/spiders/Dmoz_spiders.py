import scrapy
import re
import json
import urllib.request

key_name = {'现价' : 'price', '目前市值排名': 'rank', '换手率' : 'hand', '24H最高' : 'day_max', '24H最低' : 'day_min', '7D最高' : 'week_max', '7D最低' : 'week_min', '24H涨幅' : 'day_add', '7D涨幅' : 'week_add', '今年来' : 'now_year', '24H交易量' : 'day_action_num', '24H交易额' : 'day_action', '24H净流入' : 'day_in'}

key_value = {'price' : '', 'rank': '', 'hand' : '', 'day_max' : '', 'day_min' : '', 'week_max' : '', 'week_min' : '', 'day_add' : '', 'week_add' : '', 'now_year' : '', 'day_action_num' : '', 'day_action' : '', 'day_in' : ''}

usdturl = "http://webforex.hermes.hexun.com/forex/quotelist?code=FOREXUSDCNY&column=Code,Price"
req = urllib.request.Request(usdturl)
f = urllib.request.urlopen(req)
html = f.read().decode("utf-8")
print(html)

s = re.findall("{.*}",str(html))[0]
sjson = json.loads(s)

USDCNY = sjson["Data"][0][0][1]/10000
print(USDCNY)

urls = {
        "非小号官网" : "https://www.feixiaohao.com/#USD",
        "非小号okb" : "https://www.feixiaohao.com/currencies/okb/",
        "非小号杂乱数据" : "https://dncapi.bqiapp.com/api/coin/coinchange?code=okb&webp=1",
        "非小号一周内价格" : "https://dncapi.bqiapp.com/api/coin/web-charts?code=okb&type=w&webp=1",
        "非小号一天内价格" : "https://dncapi.bqiapp.com/api/coin/web-charts?code=okb&type=d&webp=1",
        "非小号手机端" : "https://m.feixiaohao.com/currencies/okb/",
        "aicoin" : "https://www.aicoin.cn/currencies/okb.html",
        }

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["www.feixiaohao.com"]
    start_urls = [
        urls["非小号杂乱数据"],
        urls["非小号一周内价格"],
        urls["非小号一天内价格"],
        urls["非小号手机端"],
        urls["aicoin"]
    ]
    '''
    allowed_domains = ["dmoz.org"]
    start_urls = [
        #涨幅
        "https://dncapi.bqiapp.com/api/coin/coinchange?code=okb&webp=1",

        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]
    '''

    need_keys = ['现价', '目前市值排名', '换手率', '24H最高', '24H最低', '7D最高', '7D最低', '24H涨幅', '7D涨幅', '今年来', '24H交易量', '24H交易额', '24H净流入']
    need_keys = ['24H最高', '24H最低', '7D最高', '7D最低'] 

    def usd_cny(self, usd, num):
        return str(round(float(usd)/float(USDCNY), num))

    def parse(self, response):
        '''
        filename = response.url.split("/")[-3] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        '''
        if response.url == urls["aicoin"]:
            self.aicoin(response)
        if response.url == urls["非小号杂乱数据"]:
            self.feixiaohao_data(response)
        if response.url == urls["非小号手机端"]:
            self.feixiaohao_m(response)
        if response.url == urls["非小号一周内价格"]:
            self.feixiaohao_week_data(response)
        if response.url == urls["非小号一天内价格"]:
            self.feixiaohao_day_data(response)
        
        print(key_value)
        self.construct()
        
    #净流入
    def aicoin(self, response):
        day_action = float(response.css('span.deg_down').css('span::text').extract()[0].replace(',',''))
        day_action = self.usd_cny(day_action, 3) + "万"
        if day_action[0] == '-':
            key_value['day_in'] = day_action[0] + '$' + day_action[1 : ]
        else :
            key_value['day_in'] = '+$' + day_action

    #24H涨幅，一周涨幅，今年来
    def feixiaohao_data(self, response):
        data = str(response.body, encoding = "utf8")
        dic = json.loads(data)['data']

        key_value['day_add'] = str(dic['change_day']) + '%'
        key_value['week_add'] = str(dic['change_week']) + '%'
        key_value['now_year'] = str(dic['change_thisyear']) + '%'

    #24H最大最小  一周最大最小
    def feixiaohao_week_data(self, response):
        data = str(response.body, encoding = "utf8")
        data = json.loads(data)['value']
        print(type(data))
        data = data[1:-1].split("],[")
        price = []
        for it in data:
            price.append(float(it.split(",")[1]))
        price_week = []
        for i in range(0, len(price)):
            price_week.append(price[i])
        key_value['week_max'] = '$' + str(round(max(price_week), 3))
        key_value['week_min'] = '$' + str(round(min(price_week), 3))

    #24H最大最小
    def feixiaohao_day_data(self, response):
        data = str(response.body, encoding = "utf8")
        data = json.loads(data)['value']
        print(type(data))
        data = data[1:-1].split("],[")
        price = []
        for it in data:
            price.append(float(it.split(",")[1]))
        price_day = []
        for i in range(0, len(price)):
            price_day.append(price[i])
        key_value['day_max'] = '$' + str(round(max(price_day), 3))
        key_value['day_min'] = '$' + str(round(min(price_day), 3))

    #现价，排名，换手率，24H交易量 交易额
    def feixiaohao_m(self, response):
        price = response.css('div.sub_price')[0].css('span::text').extract()[1]
        price = round(float(price), 2)
        key_value['price'] = '$' + str(price)
        rank = response.css('h1.coin_name').css('div')[-1].css('span::text').extract()[0]
        key_value['rank'] = rank[3:]
        key_value['hand'] = response.css('div.item')[4].css('span::text').extract()[1]
        key_value['day_action_num'] = response.css('div.item')[2].css('span::text').extract()[1].replace(",", "")

        action = response.css('div.item')[3].css('span::text').extract()[2]
        key_value['day_action'] = '$' + self.usd_cny(action[:-1], 2) + action[-1]

    


    def feixiaohao(self, response):
        output = {}
        info_list = response.css('div.info_list')
        info_tit = info_list.css('span.info_tit::text').extract()
        convert = info_list.css('span.convert::text').extract()
        for i in range(0, len(convert)-1):
            if i == 6 :
                continue
            output[info_tit[i]] = convert[i]
        #排名
        rankstr = response.css('div.tag').extract()[0]
        rankflag = rankstr.find('.')
        rank = rankstr[rankflag+1 : rankflag+4]
        rankflag = rank.find('<')
        rank = rank[ : rankflag]
        key_value['rank'] = rank

        #现价
        sub = response.css('div.sub')
        convert = float(sub.css('span.convert::text').extract()[0])
        output['现价'] = str(convert)
        convert = round(convert/float(USDCNY), 2)
        key_value['price'] = '$' + str(convert)

        #换手率
        charbox = response.css('div.charbox')[2]
        val = charbox.css('div.val::text').extract()[0]
        key_value['hand'] = val
        
        print(output)




    def construct(self):
        print(str(key_value))
        output = ""
        for key, value in key_name.items():
            col = key + ":" + key_value[value]
            output += col+"  "
        with open('feixiaohao.out', 'w') as f:
            f.write(output)
        

        

