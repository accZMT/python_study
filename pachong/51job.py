
# 51job
# 爬取任意城市的python岗位
# 包含公司名称
# 存入execl中

from urllib.request import Request,urlopen
import re
import json
import xlwt
from urllib.parse import quote
import string
import time

class JobSpider(object):
    def __init__(self,cityList=[],workName=""):
        self.old_work_name = workName
        self.base_url = "https://search.51job.com/list/{},000000,0000,00,9,99,{},2,{}.html"
        self.total_page = 1
        self.cityString = ""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        # 将获取的字典反转
        self.cityDic = {v: k for k, v in self.get_city_info().items()}
        # 或者使用通过 值获取对应的键 list(dic.keys())[list(dic.values()).index(2)]
        # 如果没有选择城市默认为全国
        if len(cityList) == 0:
            self.cityString = '000000'
        else:
            # 以下代码为：如果城市名输入错误进行错误处理
            for cityName in cityList:
                if cityName in self.cityDic:
                    if cityName == cityList[-1]:
                        self.cityString+=self.cityDic[cityName]
                    else:
                        self.cityString += self.cityDic[cityName] + "%252C"
                else:
                    print("******{}城市输入错误******".format(cityName))
            if len(self.cityString) == 0:
                self.cityString = '000000'
        # 职位处理
        if len(workName) == 0:
            self.workName = '%2520'
        else:
            self.workName = quote(workName,string.printable)

    def get_city_info(self):
        # 获取城市对应的ID
        url = "https://js.51jobcdn.com/in/js/2016/layer/area_array_c.js?20180319"
        request = Request(url,headers=self.headers)
        code = urlopen(request).read().decode("gbk")
        pattern = re.compile(r'.*?area=(.*?);',re.S)
        result = pattern.findall(code)
        return json.loads(result[0])

    def get_code(self,pageIndex=1):
        # 获取网页源码
        url = self.base_url.format(self.cityString,self.workName,pageIndex)
        print(url)
        try:
            request = Request(url,headers=self.headers)
            code = urlopen(request).read().decode("gbk")
        except Exception as e:
            print("请求失败",e)
        else:
            return code

    def get_total_page(self,code):
        # 获取所有页数
        pattern = re.compile(r'共(\d+)页，到第',re.S)
        total_page = pattern.findall(code)[0]
        self.total_page=int(total_page)

    def get_all_data(self,code):
        # 提取数据
        pattern = re.compile(r'<p class="t1 ">.*?<a.*?title="(.*?)".*?>.*?<span class="t2">.*?<a.*?title="(.*?)".*?>.*?<span class="t3">(.*?)</span>.*?<span class="t4">(.*?)</span>',re.S)
        result = pattern.findall(code)
        return result

    def open_sheet_table(self):
        # 创建execl表
        workBook = xlwt.Workbook(encoding="utf-8")
        sheet = workBook.add_sheet(self.old_work_name+"职位")
        lista = ["职位名","公司名","工作地点","薪资"]
        for y,i in enumerate(lista):
            sheet.write(0,y,i)
        return sheet,workBook
    def start_spider(self):
        # 程序入口
        code = self.get_code(1)
        self.get_total_page(code)
        sheet,workBook = self.open_sheet_table()
        x = 1
        for index in range(1,self.total_page+1): #self.total_page+1
            time.sleep(1)
            code = self.get_code(index)
            results = self.get_all_data(code)
            if len(results) == 0:
                print("对不起，没有找到符合你条件的职位！")
                continue
            for result in results:
                for y,res in enumerate(result):
                    # x 代表行，y代表列  res代表值
                    sheet.write(x,y,res)
                x += 1
            workBook.save("51job招聘信息4.xls")

if __name__ == "__main__":
    cityList = []
    while 1:
        city = input("请输入你想去的城市,按Q退出：")
        if city == "Q":
            break
        cityList.append(city)
    work = input("请输入你喜欢的工作：")

    # job = JobSpider(["北京","上海"],"python")
    job = JobSpider(cityList,work)
    job.start_spider()



