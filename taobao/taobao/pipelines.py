# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import scrapy
import sqlite3
import xlwt
from urllib.request import urlretrieve
from scrapy.exporters import JsonItemExporter


class UrllibPipeline(object):
    def process_item(self, item, spider):
        urlretrieve(item["img_src"][0],"imgs/"+item["info"]+".jpg")
        return item

class JsonFilePipeline(object):

    def __init__(self):
        self.file = open('taobao.json','wb')
        self.exporter = JsonItemExporter(self.file,ensure_ascii=False,encoding='utf-8')

    def open_spider(self,spider):
        self.exporter.start_exporting()

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()


class TaobaoPipeline(object):
    def __init__(self):
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.workbook.add_sheet('一加手机')
        self.info_list = ['info','price','shop','img_src']
        self.row = 1
    def open_spider(self,spider):

        for index,info in enumerate(self.info_list):
            self.sheet.write(0,index,info)

    def close_spider(self,spider):

        self.workbook.save("Taobao.xlsx")

    def process_item(self, item, spider):

        data_list = [item["info"],item["price"],item["shop"],item["img_src"]]

        for index,data in enumerate(data_list):
            self.sheet.write(self.row,index,data)
        self.row += 1
        return item


class SqlitePipeline(object):

    def __init__(self):
        self.conn = sqlite3.connect('taobaoDB')
        self.cursor = self.conn.cursor()

    def open_spider(self,spider):

        self.cursor.execute('create table if not exists phone (img text,info text,price text,shop text)')
        self.conn.commit()

    def process_item(self,item,spider):

        self.cursor.execute(f'insert into phone VALUES ("{item["img_src"]}","{item["info"]}","{item["price"]}","{item["shop"]}")')
        self.conn.commit()

        return item
    def close_spider(self,spider):

        self.conn.close()

class DownloadImagePipeline(ImagesPipeline):


    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['img_src'][0],meta={"item":item})

    def file_path(self, request, response=None, info=None):

        name = request.meta["item"]["info"]

        return name+".jpg"
