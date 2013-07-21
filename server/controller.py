# coding=utf8
import datetime
from extractfirst import extract_first, extract_web_num, extract_main_frame
from urlencoder import genurl, genurl_web 
import json

date_today = datetime.date.today()

RANGE_DAYS = 120
PAST_DAYS = 120 
FUTURE_DAYS = 120

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

def trans_date(date):
    return date.replace(':', ',').replace('-', ',').replace(' ',',').replace(',0',',')


def trans_to_timeline(data):
    tl = {'timeline': {'headline': data['query'], 'type': 'default', 'text': '', 'startDate': '', 'date': 
        [
        ]}}


    array = []
    data = data['data']
    for rec in data:
        item = {'startDate': '', 'headline': '', 'text': '', "asset": {'media': '', 'credit': '', 'caption': ''}}
        item['startDate'] = trans_date(rec['time'])
        item['headline'] = rec['news_title']
        item['text'] = rec['content'] + '\n' + rec['source_url']

        array.append(item)

    tl['timeline']['date'] = array

    json_content = json.dumps(tl, indent = 4)

    fout = open("result.json", "w")

    fout.write(json_content)

    return json_content




def load_json(fin):
    fin = open(fin, 'r')
    return json.loads(fin.read())


def main(query):
    #data =  find_peak(query)
    #print data
    data = [(datetime.date(2013, 3, 24), ('', '', '', None, 0)), (datetime.date(2013, 3, 25), ('', '', '', None, 0)), (datetime.date(2013, 3, 26), ('http://www.kejixun.com/article/201303/5498.html', '\xce\xa2\xc8\xed\xb1\xd8\xd3\xa6\xc8\xe7\xba\xce\xb8\xc4\xb1\xe4\xcb\xd1\xcb\xf7\xd5\xbd\xbe\xd6?\xbb\xf2\xd3\xa6\xd3\xebIE\xc9\xee\xb6\xc8\xd5\xfb\xba\xcf', '\xbf\xc6\xbc\xbc\xd1\xb6', '2013-03-26 09:29:22', 1)), (datetime.date(2013, 3, 27), ('', '', '', None, 0)), (datetime.date(2013, 3, 28), ('', '', '', None, 0)), (datetime.date(2013, 3, 29), ('', '', '', None, 0)), (datetime.date(2013, 3, 30), ('', '', '', None, 0)), (datetime.date(2013, 3, 31), ('', '', '', None, 0)), (datetime.date(2013, 4, 1), ('', '', '', None, 0)), (datetime.date(2013, 4, 2), ('', '', '', None, 0)), (datetime.date(2013, 4, 3), ('', '', '', None, 0)), (datetime.date(2013, 4, 4), ('', '', '', None, 0)), (datetime.date(2013, 4, 5), ('', '', '', None, 0)), (datetime.date(2013, 4, 6), ('', '', '', None, 0)), (datetime.date(2013, 4, 7), ('', '', '', None, 0)), (datetime.date(2013, 4, 8), ('http://tech.ifeng.com/it/detail_2013_04/08/23986135_0.shtml', '\xb4\xab\xce\xa2\xc8\xedWindows Blue\xbd\xab\xd5\xfb\xba\xcfWindows\xd7\xc0\xc3\xe6\xb0\xe6\xd3\xeb\xd2\xc6\xb6\xaf\xb0\xe6', '\xb7\xef\xbb\xcb\xcd\xf8\xbf\xc6\xbc\xbc', '2013-04-08 21:16:00', 2)), (datetime.date(2013, 4, 9), ('http://www.cnsoftnews.com/html/2013/ctsoft_0409/212.html', '\xce\xa2\xc8\xedWin8\xc9\xfd\xbc\xb6\xb0\xe6\xbd\xab\xd5\xfb\xba\xcfPC\xd3\xeb\xca\xd6\xbb\xfa\xc6\xbd\xcc\xa8 \xb6\xd4\xbf\xb9\xb9\xc8\xb8\xe8', '\xd6\xd0\xb9\xfa\xc8\xed\xbc\xfe\xd7\xca\xd1\xb6\xcd\xf8', '2013-04-09 07:20:00', 4)), (datetime.date(2013, 4, 10), ('http://www.cnsoftnews.com/html/2013/ctsoft_0410/253.html', 'Windows PC\xba\xcdWindows Phone\xd5\xfb\xba\xcf\xd4\xe7\xd3\xd0\xd4\xa4\xc4\xb1?', '\xd6\xd0\xb9\xfa\xc8\xed\xbc\xfe\xd7\xca\xd1\xb6\xcd\xf8', '2013-04-10 08:34:13', 1)), (datetime.date(2013, 4, 11), ('', '', '', None, 0)), (datetime.date(2013, 4, 12), ('', '', '', None, 0)), (datetime.date(2013, 4, 13), ('', '', '', None, 0)), (datetime.date(2013, 4, 14), ('', '', '', None, 0)), (datetime.date(2013, 4, 15), ('', '', '', None, 0)), (datetime.date(2013, 4, 16), ('', '', '', None, 0)), (datetime.date(2013, 4, 17), ('http://telecom.chinabyte.com/387/12594387.shtml', '\xce\xa2\xc8\xed\xca\xd6\xbb\xfa\xb2\xbf\xc3\xc5\xb8\xdf\xb9\xdc\xb3\xc6\xce\xa2\xc8\xed\xb2\xbb\xbb\xe1\xd7\xd4\xbc\xba\xd6\xc6\xd4\xec\xca\xd6\xbb\xfa', '\xb1\xc8\xcc\xd8\xcd\xf8', '2013-04-17 11:44:00', 1)), (datetime.date(2013, 4, 18), ('', '', '', None, 0)), (datetime.date(2013, 4, 19), ('', '', '', None, 0)), (datetime.date(2013, 4, 20), ('', '', '', None, 0)), (datetime.date(2013, 4, 21), ('', '', '', None, 0)), (datetime.date(2013, 4, 22), ('', '', '', None, 0)), (datetime.date(2013, 4, 23), ('', '', '', None, 0)), (datetime.date(2013, 4, 24), ('', '', '', None, 0)), (datetime.date(2013, 4, 25), ('', '', '', None, 0)), (datetime.date(2013, 4, 26), ('', '', '', None, 0)), (datetime.date(2013, 4, 27), ('', '', '', None, 0)), (datetime.date(2013, 4, 28), ('', '', '', None, 0)), (datetime.date(2013, 4, 29), ('', '', '', None, 0)), (datetime.date(2013, 4, 30), ('http://it.sohu.com/20130430/n374478066.shtml', '\xce\xa2\xc8\xed\xc3\xe2\xb7\xd1\xd3\xca\xcf\xe4Outlook.com\xd5\xfd\xca\xbd\xd5\xfb\xba\xcfSkype\xcd\xa8\xbb\xb0', '\xcb\xd1\xba\xfcIT', '2013-04-30 17:29:00', 1)), (datetime.date(2013, 5, 1), ('', '', '', None, 0)), (datetime.date(2013, 5, 2), ('', '', '', None, 0)), (datetime.date(2013, 5, 3), ('http://www.donews.com/it/201305/1487321.shtm', '\xd5\xfb\xba\xcfSkype \xce\xa2\xc8\xed3D\xd2\xf4\xca\xd3\xc6\xb5\xbb\xe1\xd2\xe9\xd0\xc2\xbc\xbc\xca\xf5\xc6\xd8\xb9\xe2!', 'donews', '2013-05-03 19:20:00', 1)), (datetime.date(2013, 5, 4), ('', '', '', None, 0)), (datetime.date(2013, 5, 5), ('', '', '', None, 0)), (datetime.date(2013, 5, 6), ('http://it.msn.com.cn/network/666034/138427017442b.shtml', '\xd5\xfb\xba\xcfSkype \xce\xa2\xc8\xed3D\xd2\xf4\xca\xd3\xc6\xb5\xbb\xe1\xd2\xe9\xd0\xc2\xbc\xbc\xca\xf5\xc6\xd8\xb9\xe2!', 'MSN\xd6\xd0\xb9\xfa', '2013-05-06 14:56:00', 1)), (datetime.date(2013, 5, 7), ('', '', '', None, 0)), (datetime.date(2013, 5, 8), ('', '', '', None, 0)), (datetime.date(2013, 5, 9), ('', '', '', None, 0)), (datetime.date(2013, 5, 10), ('', '', '', None, 0)), (datetime.date(2013, 5, 11), ('', '', '', None, 0)), (datetime.date(2013, 5, 12), ('', '', '', None, 0)), (datetime.date(2013, 5, 13), ('', '', '', None, 0)), (datetime.date(2013, 5, 14), ('http://info.audio.hc360.com/2013/05/141159407962.shtml', '\xce\xa2\xc8\xed\xd0\xc2\xbc\xbc\xca\xf5:\xd5\xfb\xba\xcfSkype\xcd\xc63D\xd2\xf4\xca\xd3\xc6\xb5\xbb\xe1\xd2\xe9', '\xbb\xdb\xb4\xcf\xcd\xf8', '2013-05-14 11:59:00', 1)), (datetime.date(2013, 5, 15), ('http://it.dbw.cn/system/2013/05/15/054767953.shtml', '\xce\xa2\xc8\xedOutlook.com\xd5\xfb\xba\xcfGoogle Talk', 'it\xc6\xb5\xb5\xc0', '2013-05-15 10:03:09', 1)), (datetime.date(2013, 5, 16), ('', '', '', None, 0)), (datetime.date(2013, 5, 17), ('', '', '', None, 0)), (datetime.date(2013, 5, 18), ('', '', '', None, 0)), (datetime.date(2013, 5, 19), ('', '', '', None, 0)), (datetime.date(2013, 5, 20), ('http://www.cbinews.com/server2/news/2013-05-20/204014.htm', '\xbb\xdd\xc6\xd5\xd1\xee\xce\xc4\xca\xa4\xb4\xc7\xd6\xb0\xbc\xd3\xc3\xcb\xce\xa2\xc8\xed \xbb\xf2\xd0\xed\xba\xcd\xbb\xdd\xc6\xd5\xba\xcf\xb2\xa2\xb2\xbf\xc3\xc5\xd3\xd0\xb9\xd8\xcf\xb5', '\xb5\xe7\xc4\xd4\xc9\xcc\xc7\xe9\xd4\xda\xcf\xdf', '2013-05-20 15:53:24', 1)), (datetime.date(2013, 5, 21), ('', '', '', None, 0)), (datetime.date(2013, 5, 22), ('http://game.people.com.cn/n/2013/0522/c48662-21569771.html', 'XboxOne\xb7\xa2\xb2\xbc\xbb\xe1:\xce\xa2\xc8\xed\xd5\xfb\xba\xcf\xbc\xd2\xd3\xc3\xc6\xbd\xcc\xa8\xb5\xc4\xd2\xb0\xcd\xfb', '\xc8\xcb\xc3\xf1\xcd\xf8\xd3\xce\xcf\xb7', '2013-05-22 09:16:00', 1)), (datetime.date(2013, 5, 23), ('', '', '', None, 0)), (datetime.date(2013, 5, 24), ('http://do.chinabyte.com/19/12623519.shtml', '\xce\xa2\xc8\xed\xd3\xe9\xc0\xd6\xb2\xbf\xc3\xc5\xd6\xf7\xb9\xdc:Xbox One\xcf\xf2\xcf\xc2\xbc\xe6\xc8\xdd\xbc\xb4\xb5\xb9\xcd\xcb', '\xb1\xc8\xcc\xd8\xcd\xf8\xd0\xd0\xd2\xb5', '2013-05-24 07:30:00', 1)), (datetime.date(2013, 5, 25), ('', '', '', None, 0)), (datetime.date(2013, 5, 26), ('', '', '', None, 0)), (datetime.date(2013, 5, 27), ('', '', '', None, 0)), (datetime.date(2013, 5, 28), ('', '', '', None, 0)), (datetime.date(2013, 5, 29), ('', '', '', None, 0)), (datetime.date(2013, 5, 30), ('', '', '', None, 0)), (datetime.date(2013, 5, 31), ('', '', '', None, 0)), (datetime.date(2013, 6, 1), ('', '', '', None, 0)), (datetime.date(2013, 6, 2), ('', '', '', None, 0)), (datetime.date(2013, 6, 3), ('', '', '', None, 0)), (datetime.date(2013, 6, 4), ('', '', '', None, 0)), (datetime.date(2013, 6, 5), ('http://tech.ifeng.com/digi/mobile/new/wp/detail_2013_06/05/26096463_0.shtml', '\xbe\xab\xbc\xf2\xbb\xfa\xb9\xb9\xd3\xeb\xc4\xda\xb2\xbf\xd5\xfb\xba\xcf:\xce\xa2\xc8\xed\xd7\xaa\xd0\xcd\xc2\xb7\xc9\xcf\xb2\xbb\xb5\xc3\xb2\xbb\xbe\xad\xc0\xfa\xb5\xc4\xd6\xd8\xd7\xe9', '\xb7\xef\xbb\xcb\xcd\xf8\xbf\xc6\xbc\xbc', '2013-06-05 08:06:00', 1)), (datetime.date(2013, 6, 6), ('', '', '', None, 0)), (datetime.date(2013, 6, 7), ('', '', '', None, 0)), (datetime.date(2013, 6, 8), ('http://tech.ifeng.com/it/detail_2013_06/08/26232368_0.shtml', '\xce\xa2\xc8\xed\xb1\xbb\xc6\xd8\xbd\xab\xbd\xf8\xd0\xd0\xbc\xdc\xb9\xb9\xd6\xd8\xd7\xe9 8\xb8\xf6\xd2\xb5\xce\xf1\xb2\xbf\xc3\xc5\xbe\xab\xbc\xf2\xce\xaa4\xb8\xf6', '\xb7\xef\xbb\xcb\xcd\xf8\xbf\xc6\xbc\xbc', '2013-06-08 06:33:00', 1)), (datetime.date(2013, 6, 9), ('http://server.chinabyte.com/319/12636319.shtml', '\xb4\xab\xce\xa2\xc8\xed\xd6\xd8\xd7\xe9 \xd2\xb5\xce\xf1\xb2\xbf\xc3\xc5\xd3\xc98\xb8\xf6\xbc\xf5\xd6\xc14\xb8\xf6', '\xb1\xc8\xcc\xd8\xcd\xf8', '2013-06-09 10:49:00', 1)), (datetime.date(2013, 6, 10), ('', '', '', None, 0)), (datetime.date(2013, 6, 11), ('http://tech.qq.com/a/20130611/006641.htm', '\xcb\xf7\xc4\xe1PS4\xca\xdb\xbc\xdb399\xc3\xc0\xd4\xaa \xd5\xfb\xba\xcf\xb5\xe7\xd3\xb0\xbf\xb9\xba\xe2\xce\xa2\xc8\xed', '\xcc\xda\xd1\xb6\xbf\xc6\xbc\xbc', '2013-06-11 15:32:00', 1)), (datetime.date(2013, 6, 12), ('http://www.sarft.net/web2011/a/109035.aspx', '\xcb\xf7\xc4\xe1PS4\xca\xdb\xbc\xdb399\xc3\xc0\xd4\xaa \xd5\xfb\xba\xcf\xb5\xe7\xd3\xb0\xbf\xb9\xba\xe2\xce\xa2\xc8\xed', '\xd6\xd0\xb9\xe3\xbb\xa5\xc1\xaa', '2013-06-12 05:17:00', 1)), (datetime.date(2013, 6, 13), ('', '', '', None, 0)), (datetime.date(2013, 6, 14), ('', '', '', None, 0)), (datetime.date(2013, 6, 15), ('', '', '', None, 0)), (datetime.date(2013, 6, 16), ('', '', '', None, 0)), (datetime.date(2013, 6, 17), ('', '', '', None, 0)), (datetime.date(2013, 6, 18), ('', '', '', None, 0)), (datetime.date(2013, 6, 19), ('', '', '', None, 0)), (datetime.date(2013, 6, 20), ('', '', '', None, 0)), (datetime.date(2013, 6, 21), ('', '', '', None, 0)), (datetime.date(2013, 6, 22), ('', '', '', None, 0)), (datetime.date(2013, 6, 23), ('', '', '', None, 0)), (datetime.date(2013, 6, 24), ('http://tech.ifeng.com/it/detail_2013_06/24/26722146_0.shtml', '\xb4\xab\xce\xa2\xc8\xed\xb4\xf3\xb9\xe6\xc4\xa3\xd6\xd8\xd7\xe9\xd3\xc9\xb1\xab\xb6\xfb\xc4\xac\xd6\xf7\xb5\xbc \xbd\xab\xb4\xb4\xd4\xec\xcb\xc4\xb8\xf6\xb6\xc0\xc1\xa2\xb2\xbf\xc3\xc5', '\xb7\xef\xbb\xcb\xcd\xf8\xbf\xc6\xbc\xbc', '2013-06-24 07:23:00', 3)), (datetime.date(2013, 6, 25), ('http://news.zol.com.cn/tech/74894.html', '\xc8\xe7\xb9\xfbWindows \xba\xcd Windows Phone \xb2\xbf\xc3\xc5\xba\xcf\xb2\xa2', '\xd6\xd0\xb9\xd8\xb4\xe5\xd4\xda\xcf\xdf', '2013-06-25 10:59:00', 3)), (datetime.date(2013, 6, 26), ('http://news.zol.com.cn/tech/75849.html', '\xce\xa2\xc8\xed\xb3\xc9\xc1\xa2\xb7\xe7\xcf\xd5\xcd\xb6\xd7\xca\xb2\xbf\xc3\xc5 \xd5\xfb\xba\xcf\xb6\xe0\xb8\xf6\xcf\xee\xc4\xbf', '\xd6\xd0\xb9\xd8\xb4\xe5\xd4\xda\xcf\xdf', '2013-06-26 10:14:00', 12)), (datetime.date(2013, 6, 27), ('http://finance.takungpao.com/tech/q/2013/0627/1718742.html', '\xce\xa2\xc8\xed\xb7\xe7\xcf\xd5\xcd\xb6\xd7\xca\xb2\xbf\xc3\xc5Microsoft Ventures\xc0\xb4\xc1\xcb', '\xb4\xf3\xb9\xab\xcd\xf8', '2013-06-27 11:25:35', 1)), (datetime.date(2013, 6, 28), ('http://www.eet-china.com/ART_8800686757_617693_NT_80167e31.HTM', '\xce\xa2\xc8\xed\xbb\xf2\xb4\xf3\xb9\xe6\xc4\xa3\xd6\xd8\xd7\xe9 Windows\xba\xcdWP\xb2\xbf\xc3\xc5\xd5\xfb\xba\xcf\xb8\xdf\xb9\xdc\xb1\xe4\xb6\xaf', '\xb5\xe7\xd7\xd3\xb9\xa4\xb3\xcc\xd7\xa8\xbc\xad', '2013-06-28 00:06:45', 3)), (datetime.date(2013, 6, 29), ('', '', '', None, 0)), (datetime.date(2013, 6, 30), ('', '', '', None, 0)), (datetime.date(2013, 7, 1), ('', '', '', None, 0)), (datetime.date(2013, 7, 2), ('http://news.zol.com.cn/tech/80176.html', '\xce\xa2\xc8\xed\xbb\xa5\xb6\xaf\xd3\xe9\xc0\xd6\xb2\xbf\xc3\xc5\xd7\xdc\xb2\xc3Don Mattrick\xbd\xab\xc0\xeb\xd6\xb0', '\xd6\xd0\xb9\xd8\xb4\xe5\xd4\xda\xcf\xdf', '2013-07-02 01:36:00', 2)), (datetime.date(2013, 7, 3), ('http://finance.people.com.cn/n/2013/0703/c66323-22065483.html', '\xce\xa2\xc8\xed\xd6\xd8\xd7\xe9\xbc\xc6\xbb\xae\xc6\xd8\xb9\xe2:WP\xba\xcdWindows\xb2\xbf\xc3\xc5\xbd\xab\xba\xcf\xb2\xa2', '\xc8\xcb\xc3\xf1\xcd\xf8\xb2\xc6\xbe\xad\xbe\xad\xbc\xc3\xc6\xb5\xb5\xc0', '2013-07-03 14:51:00', 2)), (datetime.date(2013, 7, 4), ('http://tech.ifeng.com/digi/detail_2013_07/04/27119864_0.shtml', '\xce\xa2\xc8\xed\xd6\xd8\xd7\xe9\xbc\xc6\xbb\xae\xc1\xf7\xb3\xf6:\xbc\xd3\xc7\xbf\xb2\xbf\xc3\xc5\xc4\xda\xba\xcf\xd7\xf7\xb6\xc0\xc1\xa2\xd3\xaa\xcf\xfa\xba\xcd\xb2\xc6\xd5\xfe', '\xb7\xef\xbb\xcb\xcd\xf8\xbf\xc6\xbc\xbc', '2013-07-04 08:42:00', 2)), (datetime.date(2013, 7, 5), ('', '', '', None, 0)), (datetime.date(2013, 7, 6), ('http://bizsoft.yesky.com/41/35157541.shtml', '\xce\xa2\xc8\xed\xd6\xd8\xd7\xe9\xbc\xc6\xbb\xae:\xb2\xd9\xd7\xf7\xcf\xb5\xcd\xb3\xd3\xeb\xd3\xb2\xbc\xfe\xb2\xbf\xc3\xc5\xd7\xee\xca\xdc\xb9\xd8\xd7\xa2', '\xcc\xec\xbc\xab\xcd\xf8', '2013-07-06 06:00:00', 1)), (datetime.date(2013, 7, 7), ('http://www.pconline.com.cn/news/gjyj/0608/840094.html', 'Vista\xb3\xd9\xb3\xd9\xb2\xbb\xb3\xf6\xd2\xfd\xce\xa2\xc8\xed\xb7\xa2\xc5\xad Windows\xb2\xbf\xc3\xc5\xd4\xe2\xb5\xbd\xd6\xd8\xd7\xe9', '\xcc\xab\xc6\xbd\xd1\xf3\xb5\xe7\xc4\xd4\xcd\xf8', '2013-07-07 01:05:21', 1)), (datetime.date(2013, 7, 8), ('http://tech.ifeng.com/it/detail_2013_07/08/27266549_0.shtml', '\xce\xa2\xc8\xed\xd4\xda\xbb\xaa\xd2\xfd\xc8\xeb\xb4\xb4\xcd\xb6\xb2\xbf\xc3\xc5 \xce\xaa\xb4\xb4\xd2\xb5\xd5\xdf\xcc\xe1\xb9\xa9\xbc\xbc\xca\xf5\xd7\xca\xbd\xf0\xd6\xa7\xb3\xd6', '\xb7\xef\xbb\xcb\xcd\xf8\xbf\xc6\xbc\xbc', '2013-07-08 15:43:00', 2)), (datetime.date(2013, 7, 9), ('http://www.ithome.com/html/it/48539.htm', '\xa1\xb0\xc9\xe8\xb1\xb8\xd3\xeb\xb7\xfe\xce\xf1\xa1\xb1,\xce\xa2\xc8\xed\xd6\xd8\xd7\xe9\xb7\xbd\xb0\xb8\xd4\xa4\xbc\xc6\xd4\xda\xd6\xdc\xcb\xc4\xb9\xab\xbf\xaa', 'IT\xd6\xae\xbc\xd2', '2013-07-09 18:42:57', 1)), (datetime.date(2013, 7, 10), ('', '', '', None, 0)), (datetime.date(2013, 7, 11), ('http://tech.qq.com/a/20130711/017863.htm', '\xce\xa2\xc8\xed\xa1\xb0\xca\xdd\xc9\xed\xa1\xb1:\xcf\xeb\xd2\xaa\xb8\xfc\xc1\xe9\xbb\xee \xb7\xb4\xd3\xa6\xb8\xfc\xbf\xec', '\xcc\xda\xd1\xb6\xbf\xc6\xbc\xbc', '2013-07-11 23:47:00', 2)), (datetime.date(2013, 7, 12), ('http://finance.cnr.cn/jjpl/201307/t20130712_513046453.shtml', '\xce\xa2\xc8\xed\xba\xcf\xb2\xa2\xb6\xe0\xb2\xbf\xc3\xc5 \xc6\xc0:\xca\xdd\xc9\xed\xc8\xc3\xce\xa2\xc8\xed\xb5\xc4\xb2\xfa\xc6\xb7\xcf\xdf\xb8\xfc\xc7\xe5\xce\xfa', '\xd6\xd0\xb9\xfa\xb9\xe3\xb2\xa5\xcd\xf8', '2013-07-12 18:26:00', 188)), (datetime.date(2013, 7, 13), ('http://finance.china.com.cn/roll/20130713/1634880.shtml', '\xce\xa2\xc8\xed\xd0\xfb\xb2\xbc\xd6\xd8\xd7\xe9\xbc\xc6\xbb\xae \xb8\xc4\xbd\xa8\xb3\xc9\xcb\xc4\xb4\xf3\xd2\xb5\xce\xf1\xb2\xbf\xc3\xc5', '\xd6\xd0\xb9\xfa\xcd\xf8', '2013-07-13 07:28:00', 6)), (datetime.date(2013, 7, 14), ('http://finance.cnr.cn/gs/201307/t20130714_513054456.shtml', '\xd5\xc5\xd7\xd3\xd3\xea:\xce\xa2\xc8\xed\xb5\xc4\xbc\xd3\xbc\xf5\xb7\xa8', '\xd6\xd0\xb9\xfa\xb9\xe3\xb2\xa5\xcd\xf8', '2013-07-14 18:43:00', 8)), (datetime.date(2013, 7, 15), ('http://news.xinhuanet.com/info/2013-07/15/c_132541042.htm', '\xce\xa2\xc8\xed\xd0\xfb\xb2\xbc\xd6\xd8\xd7\xe9\xbc\xc6\xbb\xae \xb2\xfa\xc6\xb7\xb2\xbf\xc3\xc5\xbd\xab\xb7\xd6\xce\xaa\xcb\xc4\xb8\xf6\xd0\xc2\xb2\xbf\xc3\xc5 ', '\xd0\xc2\xbb\xaa\xcd\xf8', '2013-07-15 09:06:36', 10)), (datetime.date(2013, 7, 16), ('http://news.qudong.com/2013/0716/148762.shtml', '\xce\xa2\xc8\xed\xbd\xabSurface\xba\xcdXbox\xb2\xbf\xc3\xc5\xba\xcf\xb2\xa2 Win8\xd6\xc7\xc4\xdc\xca\xd6\xb1\xed\xc6\xd8\xb9\xe2', '\xc7\xfd\xb6\xaf\xd6\xd0\xb9\xfa', '2013-07-16 08:55:00', 7)), (datetime.date(2013, 7, 17), ('http://tech.sina.com.cn/it/2013-07-17/07198546948.shtml', '\xce\xa2\xc8\xed\xbc\xdc\xb9\xb9\xb5\xf7\xd5\xfb\xb3\xbe\xb0\xa3\xc2\xe4\xb6\xa8', '\xd0\xc2\xc0\xcb\xbf\xc6\xbc\xbc', '2013-07-17 07:19:00', 2)), (datetime.date(2013, 7, 18), ('http://www.eet-china.com/ART_8800686757_617693_NT_80167e31.HTM?click_from_postlink', '\xce\xa2\xc8\xed\xbb\xf2\xb4\xf3\xb9\xe6\xc4\xa3\xd6\xd8\xd7\xe9 Windows\xba\xcdWP\xb2\xbf\xc3\xc5\xd5\xfb\xba\xcf\xb8\xdf\xb9\xdc\xb1\xe4\xb6\xaf', '\xb5\xe7\xd7\xd3\xb9\xa4\xb3\xcc\xd7\xa8\xbc\xad', '2013-07-18 03:25:55', 4)), (datetime.date(2013, 7, 19), ('', '', '', None, 0)), (datetime.date(2013, 7, 20), ('', '', '', None, 0)), (datetime.date(2013, 7, 21), ('', '', '', None, 0))]
    put_data(query, data)
    #data = load_json('demo.json')
    #print trans_to_timeline(data)



if __name__ == '__main__':
    query = u'微软整合部门'
    main(query)



