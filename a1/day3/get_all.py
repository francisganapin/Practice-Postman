from data import session, Student

students = session.query(Student).all()

for student in students:
    print(student.name)