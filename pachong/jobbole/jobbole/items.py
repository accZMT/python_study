# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


# itemloader 是分离数据的另一种 方式  使用itemloader 有一些优势
# 1。默认使用xpath()/css() 这种数据提取方式
# 是将数据的提取和数据的过滤等过程放在一个函数中
# 采用itemloader 这种数据加载方式 可以将数据的提取和分离分成两部分
# 让代码更加清晰，代码更加整洁
# 2、可以将数据的处理的处理函数，单独定义
# 也可以对一个数据使用多个处理函数
# 这样的话对代码的重用有着非常好的实现
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst

class JobboleItemLoader(ItemLoader):
    # 设置输出内容的类型
    # TakeFirst 获取所有数据当中的第一条数据
    # 默认返回的数据为一个列表 列表当中一条数据
    default_output_processor = TakeFirst()


# def changeTitle(value):
#     value = '标题：' + value
#     return value

def get_num(value):
    value = value.split(' ')[1]
    value = 0 if value=='' else int(value)
    return value

class JobboleItem(scrapy.Item):

    # 如果函数以Map..开头 那么内部很大可能是一个可迭代对象
    # 在此处 Mapcompose括号里面可以追加多个参数 每个参数都是一个函数
    # 那么获取的内容 会依次进入到每个函数当中被执行
    img_src = scrapy.Field()
    title = scrapy.Field()
        # input_processor = MapCompose(changeTitle,lambda x:x+'*'*6)
    # )
    date = scrapy.Field(
        input_processor = MapCompose(lambda x:x.strip().replace(' ·',''))
    )
    detail_url = scrapy.Field()
    like = scrapy.Field(input_processor=MapCompose(lambda x:int(x)))
    collect = scrapy.Field(
        input_processor = MapCompose(get_num)
    )
    comment = scrapy.Field(input_processor=MapCompose(get_num))
