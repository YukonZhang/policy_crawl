import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("贵州省卫健委: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc("#Zoom").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#Zoom a").items()]
    try:
        data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        # data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="贵州省卫健委"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    urls=re.findall('var str_1 = "(.+?)";',html)
    for url in urls:
        url="" + url
        if "http" not in url:
            url="http://www.gzhfpc.gov.cn/xwzx_500663/tzgg" + url.replace("./","/")
        print(url)
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(0,67):
        print(i)
        if i==0:
            url="http://www.gzhfpc.gov.cn/xwzx_500663/tzgg/index.html"
        else:
            url="http://www.gzhfpc.gov.cn/xwzx_500663/tzgg/index_"+ str(i) +".html"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()