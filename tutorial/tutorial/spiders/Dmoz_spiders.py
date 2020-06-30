import scrapy

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["www.feixiaohao.com"]
    start_urls = [
        #"https://www.feixiaohao.com/#USD",
        "https://www.feixiaohao.com/currencies/okb/"
    ]
    '''
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]
    '''

    need_keys = ['现价', '目前市值排名', '换手率', '24H最高', '24H最低', '7D最高', '7D最低', '24H涨幅', '7D涨幅', '今年来', '24H交易量', '24H交易额', '24H净流入']
    need_keys = ['24H涨幅', '7D涨幅', '今年来', '24H净流入']

    def parse(self, response):
        #filename = response.url.split("/")[-2]
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
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
        

        

        

