from flask import request
from flask_restx  import Namespace,Resource
from extensions import db
from model import User,GymMember
from schema import UserSchema,GymMemberSchema
from flask_jwt_extended import create_access_token,jwt_required
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

auth_ns = Namespace('auth')
member_ns = Namespace('members')

user_schema = UserSchema()
member_schema = GymMemberSchema()
members_schema = GymMemberSchema(many=True)


@auth_ns.route('/register')
class Register(Resource):
    def post(self):
        data= request.json
        hashed_pw = generate_password_hash(data['password'])
        new_user = User(username=data['username'],password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user),201
    
@auth_ns.route('/login')
class Login(Resource):
    def post(self):
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password,data['password']):
            token = create_access_token(identity=user.id)
            return {'access_token':token},200
        return {'error':'Invalid Credentials'},401
    
@member_ns.route('/')
class MemberList(Resource):
    @jwt_required()
    def get(self):
        members = GymMember.query.all()
        return member_ns.dump(members),200
    
    @jwt_required()
    def post(self):
        data = request.json
        member = GymMember(
            first_name=data['first_name'],
            last_name=data['last_name'],
            expiry=datetime.strptime(data['expiry'],'%Y-%m-%d').date()
        )
        db.session.add(member)
        db.session.commit()
        return member_schema.dump(member),201
    
@member_ns.route('/<int:id>/update-expiry')
class UpdateExpiry(Resource):
    @jwt_required()
    def patch(self,id):
        member = GymMember.query.get_or_404(id)
        data = request.json
        member.expiry = datetime.strptime(data['expiry'],'%Y-%m-%d').date()
        db.session.commit()
        return member_schema.dump(member),200