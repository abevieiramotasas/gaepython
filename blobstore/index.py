# -*- encoding: utf-8 -*-
# modulos gerais
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from blobstore import *



# aplicação
application = webapp.WSGIApplication([
    ('/', BlobstoreHandler),
    ('/upload', BlobUploadHandler),
    ('/uploads', UploadsHandler),
    ('/download/(.*)', BlobDownloadHandler)
    ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
