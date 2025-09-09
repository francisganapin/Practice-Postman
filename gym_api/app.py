from flask import Flask
from extensions import db,migrate,jwt
from routes import auth_ns,member_ns
from flask_restx import Api


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym.db'
    app.config['JWT_SECRET_KEY'] = 'super-secret'

    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)

    api = Api(app,title='Gym Api',version='1.0',description='Gym Members Api')
    api.add_namespace(auth_ns,path='/api/auth')
    api.add_namespace(member_ns,path='/api/members')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)