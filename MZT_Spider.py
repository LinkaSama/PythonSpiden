#!/usr/bin/env python
# -*- encoding: utf-8 -*- 


"""
@version: ??
@Python version:3.5.2
@author: Savior
@license: Apache Licence 
@contact E-mail: 558405@qq.com  
@site: 
@software: PyCharm
@file: mzitu.py
@time: 2021/7/8 11:53
"""

import os , requests, time,random
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from lxml import etree
from fake_useragent import UserAgent




class Mzitu:
    def __init__(self):

        pass





    def run(self):


        frist_url = "https://www.mzitu.com/page/{}/"

        self.start_url = 1  # input('起始页码>>:')
        self.end_url = 1  # input('结束页码>>:')

        all_info=[frist_url.format(i) for i in range(int(self.start_url), int(self.end_url) + 1)]

        print(all_info)

        get_url = self.get_all_url(all_info)

    def res(self,url):
        time.sleep(random.random())
        self.ua = ua.random
        self.headers = {'User-Agent': ua.random,
                        'Referer': 'https://www.mzitu.com/'}

        res=requests.get(url,headers=self.headers)
        # print(res.text)

        return res

    def get_all_url(self, all_info):

        for i in all_info:

            res = self.res(i)
            et=etree.HTML(res.text)
            urls=et.xpath('//ul[@id="pins"]/li/a/@href')
            print(urls)

            for j in urls:
                queue.put(j)

    def get_picture_info(self,url):
        picture_info = {}

        res = self.res(url)

        et=etree.HTML(res.text)
        title=et.xpath('/html/body/div[2]/div[1]/h2/text()')[0]

        picture_info['title'] = title

        max_page=et.xpath('/html/body/div[2]/div[1]/div[4]/a[5]/span/text()')[0]

        get_photo = et.xpath("//img[@class='blur']/@src")[0].split('/')[-1].replace('01.jpg','')



        get_best_url=et.xpath("//img[@class='blur']/@src")[0].rsplit('.',1)[0].rsplit('/',1)[0]

        # ulrs=[get_best_url+"/"+str(get_photo)+str(i)+'.jpg' for i in range(1,int(max_page))]
        #
        # print(ulrs)

        ulrs=[]

        for i in range(1,int(max_page)+1):

            if i < 10:

                A_url=get_best_url+"/"+str(get_photo)+str(0)+str(i)+'.jpg'
                ulrs.append(A_url)



            else:
                B_url=get_best_url+"/"+str(get_photo)+str(i)+'.jpg'

                ulrs.append(B_url)

        picture_info['src']=ulrs










        
        # src_list=[]
        # for u in all_page:
        #     print(u)
        #     resp= self.res(u)
        #     et=etree.HTML(resp.text)
        #     src=et.xpath("//img[@class='blur']/@src")[0]
        #     print(src)


    #         src_list.append(src)
    #
    #     picture_info['src']=src_list
    #     # print(src_list)
    #     #
        # print(picture_info)
        self.download(picture_info)

    def download(self,picture_info):

        print(picture_info)
        self.downtime = time.time()
        title = picture_info['title']
        # file_path = 'r18file' + '/' + str(self.start_page + '-' + self.end_page) + '/' + title + '/'

        file_path= 'mzitu'+'/'+str(self.start_url)+'-'+str(self.end_url)+'/' + title + '/'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        # print('正在下载', title, '|剩余',end='')
        maxpage=len(picture_info['src'])
        # print()
        k = 1

        for url in picture_info['src']:


            print()

            time.sleep(0.03)



            name = url.split('/')[-1]
            time.sleep(random.random())
            headers = {'User-Agent': self.ua,
                       'Referer': 'https://www.mzitu.com/'}

            res = requests.get(url, headers=headers)
            print('正在下载',url)
            with open(file_path + str(name), mode='wb') as f:
                f.write(res.content)


        end_down_time = time.time()
        print('已下载完成', title, "|耗时:", end_down_time - self.downtime)


























if __name__ == '__main__':
    stime = time.time()
    queue = Queue()
    ua = UserAgent()

    spider = Mzitu()
    spider.run()
    pool = ThreadPoolExecutor(max_workers=1)

    while queue.qsize() > 0:
        pool.submit(spider.get_picture_info, queue.get())