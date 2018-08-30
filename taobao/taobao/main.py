

from scrapy import cmdline

cmdline.execute('scrapy crawl phone'.split())

"""
补充：
之前使用系统下载管道scrapy.pipelines.images.ImagesPipeline和自定义管道DownloadImagePipeline
下载图片都会报 OSError: cannot identify image file <_io.BytesIO object at 0x05762180> 这个错误
不知道怎么搞得。
最后使用之前学习过的urlretrieve可以下载

pipelines.py文件：

from urllib.request import urlretrieve
class UrllibPipeline(object):
    def process_item(self, item, spider):
        urlretrieve(item["img_src"][0],"imgs/"+item["info"]+".jpg")
        return item

settings.py文件：

ITEM_PIPELINES = {
   'taobao.pipelines.TaobaoPipeline': 1,
   'taobao.pipelines.UrllibPipeline': 4,
   # 'taobao.pipelines.DownloadImagePipeline': 3,
   # 'scrapy.pipelines.images.ImagesPipeline':2
}
IMAGES_STORE = 'imgs'

"""