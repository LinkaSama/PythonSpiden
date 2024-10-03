 
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/5/25 19:32 五月
# @Author : ikaoser
# @Email : 5584805@qq.com
# @File : r18com.py
# @Project : PYthonProjact
 
 
import os, requests, time, random
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from lxml import etree
from fake_useragent import UserAgent
class R18com:
 
    def __init__(self):
 
        self.ua=UserAgent()
 
        self.headers={
            "User-Agent": self.ua.random,
            "Referer": "https://www.r18.com"
        }
 
    def resp(self,url):
        # print(url)
        time.sleep(0.1)
        res=requests.get(url=url,headers=self.headers)
        if res.status_code==200:
            return etree.HTML(res.text)
        else:
            return
 
 
 
 
    def Get_all_urls(self,url_list):
 
 
        for url in url_list:
 
 
            res=self.resp(url)
 
            links=res.xpath('//li[@data-tracking_id="video"]/a/@href')
 
            for url in links:
                print('构造链接',url)
 
                queue.put(url)
 
 
 
 
 
    def run(self):
        self.start_page=input('起始页码~~：')
        self.end_page=input('结束页码~~：')
 
        start_url="https://www.r18.com/videos/vod/movies/list/pagesize=30/price=all/sort=popular/type=all/page="
 
        url_list=[start_url+str(i) for i in (int(self.start_page),int(self.end_page)+1)]
        # print(url_list)
        get_all_url=self.Get_all_urls(url_list)
 
        print('开始你的表演！！！')
 
 
    def down(self,url):
 
        picture_info = {}
        # print(url)
        res=self.resp(url)
 
 
        one_photo=res.xpath('//*[@id="contents"]/div[10]/div[1]/section/section/section[4]/div/img/@src')[0]
        # 封面图片
        page_src = res.xpath('//ul[@class="js-owl-carousel clearfix"]/li/p/img/@data-src')
        # 番号组图
        name = res.xpath('//*[@id="contents"]/div[10]/div[1]/section/section/section[1]/div[3]/dl[2]/dd[3]/text()')[0].strip()
        videos = res.xpath('//*[@id="contents"]/div[10]/div[1]/section/section/section[1]/div[1]/div[2]/p/a/@data-video-low')[0]
 
 
        new_pic=page_src
        new_pic.append(one_photo)
 
 
 
        if len(videos)>10:
            new_pic.append(videos)
            # print(new_pic)
 
        picture_info['urls'] = new_pic
 
        picture_info['title']=name
 
        self.download(picture_info)
 
    def download(self,picture_info):
        self.downtime = time.time()
        title = picture_info['title']
 
 
 
 
        file_path='r18file'+'/'+str(self.start_page+'-'+self.end_page)+'/'+title+'/'
 
        if not os.path.exists(file_path):
            os.makedirs(file_path)
 
        for url in picture_info['urls']:
 
            time.sleep(0.03)
            name = url.split('/')[-1]
            res=requests.get(url,headers=self.headers)
            with open(file_path+str(name),mode='wb') as f:
                f.write(res.content)
 
        end_down_time=time.time()
 
        print('已下载完成',title,"|耗时:",end_down_time-self.downtime)
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
if __name__ == '__main__':
 
    queue = Queue()
 
    spider=R18com()
 
    spider.run()
 
    pool=ThreadPoolExecutor(max_workers=9)
 
    while queue.qsize()>0:
        pool.submit(spider.down,queue.get())
 