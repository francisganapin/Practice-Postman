from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///members.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

class Member(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)


class MemberResource(Resource):
    def post(self):
        data = request.get_json()

        errors = {}

        if not data.get('first_name'):
            errors['first_name'] = 'First name is required'
        if not data.get('last_name'):
            errors['last_name'] = 'Last name is required'
        if not data.get('email'):
            errors['email'] = 'Email name is required'

        if errors:
            return {'errors':errors},400
        
        member = Member(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )

        db.session.add(member)
        db.session.commit()
        return {'message':"Member added successfully"},201

api.add_resource(MemberResource,'/members')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)