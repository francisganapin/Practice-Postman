from data import session, Student

students = session.query(Student).all()

for student in students:
    if student.score >= 85:
        print(f"{student.name} is an honor student")
    else:
        print(f"{student.name} needs improvement")
