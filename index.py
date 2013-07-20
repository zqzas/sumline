
import web
import os
from bae.api import logging

urls = (
    '/', 'Hello' 
)
 
app_root = os.path.dirname(__file__)
templates_root = app_root   # os.path.join(app_root, 'client')
render = web.template.render(templates_root)
 
class Hello:        
    def GET(self):
      	q = web.input(q1=None)
      	q = web.input(q2=None)
      	query = None
        if hasattr(q, 'q1'):
            query = q.q1
        elif hasattr(q, 'q2'):
            query = q.q2
        if query:
            # TODO call server
            return render.search()
        return render.index()
 
app = web.application(urls, globals()).wsgifunc()
 
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)
