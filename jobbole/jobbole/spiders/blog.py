# -*- coding: utf-8 -*-
import scrapy
from ..items import JobboleItem
from ..items import JobboleItemLoader

class BlogSpider(scrapy.Spider):
    name = 'blog'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # 需求 ： 获取所有文章的标题 图片 图片地址 时间 详情页地址
    # 收藏 点赞 评论
    def parse(self, response):

        data_list = response.xpath('//div[@class="post floated-thumb"]')

        for data in data_list:
            img_src = data.xpath('.//div[@class="post-thumb"]/a/img/@src').get()
            detail_url = data.xpath('.//div[@class="post-thumb"]/a/@href').get()

            yield scrapy.Request(detail_url,meta={"img":img_src},callback=self.get_detail_info_with_url)

        next_page = response.xpath('//a[@class="next page-numbers"]/@href')
        if len(next_page) != 0:
            yield scrapy.Request(next_page.get(),callback=self.parse)
    """
    def get_detail_info_with_url(self,response):

        img_src = response.meta['img']
        title = response.xpath('//h1/text()').get()
        date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').get().strip().replace(' ·','')
        detail_url = response.url
        like = int(response.xpath('//h10/text()').get())

        collect = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').get().split(' ')[1]
        collect = 0 if collect == '' else int(collect)

        comment = response.xpath('//span[@class="btn-bluet-bigger href-style hide-on-480"]/text()').get().split(' ')[1]
        comment = 0 if comment == "" else int(comment)

        item = JobboleItem(img_src=img_src,title=title,date=date,detail_url=detail_url,
                           like=like,collect=collect,comment=comment)

        yield item
    """
    def get_detail_info_with_url(self, response):

        # 创建ItemLoader的实例化对象的时候 需要传入两个参数
        # 参数1：item的实例化对象 item里面为还要提取的数据的字段
        # 参数2：网页的源码
        item_loader = JobboleItemLoader(item=JobboleItem(),response=response)

        # add_xpath() 用于给一个field设置值 后面需要追加两个参数
        # 参数1、需要设置的field的名称
        # 参数2、xpath路径
        item_loader.add_xpath('title','//h1/text()')
        item_loader.add_value('img_src',response.meta['img'])
        item_loader.add_xpath('date','//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_value('detail_url',response.url)
        item_loader.add_xpath('like','//h10/text()')
        item_loader.add_xpath('collect','//span[contains(@class,"bookmark-btn")]/text()')
        item_loader.add_xpath('comment','//span[@class="btn-bluet-bigger href-style hide-on-480"]/text()')
        # 将item_loader加载器中保存的每一个field数据收集起来
        # 赋值给item
        item = item_loader.load_item()

        yield item




