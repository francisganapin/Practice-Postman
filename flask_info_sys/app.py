from flask import Flask
from extensions import db,ma
from routes import student_bp
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(student_bp,url_prefix='/api/students')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)