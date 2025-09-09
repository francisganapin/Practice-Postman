from flask import Blueprint,request,jsonify
from extensions import db
from models import Student
from schemas import StudentSchema


student_bp = Blueprint('student_bp',__name__)

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

@student_bp.route("/", methods=["POST"])
def add_student():
    data = request.json
    new_student = Student(
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=data["age"],
        course=data["course"]
    )

    db.session.add(new_student)
    db.session.commit()   # <-- this saves the student

    return jsonify(student_schema.dump(new_student)), 201



#get all students
@student_bp.route('/',methods=['GET'])
def get_student():
    student = Student.query.all()
    return student_schema.jsonify(student)

@student_bp.route('/<int:id>',methods=['GET'])
def get_student_id(id):
    student = Student.query.get_or_404(id)
    return student_schema.jsonify(student)

@student_bp.route('/<int:id>',methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.json
    student.first_name = data.get('first_name',student.first_name)
    student.last_name = data.get('last_name',student.last_name)
    student.age = data.get('age',student.age)
    student.course = data.get('course',student.course)
    db.session.commit()
    return student_schema.jsonify(student)

@student_bp.route('/<int:id>',methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message":"student deleted succesffuly"})