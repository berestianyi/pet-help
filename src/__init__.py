import os

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_wtf import CSRFProtect
from config import Config

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
app.config['WTF_CSRF_CHECK_DEFAULT'] = False
app.config['UPLOAD_FOLDER'] = '/src/static/'
app.config['UPLOAD_FOLDER_FOR_SHELTER'] = './static/uploads/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
admin = Admin(app, name='PetsHelp', template_mode='bootstrap3')
