import urllib, urllib2
import re

sig = '<table cellspacing=0 cellpadding=2>'

url_sig = '<a href="'


def strip_html_tags(html):
    return re.sub('<[^<]+?>', '', html)

def extract_first(url):
    '''
    @return: (source_url, news_title, source_title, time)

    '''
    html = urllib2.urlopen(url).read()

    f = open('test.txt', 'w')
    f.write(html)


    print html.find(sig)

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

    print (source_url, news_title, source_title, time)


extract_first("http://news.baidu.com/ns?from=news&cl=2&bt=1374163200&y0=2013&m0=07&d0=19&y1=2013&m1=07&d1=19&et=1374249599&q1=%BA%AB%D1%C7%BA%BD%BF%D5&submit=%B0%D9%B6%C8%D2%BB%CF%C2&q3=&q4=&mt=0&lm=&s=2&begin_date=2013-07-19&end_date=2013-07-19&tn=newsdy&ct1=1&ct=1&rn=20&q6=")









