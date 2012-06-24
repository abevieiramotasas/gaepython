# -*- encoding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
import os
import logging

# definição da entidade User

class User(db.Model):
    nickname = db.StringProperty()

# definição da entidade Pessoa com db.Expando
class Pessoa(db.Expando):
    pass

class ExpandoHandler(webapp.RequestHandler):
    def get(self):
        p = Pessoa()
        # propriedade da instancia, dinamica
        p.nome = "Abelardo Vieira Mota"
        p.put()
        q = Pessoa.all()
        for pessoa in q:
            self.response.out.write(u"Propriedades dinâmicas : "+ str(pessoa.dynamic_properties())+"</br>")
            self.response.out.write(pessoa.nome)

class CadastrarHandler(webapp.RequestHandler):
    def get(self):
        # se está logado
        cadastrar = None
        nickname = None
        user = users.get_current_user()  
        if user:
            # crio link de logout
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            cadastrar = '/user'
            nickname = user.nickname()
        # caso contrário
        else:
            # crio link de login
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        # valores a serem passados para o template
        template_values = {
            'url' : url,
            'url_linktext' : url_linktext,
            'cadastrar' : cadastrar,
            'nickname' : nickname
        }
        # caminho do template
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

# recupera todos os usuários
class TodosUsersHandler(webapp.RequestHandler):
    def get(self):
        # utilizando a interface GqlQuery
        users_db = db.GqlQuery("SELECT * FROM User")
        # poderia ser feito também
        # users_db = User.gql() 
        # que já retorna todas as entidades, podendo ter como parâmetro filtros e order by
        # users_db = User.all()
        template_values = {
            'users' : users_db
        }
        path = os.path.join(os.path.dirname(__file__), 'todosuser.html')
        self.response.out.write(template.render(path, template_values))
    # novo user
    def post(self):
        user = User()
        user.nickname = self.request.get('nickname')
        # adiciona ao datastore
        user.put()
        # utilizando a interface Query
        users_db = User.all()
        template_values = {
            'users' : users_db
        }
        path = os.path.join(os.path.dirname(__file__), 'todosuser.html')
        self.response.out.write(template.render(path, template_values))
