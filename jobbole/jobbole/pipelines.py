# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
import scrapy

class JobbolePipeline(object):
    # 保存到mysql数据库，需要先新建一个名为jobbole数据库
    def __init__(self):
        self.conn = pymysql.connect(host="localhost",port=3306,user="root",password="123456",db='jobbole',charset='utf8')

        self.cursor = self.conn.cursor()
    def open_spider(self,spider):
        sql = """create table if not exists blog(
        img text,
        title text,
        date_ text,
        detail_text text,
        like_ INT ,
        collect int,
        comment INT
        )engine=InnoDB default charset=utf8"""
        self.cursor.execute(sql)
        self.conn.commit()

    def process_item(self, item, spider):
        values = (item['img_src'],item['title'],item['date'],item['detail_url'],item['like'],item['collect'],item['comment'])
        self.cursor.execute('insert into blog VALUES (%s,%s,%s,%s,%s,%s,%s)',values)

        return item

    def close_spider(self,spider):

        self.conn.commit()
        self.conn.close()

class JsonPipeline(object):
    """保存为json"""
    def __init__(self):
        self.file = open('blog.json','wb')
        self.export = JsonItemExporter(self.file,ensure_ascii=False,encoding='utf-8')

    def open_spider(self,spider):
        print("爬虫开始了")
        self.export.start_exporting()

    def process_item(self,item,spider):
        self.export.export_item(item)
        return item

    def close_spider(self,spider):
        self.export.finish_exporting()
        self.file.close()
        print('爬虫结束了')

class DownloadImagesPipeline(ImagesPipeline):
    """下载封面图片"""
    def get_media_requests(self, item, info):

        src = item['img_src']
        yield scrapy.Request(url=src,meta={'item':item['title']})

    def file_path(self, request, response=None, info=None):

        # 以标题命名
        title = request.meta['item']
        return title + '.jpg'

