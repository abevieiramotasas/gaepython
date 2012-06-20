import cgi
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

form = """
    <html>
        <body>
            Oi %s, gostaria de se cadastrar?
            <form action="/teste" method="post">
                <input type="hidden" name="nickname" value="%s"/>
                <div><input type="submit" value="Cadastrar" /></div>
            </form>
        </body>
    </html>
"""

class User(db.Model):
    nickname = db.StringProperty()
    

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()    
        if user:
            self.response.headers['Content-type'] = 'text/html'
            self.response.out.write(form %(user.nickname(),user.nickname()))
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Teste(webapp.RequestHandler):
    def get(self):
        users_db = db.GqlQuery("SELECT * FROM User")
        for user in users_db:
            self.response.out.write(user.nickname())
    def post(self):
        user = User()
        user.nickname = self.request.get('nickname')
        user.put()
        users_db = db.GqlQuery("SELECT * FROM User")
        for user in users_db:
            self.response.out.write("%s</br>" %(user.nickname))

application = webapp.WSGIApplication([
    ('/', MainPage), 
    ('/teste', Teste)
    ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
