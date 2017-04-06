# coding:utf-8
import random
import re
import threading
import time
import urllib2
from Queue import Queue

import pymysql.cursors
from lxml import etree

conn = pymysql.connect(host='localhost', user='root', passwd='', charset='utf8')
cur = conn.cursor()
cur.execute('create database if not exists lagou')
conn.select_db('lagou')
sql = "INSERT IGNORE INTO `lagou_company` VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

repace = re.compile(r'leaders":\[(.*?)\]')
repace1 = re.compile(r'history":\[(.*?)\]')
repace2 = re.compile(r'"companyProfile\"\:\"(.*?)\"')
threadLock = threading.Lock()
# html=requests.get('https://www.lagou.com/gongsi/10.html')
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

q_queue = Queue()
file_object = open('proxy.txt')  # proxy.txt保存可用代理ip
ip_lists = file_object.readlines()


def crawl():
    time.sleep(1)
    while not q_queue.empty():
        url = q_queue.get()
        time.sleep(1)
        header = {'User-Agent': random.choice(USER_AGENTS)}
        proxy = {'http': 'http://%s:%s' % (random.choice(ip_lists).split(':')[0], 8080)}  # 随机抽取ip
        try:
            # req=requests.get(url,headers=header,timeout=60,proxies=proxy)
            proxy_handler = urllib2.ProxyHandler(proxy)
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)
            req = urllib2.urlopen(url=url, timeout=10)
        except Exception as e3:
            print(e3)
        try:
            if req:
                print(url)
                content = req.read().decode('utf-8')
                # content=req.content.decode('utf-8')
                content_xpath = etree.HTML(content)
                try:
                    title = content_xpath.xpath('//head/title')[0].text.strip().replace('\\', '1')
                    urllist = content_xpath.xpath('//h1/a/@href')[0].strip().replace('\\', '1')
                    intro = content_xpath.xpath('//*[@id="basic_container"]/div[2]/ul/li[1]/span/text()')[
                        0].strip()  # 公司类型
                    manage = content_xpath.xpath('//*[@id="basic_container"]/div[2]/ul/li[3]/span/text()')[
                        0].strip()  # 公司人数
                    touzi_jigou = content_xpath.xpath('//*[@id="basic_container"]/div[2]/ul/li[2]/span/text()')[
                        0].strip()  # 投资
                    productend = content_xpath.xpath('//*[@id="basic_container"]/div[2]/ul/li[4]/span/text()')[
                        0].strip()  # 地理位置
                    producklist = content_xpath.xpath(
                        '//*[@id="company_products"]/div[2]/div[@class="product_content product_item clearfix"]/div/h4/div/a[1]')
                    product = ""
                    for i in producklist:
                        product = i.text.strip() + "-" + product
                    company_profile = repace2.findall(content)[0].strip().replace('\\', '1')
                    area = content_xpath.xpath('//p[@class="mlist_li_desc"]')
                    area1 = ""
                    for ii in area:
                        area1 = ii.text.strip() + "_" + area1
                    area2 = area1.replace('\\', '1')
                except Exception as e2:
                    print(e2)

                print(urllist, u"=", title, u"=", intro, u"=", productend, u"=", company_profile, u"=", manage, u"=",
                      touzi_jigou, u"=", area2)
                threadLock.acquire()
                try:
                    cur.execute(sql,
                                (str(url), str(urllist), str(title), str(intro), str(productend), str(company_profile), \
                                 str(manage), str(touzi_jigou), str(area2)))
                    conn.commit()
                except Exception as e1:
                    print("Mysql Error")
                    print(e1)
                    conn.rollback()
                threadLock.release()
                title = content_xpath.xpath('//head/title')[0].text
                print(title)
            else:
                pass
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # for i in range(1, 300000):
    for i in range(1, 5):
        url = "https://www.lagou.com/gongsi/" + str(i) + ".html"
        q_queue.put(url)
    t = threading.Thread(target=crawl, )
    t.start()
    t.join()
    time.sleep(1)
    print('ok')
