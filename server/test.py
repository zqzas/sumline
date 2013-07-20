# coding=utf8
import unittest

class Test(unittest.TestCase):
    #query_set = [u'韩亚航空', u'阿拉法特', u'马浩'， u'戴涵俊', u'啊速读法速读法舒服1啊速读法暗示']
    def setUp(self):
        self.query_set = [u'韩亚', u'阿拉法特', u'马浩', u'戴涵俊', u'1223jas;kfaks;df;jas啊速读法舒服大是大123123123非']

    def genurl(self, query):
        from urlencoder import genurl
        from datetime import date
        
        the_date = date(2013, 7, 19)
        return genurl(query, the_date)

    def genurl_web(self, query):
        from urlencoder import genurl_web
        
        return genurl_web(query)

    def test_extract_first(self):
        from extractfirst import extract_first
        for query in self.query_set:
            url = self.genurl(query)
            print extract_first(url)

    def test_web_num(self):
        from extractfirst import extract_web_num
        for query in self.query_set:
            url = self.genurl_web(query)
            print extract_web_num(url)

if __name__ == '__main__':
    print 'hh'
    unittest.main()

