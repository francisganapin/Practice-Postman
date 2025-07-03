from data import session,Student

student_name = input('Insert Name: ').strip()



if not student_name:
    print('No name entered. Please provide a valid name.')
else:
    student = session.query(Student).filter_by(name=student_name).first()

    if student:
        if student.score + 10 > 100:
            print(f"Score limit exceeded:{student.score + 10 }")
        else:
            student.score += 10
            session.commit()
            print(f"Updated score to {student.score}")
    else:
        print('Student not Found')