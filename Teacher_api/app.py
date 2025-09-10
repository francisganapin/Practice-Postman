from flask import Flask
from extensions import db,ma
from routes import student_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

      # Enable CORS for all routes
    CORS(app)   # <---


    db.init_app(app)
    ma.init_app(app)


    app.register_blueprint(student_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)