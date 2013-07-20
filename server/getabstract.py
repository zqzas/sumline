import urllib2, urllib
import json

def getUnicodeFromFile(filename):
    content = ''
    with open(filename, 'rb') as inputFile:
        for row in inputFile:
            row = row.strip()
            content = content + row
    return content.decode('gb18030').encode('utf8')
    
def getSummary(key, content):
    values = {'key': key, 'content': content}
    f = urllib2.urlopen(url = 'http://api.tuofeng.cn/zhaiyao/article', data = urllib.urlencode(values) )
    result = f.read()
    resultJson = json.loads(result)
    return resultJson["summary"]['middleAbstract']

if __name__ == '__main__':
    content = getUnicodeFromFile('test.txt')
    a = getSummary('mgwqQFlwPhUvO5Oy', content)
    print a