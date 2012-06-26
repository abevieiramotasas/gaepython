# -*- encoding: utf-8 -*-
# modulos gerais
from google.appengine.ext.webapp.util import run_wsgi_app


# aplicação
application = webapp.WSGIApplication([
    ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
