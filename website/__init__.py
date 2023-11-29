from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, environ
from flask_login import LoginManager
import psycopg2

db = SQLAlchemy()
DB_NAME = "database.db"
your_password = 'whatisthepassword23@'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fgcu2024'

    # Azure PostgreSQL Database URI
    ##connection_string = "postgresql://fgcuascecl:whatisthepassword23@fgculivesports.postgres.database.azure.com:5432/postgres"
    ###app.config['SQLALCHEMY_DATABASE_URI'] = psycopg2.connect(user="fgcuascecl", password="whatisthepassword23@", host="fgculivesports.postgres.database.azure.com", port=5432, database="postgres")
    ##app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://fgcuascecl:whatisthepassword23@@fgculivesports.postgres.database.azure.com:5432/postgres"

    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if app.config['SQLALCHEMY_DATABASE_URI']:
        db.create_all(app=app)
        print('Created Database!')

#fgcuascecl admin username 
#password: whatisthepassword23@