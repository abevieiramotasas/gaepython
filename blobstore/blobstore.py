# -*- encoding: utf-8 -*-
from google.appengine.ext.blobstore import MAX_BLOB_FETCH_SIZE
from google.appengine.ext import webapp

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
import os
import logging
import urllib

class Upload(db.Model):
   user = db.UserProperty()
   blobkey = blobstore.BlobReferenceProperty()
   filename = db.StringProperty()
    

class BlobstoreHandler(webapp.RequestHandler):
   def get(self):
      user = users.get_current_user()
      template_values = {}
      if not user:
         template_values['logado'] = False
         template_values['user_url_link'] = users.create_login_url(self.request.uri)
         template_values['user_url'] = 'Login'
      else:
         template_values['logado'] = True
         template_values['user'] = user
         template_values['upload_url'] = blobstore.create_upload_url('/upload')    
         template_values['user_url_link'] = users.create_logout_url(self.request.uri)
         template_values['user_url'] = 'Logout'
      path = os.path.join(os.path.dirname(__file__)+'/templates', 'index.html')
      self.response.out.write(template.render(path, template_values))

class BlobUploadHandler(blobstore_handlers.BlobstoreUploadHandler):    
   def post(self):
      user = users.get_current_user()
      if not user:
         self.redirect('/')
      if not self.get_uploads():
         self.redirect('/uploads')
      else:
         uploaded = self.get_uploads()[0]
         upload = Upload()
         upload.user = user
         upload.blobkey = uploaded.key()
         upload.filename = uploaded.filename
         upload.put()
         self.redirect('/uploads')

class BlobDownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
   def get(self, blobkey):
      blobkey = urllib.unquote(blobkey)
      if not blobstore.get(blobkey):   
         self.error(404)
      else:
         upload = db.Query(Upload)
         upload.filter("blobkey", blobkey)
         filename = (upload.get()).filename
         self.send_blob(blobkey, save_as=filename)

class UploadsHandler(webapp.RequestHandler):
   def get(self):
      template_values = {}
      template_values['uploads'] = Upload.all()
      path = os.path.join(os.path.dirname(__file__)+'/templates', 'uploads.html')
      self.response.out.write(template.render(path, template_values))


      
        
