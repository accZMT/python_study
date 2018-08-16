# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from ..items import ZhilianItemLoader,ZhilianItem
import json


class ZhaopinSpider(RedisCrawlSpider):
    name = 'zhaopin'
    allowed_domains = ['zhaopin.com']

    # start_urls = ['https://fe-api.zhaopin.com/c/i/sou?pageSize=100&cityId=489&lastUrlQuery={%22p%22:99,%22jl%22:%22489%22}']
    redis_key ='zhaopin:start_urls'

    def parse(self, response):

        datas = json.loads(response.text)
        data_list = datas['data']['results']

        print(len(data_list))
        for data in data_list:
            item_loader = ZhilianItemLoader(item=ZhilianItem(),response=response)

            item_loader.add_value('title',data['jobName'])
            item_loader.add_value('company',data['company']['name'])
            item_loader.add_value('salary',data['salary'])
            item_loader.add_value('city',data['city']['display'])

            item = item_loader.load_item()

            print(item)

            yield item


        """
        data_list = response.xpath('//div[@class="infoBox"]')
        for data in data_list:
            item_loader = ZhilianItemLoader(item=ZhilianItem(),response=data)

            item_loader.add_xpath('title','.//span[@class="job_title"]/@title')
            item_loader.add_xpath('company','.//a[@class="company_title"]/@title')
            item_loader.add_xpath('salary','.//p[@class="job_saray"]/text()')
            item_loader.add_xpath('city','.//ul[@class="job_demand"]/li[1]/text()')


            item = item_loader.load_item()

            yield item
            # print(title,company,salary,city)
            """
