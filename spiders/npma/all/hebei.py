import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("河北省药品监督管理局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".articlecontent1").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".articlecontent1 a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="河北省药品监督管理局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".ListColumnClass5 a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://yjj.hebei.gov.cn" + url.replace("../","/")
        try:
            html=get(url,code="gbk")
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(32,35):
        print(i)
        if i==0:
            url="http://yjj.hebei.gov.cn/CL0214/index.html"
        else:
            url="http://yjj.hebei.gov.cn/CL0214/index_"+ str(i) +".html"
        try:
            html=get(url,code="gb2312")
        except:
            html = get(url,code="GB18030")
        parse_index(html)
    for i in range(0, 2):
        print(i)
        if i == 0:
            url = "http://yjj.hebei.gov.cn/CL0215/index.html"
        else:
            url = "http://yjj.hebei.gov.cn/CL0215/index_"+ str(i) +".html"
        html = get(url,code="gb2312")
        parse_index(html)
    for i in range(0,1):
        print(i)
        if i==0:
            url="http://yjj.hebei.gov.cn/CL0434/"
        html = get(url, code="gb2312")
        parse_index(html)




if __name__ == '__main__':
    main()