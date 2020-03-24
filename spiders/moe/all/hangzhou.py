import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("杭州教育局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc("#zoom").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#zoom a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="杭州教育局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc = pq(html)
    items = doc(".tr_main_value_odd a,tr_main_value_even a").items()
    for item in items:
        url = item.attr("href")
        try:
            html = get(url)
        except:
            errorlog.logger.error("url错误:%s" % url)
        parse_detail(html, url)
        time.sleep(1)

def main():
    url="http://www.hangzhou.gov.cn/module/xxgk/search.jsp?"
    for i in range(1,91):
        params={'texttype': '0', 'fbtime': '-1', 'vc_all': '', 'vc_filenumber': '', 'vc_title': '', 'vc_number': '', 'currpage': str(i), 'sortfield': ',compaltedate:0'}
        data={'infotypeId': 'F010000201', 'jdid': '149', 'area': '', 'divid': 'div1256347', 'vc_title': '', 'vc_number': '', 'sortfield': ',compaltedate:0', 'currpage': str(i), 'vc_filenumber': '', 'vc_all': '', 'texttype': '0', 'fbtime': '-1'}
        html=post(url,params=params,data=data)
        parse_index(html)




if __name__ == '__main__':
    main()