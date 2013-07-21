# coding=utf8
import json
import jieba.posseg as pseg
import math
from getabstract import *
from operator import itemgetter
from numpy import *
from deltaLDA import deltaLDA
import jieba
import jieba.analyse
from optparse import OptionParser

ignore_words = ['e', 'o', 'p', 'w', 'x', 'y', 'm', 'u', 'r', 'c', 'k', 'f']
word_dim = 2000
topic_cnt = 10
numsamp = 5000
randseed = 194582

weights = [0.2, 0.6, 0.2]
threshold = 0.4
minimalnum = 15

def loadLocalTest():
    result = {'data':[]}
    c1 = ''
    with open('d1.txt', 'rb') as f1:
        for row in f1:
            row = row.strip()
            c1 = c1 + row
    c1 = c1.decode('gb18030').encode('utf8')
    j1 = {'news_title': u'韩亚航空承诺“无差别”赔偿事故遇难者', 'content': c1, 'web_amount':1}
    result['data'].append(j1)
    
    c2 = ''
    with open('d2.txt', 'rb') as f2:
        for row in f2:
            row = row.strip()
            c2 = c2 + row
    c2 = c2.decode('gb18030').encode('utf8')
    j2 = {'news_title': u'韩亚航空代表到浙江江山中学向家长致歉', 'content': c2, 'web_amount':2}
    result['data'].append(j2)
    return result

def isWordFlagIgnored(flag):
    for ch in ignore_words:
        if flag.startswith(ch):
            return True
    return False

def getSplitData(samples):
    split_data = []
    for i in xrange(len(samples)):
        article = {}
        t = list(pseg.cut(samples[i]['news_title'].replace('_', ' ')))
        article['words_title'] = [u.word for u in t if not isWordFlagIgnored(u.flag)]
        t = list(pseg.cut(samples[i]['content']))
        article['words_content'] = [u for u in t if not isWordFlagIgnored(u.flag)]
        split_data.append(article)
    return split_data

def getWordTable(split_data):
    word_tfidf = {}
    words_of_articles = []
    for i in xrange(len(split_data)):
        word_cnt = {}
        total_cnt = len(split_data[i]['words_content'])
        for w in split_data[i]['words_content']:
            if word_cnt.has_key(w):
                word_cnt[w] += 1
            else: 
                word_cnt[w] = 1
        for word, cnt in word_cnt.items():
            word_cnt[word] = (cnt + 0.0) / (total_cnt + 0.0)
        words_of_articles.append(word_cnt)
    
    art_cnt = len(words_of_articles)
    for i in xrange(art_cnt):
        for word, tf in words_of_articles[i].items():
            cnt = 0
            for j in xrange(art_cnt):
                if words_of_articles[j].has_key(word):
                    cnt = cnt + 1
            idf = math.log(art_cnt / cnt)
            if word_tfidf.has_key(word):
                word_tfidf[word] = max(word_tfidf[word], tf * idf)
            else:
                word_tfidf[word] = tf * idf

    word_list = []
    for key, value in word_tfidf.iteritems():
        temp = [key,value]
        word_list.append(temp)
    word_list = sorted(word_list,reverse=True,key=itemgetter(1))
    result = {}
    for i in xrange(word_dim):
        if i == len(word_list):
            break
        result[word_list[i][0]] = i;
    return result

def getFeatArr(split_data, word_table):
    result = []
    for i in xrange(len(split_data)):
        l = len(split_data[i]['words_content'])
        words = []
        for j in xrange(l):
            word = split_data[i]['words_content'][j]
            if word_table.has_key(word):
                words.append(word_table[word])
        result.append(words)
    return result

def getDocTopicMat(docs):
    alpha = .1 * ones((1, topic_cnt))
    beta = ones((topic_cnt, word_dim))
    (phi,theta,sample) = deltaLDA(docs,alpha,beta,numsamp,randseed)
    return theta

def getTitleSim(split_data):
    result = []
    for i in xrange(len(split_data)):
        if i == 0:
            result.append(0)
        else:
            s_old = split_data[i - 1]['words_title']
            s_new = split_data[i]['words_title']
            union_set = {}
            cross_set = {}
            for w in s_old:
                union_set[w] = 1
                if w in s_new:
                    cross_set[w] = 1
            for w in s_new:
                union_set[w] = 1
            result.append((len(cross_set) + 0.0) / (len(union_set) + 0.0))
    return result

def getFeatureMatrix(samples):
    split_data = getSplitData(samples['data'])
    word_table = getWordTable(split_data)
    docs = getFeatArr(split_data, word_table)
    mat = getDocTopicMat(docs)
    sim = getTitleSim(split_data)
    feat = []
    for i in xrange(len(split_data)):
        f = mat[i].tolist()
        f.append(sim[i])
        f.append(samples['data'][i]['web_amount'])
        feat.append(f)
    return feat

def getdiff(v_old, v_new):
    sum = 0
    v = [0]
    for i in xrange(len(v_old)):
        if i < len(v_old) - 2:
            v[0] += abs(v_old[i] - v_new[i])
        elif i == len(v_old) - 2:
            v.append(1 - v_new[i])
        else: 
            v.append((v_new[i] - v_old[i]) / (v_old[i] + 0.00001))
    v[0] /= len(v_old) - 2
    for i in xrange(3):
        sum += v[i] * weights[i]
    return sum

def getDisplayedIdx(feat):
    buf = []
    for i in xrange(len(feat)):
        if i == 0:
            buf.append([0,100])
            continue
        buf.append([i, getdiff(feat[i - 1], feat[i])])
    buf = sorted(buf,reverse=True,key=itemgetter(1))
    result = []
    for i in xrange(len(buf)):
        if i < minimalnum or buf[i][1] > threshold:
            result.append(buf[i][0])
    result = sorted(result)
    return result

def getListedNews(samples):
    refwords = getPeakKeywords(samples)
    samples = selectSamples(samples, refwords)

    feat = getFeatureMatrix(samples);
    idx_list = getDisplayedIdx(feat)
    result = {'query':samples['query'], 'data':[]}
    for i in idx_list:
        news = samples['data'][i]
        news['content'] = getSummary(news['news_title'].encode('utf8'), news['content'].encode('utf8'))
	if len(news['content']) < 1:
	    continue
        result['data'].append(news)
	print news['source_url']
	print news['content']
    return result

def getPeakKeywords(samples):
    peakCnt = 0
    content = ''
    for news in samples['data']:
	if (news['news_amount'] > peakCnt):
	    peakCnt = news['news_amount']
	    content = news['content']
    tags = jieba.analyse.extract_tags(content, topK=200)
    return tags

def selectSamples(samples, refwords):
    sim = []
    for news in samples['data']:
        tags = jieba.analyse.extract_tags(news['content'], topK=200)
	union_set = {}
        cross_set = {}
        for w in refwords:
            union_set[w] = 1
            if w in tags:
                cross_set[w] = 1
        for w in tags:
            union_set[w] = 1
    	sim.append((len(cross_set) + 0.0) / (len(union_set) + 0.0))
    result = {'query':samples['query'], 'data':[]}
    ok = False
    for i in xrange(len(sim)):
	if sim[i] >= 0.08:
	    ok = True
	if ok:
	    result['data'].append(samples['data'][i])
    return result

if __name__ == '__main__':
    obj = {}
    with open('microsoft.json', 'rb') as datafile:
	obj = json.load(datafile)
    result = getListedNews(obj)
    json_content = json.dumps(result)
    fout = open('result_microsoft' + '.json', 'w')
    fout.write(json_content)
