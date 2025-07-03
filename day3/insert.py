from data import session, Student


student1 = Student(name='Alice',score=90)
student2 = Student(name='Bob',score=75)
student3 = Student(name='Well',score=85)

session.add_all([student1,student2,student3])
session.commit()

print(f'Success input of {student1} and {student2}')