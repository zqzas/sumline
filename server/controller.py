# coding=utf8
import datetime
from extractfirst import extract_first, extract_web_num, extract_main_frame
from urlencoder import genurl, genurl_web 
import json

date_today = datetime.date.today()

RANGE_DAYS = 180
PAST_DAYS = 30
FUTURE_DAYS = 50

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

    json_content = {'query' : query, 'data' : []}

    for item in data:
        item = list(item[1])
        if item[4] == 0:
            continue
        for index in xrange(len(item)):
            if type(item[index]) == type(123) or item[index] == None:
                continue
            item[index] = item[index].decode('gbk')

                    

        print '*' * 30, item[0]
        if item[0]:
            source_main_content = extract_main_frame(item[0])
        else:
            source_main_content = ''
        source_web_amount = extract_web_num(genurl_web(item[1]))

        item.append(source_main_content)
        item.append(source_web_amount)

        dic = {}
        dic['source_url'] = item[0]
        dic['news_title'] = item[1]
        dic['source_title'] = item[2]
        dic['time'] = item[3]
        dic['news_amount'] = item[4]
        dic['content'] = item[5]
        dic['web_amount'] = item[6]


        json_content['data'].append(dic)

    json_content = json.dumps(json_content)

    fout = open(query + '.json', 'w')
    fout.write(json_content)

'''
def trans_date(date):
    datetime

def trans_to_timeline(data):
    tl = {'timeline': {'headline': '', 'type': 'default', 'text': '', 'startDate': '', 'date': 
        [
        ]}}


    tl['timeline']['headline'] = data['query']

    array = []
    for rec in data:
        item = {'startDate': '', 'headline': '', 'text': '', "asset": {'media': '', 'credit': '', 'caption': ''}}
        item[

'''






if __name__ == '__main__':
    query = u'韩亚航空'
    data =  find_peak(query)
    print data
    put_data(query, data)




