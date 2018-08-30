# -*- coding: utf-8 -*-


import scrapy
from selenium import webdriver
from ..items import TaobaoItem

class PhoneSpider(scrapy.Spider):
    name = 'phone'
    allowed_domains = ['s.taobao.com']
    total_page = 20

    start_urls = ['https://s.taobao.com/search?q=%E4%B8%80%E5%8A%A0%E6%89%8B%E6%9C%BA&s={}'.format(i*44) for i in range(total_page)]


    def __init__(self):

        # 配置谷歌浏览器无图和无界面模式
        self.options = webdriver.ChromeOptions()
        self.prefs = {
            'profile.default_content_setting_values':{'images':2}
        }
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_experimental_option('prefs',self.prefs)

        self.driver = webdriver.Chrome(chrome_options=self.options)

    def parse(self, response):

        data_list = response.xpath('//div[@class="item J_MouserOnverReq  "]')

        for data in data_list:

            info = ''.join(data.xpath('.//div[@class="row row-2 title"]/a/text()').extract()).strip().replace('/','')
            price = data.xpath('.//div[@class="price g_price g_price-highlight"]/strong/text()').extract_first()
            shop = data.xpath('.//a[@class="shopname J_MouseEneterLeave J_ShopInfo"]/span[2]/text()').extract_first()
            img_src = "https:" + data.xpath('.//a[@class="pic-link J_ClickStat J_ItemPicA"]/img/@data-src').extract_first()

            item = TaobaoItem()

            item['info'] = info
            item['price'] = price
            item['shop'] = shop
            item['img_src'] = [img_src]

            yield item

        # 获取总页数
        # self.total_page = response.xpath('//div[@class="total"]/text()').re_first('\d+')


    @staticmethod
    def close(spider, reason):

        spider.driver.close()
        return


