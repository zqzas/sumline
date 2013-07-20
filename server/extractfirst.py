import urllib, urllib2
import re
from readability.readability import Document

sig = '<table cellspacing=0 cellpadding=2>'

url_sig = '<a href="'

amount_sig = '<td align="right" nowrap>'

amount_web_sig = '<span class="nums" style="margin-left:120px">'


def strip_html_tags(html):
    html = re.sub('<[^<]+?>', '', html)
    return re.sub('&#[0-9]+;', '', html)


def extract_first(url):
    '''
    @return: (source_url, news_title, source_title, time, amount)

    '''
    print '-----', url, '\n------'

    html = urllib2.urlopen(url).read()
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
    html = urllib2.urlopen(url).read()

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

    html = urllib2.urlopen(url).read()
    main_content = strip_html_tags(Document(html).summary())
    return main_content
    





if __name__ == '__main__':
    print extract_first("http://news.baidu.com/ns?from=news&cl=2&bt=1374163200&y0=2013&m0=07&d0=19&y1=2013&m1=07&d1=19&et=1374249599&q1=%BA%AB%D1%C7%BA%BD%BF%D5&submit=%B0%D9%B6%C8%D2%BB%CF%C2&q3=&q4=&mt=0&lm=&s=2&begin_date=2013-07-19&end_date=2013-07-19&tn=newsdy&ct1=1&ct=1&rn=20&q6=")

    print extract_main_frame('http://news.enorth.com.cn/system/2013/07/19/011159841.shtml')
    print extract_web_num('http://www.baidu.com/s?wd=%BA%AB%D1%C7%BA%BD%BF%D5')
    print extract_web_num('http://www.baidu.com/s?wd=fasdfasdfasdfasdfasfdasdf14123edfasdf')

    








