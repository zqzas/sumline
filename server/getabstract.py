import urllib2, urllib
import json

def getUnicodeFromFile(filename):
    content = ''
    with open(filename, 'rb') as inputFile:
        for row in inputFile:
            row = row.strip()
            content = content + row
    return content.decode('gb18030').encode('utf8')
    
def getSummary(title, content):
    values = {'key': 'mgwqQFlwPhUvO5Oy', 'title': title, 'content': content}
    f = urllib2.urlopen(url = 'http://api.tuofeng.cn/zhaiyao/article', data = urllib.urlencode(values) )
    result = f.read()
    resultJson = json.loads(result)
    try:
        result = resultJson["summary"]['middleAbstract']
        return result
    except:
        return ''

if __name__ == '__main__':
    content = getUnicodeFromFile('test.txt')
    title = 'hello world'
    a = getSummary(title, content)
    print a
