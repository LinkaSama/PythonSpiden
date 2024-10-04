#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Wnacg_Spider.py
@Time    :   2024/10/04 00:17:57
@Author  :   小贤切让
@Version :   3.0
@Contact :   5584805@qq.com
'''




import os, requests, time, random
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from lxml import etree




class Wnacg_Spider:

    def __init__(self):

        self.headers = {

            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69",
        }


    def resp(self,url):
        """
        发送HTTP请求并返回响应
        :param url: 请求的URL
        :return: 响应的HTML内容或None
        """
        # print(url)
        time.sleep(0.2)
        res=requests.get(url=url,headers=self.headers)

        if res.status_code==200:

            # print(res.text)
            return etree.HTML(res.text)
        else:
            return None
        
    def get_all_pages(self,url):


        


        res = self.resp(url)

        if res is not None:

            pages = res.xpath('//div[@class="pic_box tb"]/a/@href')[1]  # https://www.wnacg.com/photos-view-id-21379066.html

            self.name=res.xpath('//h2/text()')[0]

            # print(self.name)

            B_page="https://www.wnacg.com"+pages

            res2=self.resp(B_page)

            

            all_pages=res2.xpath('//span[@class="newpagelabel"]/text()')[0].replace('/','')

            all_pages_url =res2.xpath('//img[@id="picarea"]/@src')[0]

            


            F_page_url=all_pages_url.rsplit('/',1)[0]

            

            for i in range(1,int(all_pages)+1):


                if i < 10:



                    page_url="https:" + F_page_url+"/"+"00"+str(i)+".png"

                    queue.put(page_url)

                elif i >= 10 and i < 100:


                    page_url="https:" + F_page_url+"/"+"0"+str(i)+".png"

                    # print(page_url)

                    queue.put(page_url)

                else:


                    page_url="https:" + F_page_url+"/"+""+str(i)+".png"

                    # print(page_url)

                    queue.put(page_url)




                    



                

                    

                # page_url="https:" + F_page_url+"/"+str(i)+".png"

                # print(page_url)
                # queue.put(page_url)


    def Download(self,url):

        
        


        res = self.resp(url)

        file_path="wnacg"+'/'+self.name+"/"

                                        
        if not os.path.exists(file_path):# 检查文件路径是否存在
                                                    
            os.makedirs(file_path)  # 如果文件路径不存在，则创建该路径


        if res is None:

           jpg_url=url.replace('png','jpg')

           

           res=requests.get(url=jpg_url,headers=self.headers)

           with open(file_path+jpg_url.split('/')[-1],'wb') as f:

               f.write(res.content)

               print(jpg_url,"Download successfully~~~")



        else:
           
           

           res=requests.get(url=url,headers=self.headers)

           with open(file_path+url.split('/')[-1],'wb') as f:

               f.write(res.content)

               print(url,"Download successfully~~~")

        
        
        


                      
        

               




           









        






            


            

            

               

            



     














        
        


    def run(self):
        
        
        self.first_url =input("起始页 ,输入第二页的url >>: ")                     #"https://www.wnacg.com/photos-index-page-2-aid-258940.html" # 起始页 ,输入第二页的url

        all_page=self.get_all_pages(self.first_url)

        
    














if __name__ == '__main__':
    stime = time.time()
    queue = Queue()
    spider = Wnacg_Spider()
    spider.run()

    # spider.Download(queue.get())


    pool=ThreadPoolExecutor(max_workers=8)

    while not queue.empty():

        pool.submit(spider.Download,queue.get())
        
    print("总耗时：",time.time()-stime)
    