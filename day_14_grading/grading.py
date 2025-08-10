from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grades.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class StudentGrade(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    student_name = db.Column(db.String(80), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    grade_category = db.Column(db.String(2), nullable=False) 

    def as_dict(self):
        return{
            'id':self.id,
            'student_name':self.student_name,
            'grade':self.grade,
            'grade_category':self.grade_category
                            }
    
with app.app_context():
    db.create_all()

def get_grade_category(score):
    if score >= 90:
        return '1'
    elif score >= 80:
        return '2'
    elif score >= 70:
        return '3'
    elif score >= 60:
        return  '4'
    else:
        return 'F'
    
# add grade
@app.route('/grade',methods=['POST'])
def add_grade():
    data = request.json
    student_name = data.get('student_name')
    grade = data.get('grade')

    if student_name is None or grade is None:
        return jsonify({'error':'student and grade is required'}),400
    
    try:
        grade = float(grade)
    except ValueError:
        return jsonify({"error":'grade must be a number'}),400

    grade_category = get_grade_category(grade)

    student = StudentGrade(
            student_name=student_name,
            grade=grade,
            grade_category=grade_category
    )
    db.session.add(student)
    db.session.commit()
    return jsonify(student.as_dict()), 201


@app.route('/grade',methods=['GET'])
def get_grade():
    student = StudentGrade.query.all()
    return jsonify([s.as_dict() for s in student])


if __name__ == '__main__':
    app.run(debug=True)