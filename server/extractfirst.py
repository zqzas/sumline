import urllib, urllib2
import re
from readability.readability import Document

sig = '<table cellspacing=0 cellpadding=2>'

url_sig = '<a href="'

amount_sig = '<td align="right" nowrap>'

amount_web_sig = '<span class="nums" style="margin-left:120px">'


def read_baidu(url):
    req=urllib2.Request(url)
    req.add_header('Cookie','BDREFER=%7Burl%3A%22http%3A//news.baidu.com/ns%3Ffrom%3Dnews%26cl%3D2%26bt%3D1374336000%26y0%3D2013%26m0%3D07%26d0%3D21%26y1%3D2013%26m1%3D07%26d1%3D21%26et%3D1374422399%26q1%3D91%25CE%25DE%25CF%25DF%26submit%3D%25B0%25D9%25B6%25C8%25D2%25BB%25CF%25C2%26q3%3D%26q4%3D%26mt%3D0%26lm%3D%26s%3D2%26begin_date%3D2013-07-21%26end_date%3D2013-07-21%26tn%3Dnewsdy%26ct1%3D1%26ct%3D1%26rn%3D20%26q6%3D%22%2Cword%3A%22%22%7D; Hm_lpvt_e9e114d958ea263de46e080563e254c4=1374351840; Hm_lvt_e9e114d958ea263de46e080563e254c4=1372669492,1374351840; BDNVCODE=51EAF1DEC569A3951854112; bdshare_firstime=1374340141166; H_PS_PSSID=2900_2776_1457_2703_2784_2581_1788_2250_2543_2702; BDREFER=%7Burl%3A%22http%3A//news.baidu.com/gongsi/hanyahangkong%23searchTrendContainer%22%2Cword%3A%22%22%7D; BDUSS=d2R3F3cGNaMTNzZHBLSk15Q0IxZ05TYWN-YUhaT2N3STVvV0M4N2c3NUswaEJTQVFBQUFBJCQAAAAAAAAAAAEAAADV5uk1enF6YXNfZmQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEpF6VFKRelRaj; SSUDB=m5XSkh3NXc1cllGM0N2fmdEb05-fnBqaVN4YTkwQnZhSE16S2FKVlk4amJ6QkJTQVFBQUFBJCQAAAAAAAAAAAEAAADV5uk1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANs~6VHbP-lRS; SSUDBTSP=1374240732; BDUT=ig2e22FCAE2BE4C70816D1659311E713FCDA1373776aaca1; BAIDU_WISE_UID=32CFF226F93DC5696FEBD58DDCAE59EE; BAIDU_WAP_WENKU=da09c2fc0242a8956bece42f_1_1_1000_2_1_1_color_wk; BAIDUID=222337504D06C18B9992FA4C89F4B73C:FG=1')
    req.add_header('User-Agent','Mozilla/5.0 (iPod; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3')	
    #req.add_header('Accept-Encoding','gzip, deflate')
    #req.add_header('Content-Type','application/x-www-form-urlencoded')
    #req.add_header('Connection','keep-alive')

    return urllib2.urlopen(req).read()




def strip_html_tags(html):
    html = re.sub('<[^<]+?>', '', html)
    return re.sub('&#[0-9]+;', '', html)


def extract_first(url):
    '''
    @return: (source_url, news_title, source_title, time, amount)

    '''
    print '-----', url, '\n------'

    html = read_baidu(url)
    amount = html[html.find(amount_sig) + len(amount_sig) : ]
    if amount[0] == '<': #check if no result
        return ('', '', '', None, 0)


    cnt = 0
    while amount[cnt].isdigit() == False:
        cnt += 1

    amount = amount[cnt : ]
    cnt = 0
    while amount[cnt].isdigit() or amount[cnt] == ',':
        cnt += 1

    amount = int(amount[ : cnt].replace(',', ''))

    try:
        html = html[html.find(sig) : ]
    except:
        raise Exception("Fail to find first title!")


    html = html[html.find(url_sig) + len(url_sig) : ]

    source_url = html[ : html.find('"')].strip()

    news_title = html[html.find("<span><b>") + len("<span><b>") : html.find("</b></span>")]

    source_title = html[html.find("<nobr>") + len("<nobr>") : html.find("</nobr>")]

    time = source_title[source_title.find(' ') + 1 : ]

    source_title = source_title[ : source_title.find(' ')]

    news_title = strip_html_tags(news_title)

    source_title = strip_html_tags(source_title)

    return (source_url, news_title, source_title, time, amount)



def extract_web_num(url):
    '''
    @param url  : the url of web search result page to be parsed
    @return     : the amount of the searching results, an integer

    '''
    html = read_baidu(url)

    if html.find(amount_web_sig) == -1 :
        return 0

    amount = html[html.find(amount_web_sig) + len(amount_web_sig) : ]
    cnt = 0
    while amount[cnt].isdigit() == False:
        cnt += 1
    amount = amount[cnt : ]
    cnt = 0
    while amount[cnt].isdigit() or amount[cnt] == ',':
        cnt += 1
    amount = int(amount[ : cnt].replace(',', ''))

    return amount




def extract_main_frame(url):
    '''
    @param url  : the url of news site to be parsed
    @return     : the content of the main frame

    '''

    #html = read_baidu(url)
    html = urllib2.urlopen(url).read()
    if html == None or html == '':
        return ''
    try:
        main_content = strip_html_tags(Document(html).summary())
    except:
        return ''
    return main_content
    





if __name__ == '__main__':
    print extract_first("http://news.baidu.com/ns?from=news&cl=2&bt=1374163200&y0=2013&m0=07&d0=19&y1=2013&m1=07&d1=19&et=1374249599&q1=%BA%AB%D1%C7%BA%BD%BF%D5&submit=%B0%D9%B6%C8%D2%BB%CF%C2&q3=&q4=&mt=0&lm=&s=2&begin_date=2013-07-19&end_date=2013-07-19&tn=newsdy&ct1=1&ct=1&rn=20&q6=")

    print extract_main_frame('http://news.enorth.com.cn/system/2013/07/19/011159841.shtml')
    print extract_web_num('http://www.baidu.com/s?wd=%BA%AB%D1%C7%BA%BD%BF%D5')
    print extract_web_num('http://www.baidu.com/s?wd=fasdfasdfasdfasdfasfdasdf14123edfasdf')

    








