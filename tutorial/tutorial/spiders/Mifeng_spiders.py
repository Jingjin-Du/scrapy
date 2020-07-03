import scrapy
import time

key_name = {'现价' : 'price', '目前市值排名': 'rank', '换手率' : 'hand', '24H最高' : 'day_max', '24H最低' : 'day_min', '7D最高' : 'week_max', '7D最低' : 'week_min', '24H涨幅' : 'day_add', '7D涨幅' : 'week_add', '今年来' : 'now_year', '24H交易量' : 'day_action_num', '24H交易额' : 'day_action', '24H净流入' : 'day_in'}

key_value = {'price' : '', 'rank': '', 'hand' : '', 'day_max' : '', 'day_min' : '', 'week_max' : '', 'week_min' : '', 'day_add' : '', 'week_add' : '', 'now_year' : '', 'day_action_num' : '', 'day_action' : '', 'day_in' : ''}


class MifengSpider(scrapy.Spider):
    name = "mifeng"
    allowed_domains = ["www.mifengcha.com"]
    url = "https://mifengcha.com/api/v1/data/price/history?t=73a51bc2f8ddd39b9839480a2b26cb45&lan=zh&symbol_name=okb&start="
    now_time = round(time.time() * 1000)
    day_ago_time = now_time - 24 * 3600 * 1000
    week_ago_time = now_time - 7 * 24 * 3600 * 1000
    year_time = 1577808000000
    day_ago_url = url + str(day_ago_time) + "&end=" + str(now_time)
    week_ago_url = url + str(week_ago_time) + "&end=" + str(now_time)
    year_url = url + str(year_time) + "&end=" + str(now_time)
    start_urls = [
        #"https://www.feixiaohao.com/currencies/okb/",
        day_ago_url,week_ago_url,year_url,
        "https://www.mifengcha.com/coin/okb"
    ]

    '''
    现价  span.price 
    目前排名 div.market-cap
    换手率 

    24H涨幅  span.change text-green

    24H交易量
    24H交易额  div.item
    24H净流入  div.abs-item
    '''

    def mifengcha(self, response):
        #价格
        key_value['price'] = '$' + response.css('span.price::text').extract()[0]
        #24小时交易额
        key_value['day_action'] = '$' + response.css('span.value::text').extract()[6]
        #24小时净流入
        dayin = response.css('div.abs-item').extract()[6]
        left = dayin.find('</i>')
        right = dayin.find('<!---->')
        key_value['day_in'] = '$' + dayin[left+4 : right]
        #排名
        rank = response.css('div.market-cap').css('span')[1].extract()
        left = rank.find('No.')
        key_value['rank'] = rank[left+3 : ].split('<')[0]


        


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
        output['目前市值排名'] = rank
        #现价
        sub = response.css('div.sub')
        convert = sub.css('span.convert::text').extract()[0]
        output['现价'] = '$'+convert
        #换手率
        charbox = response.css('div.charbox')[2]
        tit = charbox.css('div.tit::text').extract()[0]
        val = charbox.css('div.val::text').extract()[0]
        output[tit] = val

        print(output)


    def mifengchadata(self, response):
        flag = response.url.split("&")
        start = flag[-2].split("=")[-1]
        end = flag[-1].split("=")[-1]
        flag = int((int(end)-int(start))/(24 * 3600 * 1000))

        list = str(response.body, encoding = "utf8").split("],[")
        list[0] = list[0][2:]
        list[-1] = list[-1][:-2]
        prices = []
        for i in range(0, len(list)):
            prices.append(float(list[i].split(",")[1]))
        
        prices_max = round(max(prices), 3)
        prices_min = round(min(prices), 3)
        prices_add = round((prices[-1] - prices[0]) * 100 / prices[0] , 2)
        if flag == 1:
            key_value['day_max'] = '$'+str(prices_max)
            key_value['day_min'] = '$'+str(prices_min)
            key_value['day_add'] = str(prices_add)+"%"
        elif flag == 7:
            key_value['week_max'] = '$'+str(prices_max)
            key_value['week_min'] = '$'+str(prices_min)
            key_value['week_add'] = str(prices_add)+"%"
        else:
            key_value['now_year'] = str(prices_add)+"%"


    def construct(self):
        print(str(key_value))
        output = ""
        for key, value in key_name.items():
            col = key + ":" + key_value[value]
            output += col+"  "
        with open('data.out', 'w') as f:
            f.write(output)
    
    def parse(self, response):
        
        flag = response.url.split("/")[-2]
        print("<"+flag+">")
        if flag == "okb":
            self.feixiaohao(response)
        elif flag == "coin":
            self.mifengcha(response)
        else:
            self.mifengchadata(response)
        self.construct()
        
    
        
                




        

        

        

