# -*- coding:utf-8 -*-
import re
import os
import sys
import time
import random
import requests

class mmspider():

    def __init__(self):
        self.count = 0
        self.page_number = 1
        try:
            self.current_path = sys.path[0]
            self.filepath = self.current_path + "/save/"
            os.mkdir(self.filepath)
        except Exception as e:
            print(e)
        self.getpage()

    def getpage(self):
        url_primary = "http://www.qiushimm.com/page/%s" % self.page_number
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                      " Chrome/56.0.2924.87 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate, sdch",
                        "Accept-Language": "zh-CN,zh;q=0.8",
                        "Host": "www.qiushimm.com",
                        "Referer": url_primary}
        try:
            req = requests.get(url_primary, headers=self.headers)
            self.analyze(str(req.content))
        except Exception as e:
            print(e)
			
	#获取图片链接并去除无效链接
    def analyze(self, page_content):
        pattern = re.compile("<img src=\"(.*?)\"", re.S)
        for result in re.findall(pattern, page_content):
            if "trans" not in result:
                result = str(result)
                self.getmm(result)
        self.page_number += 1
        self.getpage()	#循环翻页
		
	#取出文件名并保存到相应的文件类型
    def getmm(self, mm_url):
        self.count += 1
        print("Downloading image No.%s" % self.count)
        filename = re.sub("http://\D{2}\d\.sinaimg.cn/(\D{2,4}\d{1,6}|large)/", "", mm_url)
        filepath = self.filepath + filename
        req = requests.get(mm_url)
        if req.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(req.content)
		#判断文件大小，如果小于6Kb自动删除
        if os.path.getsize(filepath)/1024 <= 6:
            print("Image No.%s is empty, deleting..." % self.count)
            os.remove(filepath)
        time.sleep(random.randint(3, 5))

if __name__ == "__main__":
    spider = mmspider
    spider()
