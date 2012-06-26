# -*- encoding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.api import images
import os
from google.appengine.ext.webapp import template
import logging
import urllib


class ImageUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    uploaded = self.get_uploads()[0]
    self.redirect('/images/%s' % uploaded.key())


class UploadHandler(webapp.RequestHandler):
  def get(self):
    template_values = {}
    template_values['upload_url'] = blobstore.create_upload_url('/upload_image')  
    path = os.path.join(os.path.dirname(__file__)+'/templates', 'upload.html')
    self.response.out.write(template.render(path, template_values))

class ImagesHandler_(webapp.RequestHandler):
  def get(self, image_id):
    template_values = {}
    template_values['url'] = "/images/%s" % urllib.unquote(image_id)
    path = os.path.join(os.path.dirname(__file__)+'/templates', 'image.html')
    self.response.out.write(template.render(path, template_values))      

class ImagesHandler(blobstore_handlers.BlobstoreDownloadHandler):
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


class TestandoImageHandler(webapp.RequestHandler):
  def get(self):
    # pego o primeiro blob(considero que estou uploadando apenas images)
    blob_info = blobstore.BlobInfo.all().fetch(1, 0)[0]
    #blob = blobstore.get(blob_info.key())
    self.response.out.write(images.get_serving_url(blob_info.key()))
    return
    if blob_info:
      img = images.Image(blob_info)
      #img.resize(width=80, height=100)
      #img.im_feeling_lucky()
      #logging.info(img.width)
      #thumbnail = img.execute_transforms(output_encoding=images.JPEG)
      self.response.headers['Content-Type'] = 'image/jpeg'
      self.response.out.write(img)
      return
    self.error(404)
