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
    

class BlobstoreHandler(webapp.RequestHandler):
   def get(self):
      user = users.get_current_user()
      template_values = {}
      # se não está logado
      if not user:
         template_values['logado'] = False
         template_values['user_url_link'] = users.create_login_url(self.request.uri)
         template_values['user_url'] = 'Login'
      else:
      # caso esteja logado
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
      # se não está logado, vai te logar rapaz
      if not user:
         self.redirect('/')
      # caso não tenha feito upload, envia direto para tela de uploads
      if not self.get_uploads():
         self.redirect('/uploads')
      else:
      # pega o arquivo uploadado
         uploaded = self.get_uploads()[0]
         upload = Upload()
         upload.user = user
         upload.blobkey = uploaded.key()
      # persiste
         upload.put()
         self.redirect('/uploads')

class BlobDownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
   def get(self, blobkey):
   # como é passado como query param, a string vem toda escapada, bem feia
   # mandando um urllib.unquote ela fica bonita
      blobkey = urllib.unquote(blobkey)
      if not blobstore.get(blobkey):   
         self.error(404)
      else:
   # pego o nome do arquivo
         filename = blobstore.BlobInfo.get(blobkey).filename         
   # envio
         self.send_blob(blobkey, save_as=filename)

class UploadsHandler(webapp.RequestHandler):
   def get(self):
      template_values = {}    
      template_values['uploads'] = Upload.all()     
      path = os.path.join(os.path.dirname(__file__)+'/templates', 'uploads.html')
      self.response.out.write(template.render(path, template_values))


      
        
