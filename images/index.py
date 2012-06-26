# -*- encoding: utf-8 -*-
# modulos gerais
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from images import *
import os
from google.appengine.ext.webapp.util import run_wsgi_app


class IndexHandler(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__)+'/templates', 'index.html')
        self.response.out.write(template.render(path, template_values))


# aplicação
application = webapp.WSGIApplication([
    ('/', IndexHandler),
    ('/upload', UploadHandler),
    ('/upload_image', ImageUploadHandler),
    ('/images/([^/]+)?', ImagesHandler),
    ('/image/([^/]+)?', ImagesHandler_),
    ('/testando', TestandoImageHandler)
    ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
