# Author: arapat
# Convert search queries on a specific date to url
# URL sample:
# http://news.baidu.com/ns?from=news&cl=2&bt={bt}&y0={y0}&m0={m0}&d0={d0}&y1={y1}&m1={m1}&d1={d1}&et={et}&q1={query}&submit=%B0%D9%B6%C8%D2%BB%CF%C2&q3=&q4=&mt=0&lm=&s=2&begin_date={begin_date}&end_date={end_date}&tn=newsdy&ct1=1&ct=1&rn=20&q6=

import urllib2
import datetime as DT


def formatdate(date):
    return date.strftime('%Y-%m-%d')


def genurl(query, date):
    assert(query)
    assert(isinstance(date, DT.date))

    str_date = formatdate(date)
    str_date_e = str_date.split('-')
    differ_to_src = date - DT.date(2013,7,20)

    bt = 1374249600 + int(differ_to_src.total_seconds())
    y0, m0, d0 = str_date_e
    y1, m1, d1 = str_date_e
    et = bt + 86399
    q1 = urllib2.quote(query.encode('gbk'))
    begin_date = str_date
    end_date = str_date
    # q6 = # TODO

    return "http://news.baidu.com/ns?from=news&cl=2&bt=" + str(bt) + "&y0=" + y0 + "&m0=" + m0 + "&d0=" + d0 + "&y1=" + y1 + "&m1=" + m1 + "&d1=" + d1 + "&et=" + str(et) + "&q1=" + q1 + "&submit=%B0%D9%B6%C8%D2%BB%CF%C2&q3=&q4=&mt=0&lm=&s=2&begin_date=" + begin_date + "&end_date=" + end_date + "&tn=newsdy&ct1=1&ct=1&rn=20&q6="

