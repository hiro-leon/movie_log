import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #sqlite3データベースの場所や名前を指定
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(os.path.abspath(os.path.dirname(__file__)), 'web/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY ='my_secret_key'
    ITEM_PER_PAGE = 3
    DIRECTORS_PER_PAGE = 3
