# -*- encoding: utf-8 -*-
# modulos da app
from entidade import CadastrarHandler
from entidade import TodosUsersHandler
from entidade import ExpandoHandler
from entidade import User
# modulos gerais
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
# template
import logging
import os
from google.appengine.ext.webapp import template
# stats
from google.appengine.ext.db import stats
# blobstore
from blobstore import BlobstoreHandler
from blobstore import BlobUploadHandler



# mostra as variáveis de ambiente
# ! ver template, porque deu um trabalhim danado pra usar dicionário
class EnvironmentHandler(webapp.RequestHandler):
    def get(self):
        # retirado da documentação        
        environment_map = {}
        for name in os.environ.keys():
            environment_map[name] = os.environ[name]

        # estatísticas - não funcionou :(
#        global_stat = stats.GlobalStat.all().get()
#        total_bytes = global_stat.bytes
#        total_count = global_stat.count
        template_values = {
            'environment_map' : environment_map
#            'bytes' : total_bytes,
#            'count' : total_counts
        }
        path = os.path.join(os.path.dirname(__file__), 'environment.html')
        self.response.out.write(template.render(path, template_values))

# aplicação
application = webapp.WSGIApplication([
    ('/', CadastrarHandler), 
    ('/user', TodosUsersHandler),
    ('/env', EnvironmentHandler),
    ('/expando', ExpandoHandler),
    ('/blobstore', BlobstoreHandler),
    ('/blobstorehandler', BlobUploadHandler)
    ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
