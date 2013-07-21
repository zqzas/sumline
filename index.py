
import web
import os
import sys

urls = (
    '/', 'Main' 
)
 
app_root = os.path.dirname(__file__)
templates_root = app_root   # os.path.join(app_root, 'client')
render = web.template.render(templates_root)
sys.path.insert(0, 'server')

class Main:        
    def GET(self):
      	q = web.input()
      	q = web.input()
      	query = None
        if hasattr(q, 'q1'):
            query = q.q1
        elif hasattr(q, 'q2'):
            query = q.q2
        if query:
            from controller import main
            main(query)
            return render.search()
        # self.test_mongodb() # How-to use MongoDB
        # self.demo_prepare()
        return render.the_index()

    def demo_prepare(self):
        from dbaccess import save, fetch
        files = ['server/demo_91.json', 'server/demo_hanya.json', 'server/demo_microsoft.json']
        kw = [u'收购91无线', u'韩亚航空失事', u'微软合并部门']
        for data, idx in zip(files, kw):
            raw = open(data).read()
            obj = {'query': idx, 'data': raw}
            save(obj, 'dai')

app = web.application(urls, globals()).wsgifunc()
 
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)



