# -*- encoding: utf-8 -*-
# modulos da app
from entidade import CadastrarHandler
from entidade import TodosUsersHandler
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



# mostra as variáveis de ambiente
# ! ver template, porque deu um trabalhim danado pra usar dicionário
class EnvironmentHandler(webapp.RequestHandler):
    def get(self):
        # retirado da documentação
        
        environment_map = {}
        for name in os.environ.keys():
            environment_map[name] = os.environ[name]
        template_values = {
            'environment_map' : environment_map
        }
        path = os.path.join(os.path.dirname(__file__), 'environment.html')
        self.response.out.write(template.render(path, template_values))

# aplicação
application = webapp.WSGIApplication([
    ('/', CadastrarHandler), 
    ('/user', TodosUsersHandler),
    ('/env', EnvironmentHandler)
    ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
