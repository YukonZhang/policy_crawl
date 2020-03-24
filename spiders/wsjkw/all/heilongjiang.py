import re
import time
import random 

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("黑龙江省卫健委: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".details_title h1").text()
    data["content"]=doc(".danye").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".danye a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="黑龙江省卫健委"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".wenzhanglist li a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://wsjkw.hlj.gov.cn" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(1,75):
        print(i)
        url="http://wsjkw.hlj.gov.cn/index.php/Home/News/all.shtml?typeid=33&p=" + str(i)
        html=get(url)
        parse_index(html)



if __name__ == '__main__':
    main()