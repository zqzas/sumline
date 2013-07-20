# coding=utf8
import datetime
from extractfirst import extract_first, extract_web_num, extract_main_frame
from urlencoder import genurl, genurl_web 
import json

date_today = datetime.date.today()

RANGE_DAYS = 60
PAST_DAYS = 15
FUTURE_DAYS = 45

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
    day = peak - datetime.timedelta(days = PAST_DAYS + 1) 
    for x in xrange(PAST_DAYS + FUTURE_DAYS):
        day += delta
        if day not in dic:
            continue
        res.append( (day, dic[day]) )
    return res


def put_data(query, data):
    '''
    Put data into JSON
    @param data : the response from find_peak(query)

    @json       : (query, [(source_url, news_title, source_title, time, news_amount, main_content, web_amount)])
    '''

    json_content = []

    for item in data:
        item = list(item[1])
        for index in xrange(len(item)):
            if type(item[index]) == type(123):
                continue
            item[index] = item[index].decode('gbk')
            

        print '*' * 30, item[0]
        source_main_content = extract_main_frame(item[0])
        source_web_amount = extract_web_num(genurl_web(item[1]))

        item.append(source_main_content)
        item.append(source_web_amount)

        json_content.append(item)

    json_content = json.dumps((query, json_content))

    fout = open(query + '.json', 'w')
    fout.write(json_content)






if __name__ == '__main__':
    query = u'韩亚航空'
    data =  find_peak(query)
    print data
    put_data(query, data)




