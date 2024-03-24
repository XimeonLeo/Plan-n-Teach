''' Setting up flask application '''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
  ''' initialiazes the flask app '''
  app = Flask(__name__)
  ''' Secure/encrypt cookies or website data'''
  app.config['SECRET_KEY'] = 'this is just a secret key'
  app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(DB_NAME)
# initialize database
  db.init_app(app)
  
  
  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  
  from .models import User, Note
  
  with app.app_context():
    create_database(app)
    
  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)
  
  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))
  
  return app

def create_database(app):
  if not path.exists('website/' + DB_NAME):
    db.create_all()
    print('Database created!')

# def download_file(app):
#   if not path.exists('website/' + DB_NAME):
#     db.create_all(app=app)
#     print('File successfully saved to database!')
