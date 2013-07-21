
import web
import os
import sys

urls = (
    '/', 'Hello' 
)
 
app_root = os.path.dirname(__file__)
templates_root = app_root   # os.path.join(app_root, 'client')
render = web.template.render(templates_root)
sys.path.insert(0, 'server')

class Hello:        
    def GET(self):
      	q = web.input()
      	q = web.input()
      	query = None
        if hasattr(q, 'q1'):
            query = q.q1
        elif hasattr(q, 'q2'):
            query = q.q2
        if query:
            # TODO call server
            from 
            return render.search()
        # self.test_mongodb() # How-to use MongoDB
        return render.the_index()

    def test_mongodb(self):
        from dbaccess import save, fetch
        save({'a': 1, 'b':2}, "arapat")
        return fetch({'a':1}, "arapat")
 
app = web.application(urls, globals()).wsgifunc()
 
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)



