# coding=utf8
from inspect import ismethod

class Test():
    def test_genurl(self):
        from urlencoder import genurl
        from datetime import date
        query = u'韩亚航空'
        the_date = date(2013, 7, 19)
        print genurl(query, the_date)

    def test_geturl_web(self):
        from urlencoder import genurl_web
        query = u'韩亚航空'
        print genurl_web(query)


def call_all(obj):
    for name in dir(obj):
        attribute = getattr(obj, name)
        if ismethod(attribute):
            attribute()
    
if __name__ == '__main__':
    call_all(Test())

