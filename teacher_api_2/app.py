from flask import Flask
from extensions import db,ma
from teacher_routes import teacher_bp
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///teacher.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(teacher_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)