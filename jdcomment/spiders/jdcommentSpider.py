#coding=UTF-8
from scrapy.selector import  Selector
from scrapy.spiders import CrawlSpider,Rule
from jdcomment.items import JdcommentItem
import json
import re
from scrapy.http import Request
import time
import random
global total
total=['http://sclub.jd.com/productpage/p-695467-s-0-t-3-p-0.html']
class jdcomment(CrawlSpider):
    name="jdcomment"
    start_urls=['http://sclub.jd.com/productpage/p-695467-s-0-t-3-p-1.html']


    def parse(self,response):
        #time.sleep(random.randint(1,10))

        try:
            jscontent=response.body.decode("gbk")
            new_url=re.search('''(.*)-(.*?)\.html''',response.url).group(1)
            num=re.search('''(.*)-(.*?)\.html''',response.url).group(2)
            jsDict = json.loads(jscontent)
            comments=jsDict['comments']
            print response.url
            if response.url is not None or  response.url !="":
                total.append(response.url)
            for each in comments:
                item = JdcommentItem()
                if each['productColor'] ==u"":
                    item['name']=each['nickname']
                    item['comments']=each['content']
                    item['userProvince']=each['userProvince']
                    item['commtime']=each['referenceTime']
                    item['prosize_col']=each['productSize']
                    item['level']=each['userLevelName']
                    if each['userClientShow'] == u"":
                        item['mobile']=" "
                    else:
                        item['mobile']=re.search(">(.*?)<",each['userClientShow']).group(1)
                else:
                    item['name']=each['nickname']
                    item['comments']=each['content']
                    item['userProvince']=each['userProvince']
                    item['commtime']=each['referenceTime']
                    item['prosize_col']=each['productColor']
                    item['level']=each['userLevelName']
                    if each['userClientShow'] ==u"":
                        item['mobile']=" "
                    else:
                        item['mobile']=re.search(">(.*?)<",each['userClientShow']).group(1)
                #print new_url+'-'+str(int(num)+1)+'.html'

                yield item
            yield Request(new_url+'-'+str(int(num)+1)+".html",callback=self.parse)
        except:
            time.sleep(30)
            old_url=total[-1]
            url_body=re.search('''(.*)-(.*?)\.html''',old_url).group(1)
            old_num=re.search('''(.*)-(.*?)\.html''',old_url).group(2)
            yield Request(url_body+'-'+str(int(old_num)+1)+".html",callback=self.parse,dont_filter=True)