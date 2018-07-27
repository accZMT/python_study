

"""根据输入的类别，获取www.169we.com中的所有图片"""

# coding:utf-8
import requests,os
import re
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

# base_url = "http://www.169we.com/diannaobizhi/list_7_1.html"

class Pic169Spider(object):
    def __init__(self,category):
        self.category = category
        self.base_url = "http://www.169we.com/{}/".format(self.category)

        self.headers = {
            "User-Agent":UserAgent().random,
            "Host":"www.169we.com",
        }
        self.img_headers = {
            "User-Agent": UserAgent().random,
            "Host": "724.169pp.net",
        }
        self.dic = {
        "diannaobizhi":"7",
        "shoujibizhi":"6",
        "wangyouzipai":"2",
        "gaogensiwa":"3",
        "xiyangmeinv":"4",
        "guoneimeinv":"5",
        "xingganmeinv":"1"
        }
    def getIndexPage(self,url):
        """获取图片分类的总页数"""
        response = requests.get(url,headers=self.headers)
        soup = BeautifulSoup(response.text,"lxml")
        page_all = soup.select('body  div.page  ul li a')
        return page_all[-3].get_text()

    def getPage(self, url):
        """获取图片的总页数"""
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, "lxml")
        page_all = soup.select('body  div ul.pagelist li a')
        return page_all[-2].get_text()

    def getIndexImgHref(self,url):
        response = requests.get(url,headers=self.headers)
        response.encoding="gbk"
        data = re.findall(r'<li><a href="(.*?)" class="pic".*?>.*?<p>(.*?)</p>',response.text,re.S)
        return data

    def getImgUrl(self,url,dirname,index):
        """获取图片的src"""
        if not os.path.exists(self.category + "/" +dirname):
            os.makedirs(self.category + "/" +dirname)
        response = requests.get(url, headers=self.headers)
        # response.encoding = "gbk"
        img_urls = re.findall(r'<p align="center">.*?<img src="(.*?)".*?</p>',response.text,re.S)
        for img_url in img_urls:
            self.saveImg(img_url,dirname,index)
            index+=1

    def saveImg(self,img_url,dirname,index):
        """保存图片到本地"""

        result = requests.get(img_url,headers=self.img_headers)
        with open(self.category + "/" + dirname +"/"+ str(index) + ".jpg", "wb") as f:
            f.write(result.content)
            # time.sleep(1)

    def main(self):
        """主函数"""
        if not os.path.exists(self.category):
            os.makedirs(self.category)
        pages = int(self.getIndexPage(self.base_url))
        for page in range(1,pages+1):
            print(page)
            num = self.dic[self.category]
            url = "http://www.169we.com/{}/list_{}_{}.html".format(self.category,num,page)
            for data in self.getIndexImgHref(url):
                old_url = data[0]
                dirname = data[1]
                for i in range(1,int(self.getPage(old_url))+1):
                    if i == 1:
                        new_url = old_url
                    else:
                        lista = old_url.split(".")
                        lista[-2] = lista[-2] + "_{}".format(i)
                        new_url = ".".join(lista)
                    self.getImgUrl(new_url,dirname,i)


if __name__ == "__main__":
    msg = """
            提示信息：
            diannaobizhi--——>电脑壁纸
            shoujibizhi--——>手机壁纸
            wangyouzipai--——>网友自拍
            gaogensiwa--——>高跟丝袜
            xiyangmeinv--——>西洋美女
            guoneimeinv--——>国内美女
            xingganmeinv--——>性感美女

    """
    print(msg)
    category = input("请输入你要获取的类别名：")
    diannaobizhi = Pic169Spider(category)
    diannaobizhi.main()
    