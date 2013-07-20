# coding=utf8
import datetime
from extractfirst import extract_first, extract_web_num
from urlencoder import genurl, genurl_web 
import json

date_today = datetime.date.today()

RANGE_DAYS = 30
PAST_DAYS = 3
FUTURE_DAYS = 9

def find_peak(query):
    '''
    @param query
    @return     : an array storing the info in 120 days
    '''
    delta = datetime.timedelta(days=1)
    day = date_today
    dic = {}
    max_amount = 0
    for x in xrange(RANGE_DAYS):
        news_url = genurl(query, day)
        (source_url, news_title, source_title, time, amount) = extract_first(news_url)
        dic[day] = (source_url, news_title, source_title, time, amount) 
        print dic[day]
        if amount > max_amount:
            max_amount = amount
            peak = day
        day -= delta

    res = []
    day = peak - datetime.timedelta(days = PAST_DAYS)
    for x in xrange(PAST_DAYS + FUTURE_DAYS):
        if day not in dic:
            break
        res.append( (day, dic[day]) )
        day += delta
    return res


def put_data(data):
    '''
    Put data into JSON
    @param data : the response from find_peak(query)

   ''' 


if __name__ == '__main__':
    print find_peak(u'韩亚航空')


