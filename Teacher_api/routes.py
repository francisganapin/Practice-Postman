from flask import Blueprint,request,jsonify
from extensions import db
from models import  Student
from schemas import StudentSchema

student_bp = Blueprint('student_bp',__name__,url_prefix='/api/students')

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

@student_bp.route('/',methods=['POST'])
def add_student():
    data = request.get_json()
    student = student_schema.load(data)
    db.session.add(student)
    db.session.commit()
    return student_schema.jsonify(student),201

@student_bp.route('/',methods=['GET'])
def get_all_students():
    all_student = Student.query.all()
    return students_schema.jsonify(all_student)

@student_bp.route('/<int:id>',methods=['GET'])
def get_students(id):
    student = Student.query.get_or_404(id)
    return student_schema.jsonify(student)

@student_bp.route('/<int:id>',methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get__json()
    update_student = student_schema.load(data,instance=student,partial=True)
    return student_schema.jsonify(update_student)

@student_bp.route('/<int:id>',methods=['DELETE'])
def delete_student(id):
    student = Student.quey.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message":"Student Deleted successfully"})