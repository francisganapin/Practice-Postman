from flask import Blueprint,request,jsonify
from extensions import db
from models import Teacher
from schemas import TeacherSchema

teacher_bp = Blueprint('teacher_bp',__name__,url_prefix='/api/teachers')

teacher_schema =  TeacherSchema()
teachers_schema = TeacherSchema(many=True)

@teacher_bp.route('/',methods=['POST'])
def add_teacher():
    data = request.get_json()
    teacher = teacher_schema.load(data)
    db.session.add(teacher)
    db.session.commit()
    return teacher_schema.jsonify(teacher),201


@teacher_bp.route('/',methods=['GET'])
def get_teacher():
    all_teacher = Teacher.query.all()
    return teachers_schema.jsonify(all_teacher)

@teacher_bp.route('/<int:id>',methods=['GET'])
def get_teacher_id(id):
    teacher = Teacher.query.get_or_404(id)
    return teacher_schema.jsonify(teacher)

@teacher_bp.route('/update/<int:id>',methods=['PUT'])
def update_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.update(teacher)
    data = request.get_json()
    updated_teacher = teacher_schema.load(data,instance=teacher,partial=True)
    db.session.commit()
    return teacher_schema.jsonify(updated_teacher)

@teacher_bp.route('/delete/<int:id>',methods=['DELETE'])
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    return jsonify({'message':'Teacher deleted successfully'})