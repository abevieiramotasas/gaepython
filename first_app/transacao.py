from google.appengine.ext import db
from entidade import User

# transações com db

def cria_dois_user(key):
    u1 = db.get(key)
    u1.nickname = u1.nickname+'1'
    u1.put()


def executa_com_transacao():
    # executa a transação definida em cria_dois_user
    key = 'kelly key'
    db.run_in_transaction(cria_dois_user, key)
