from data import session,Student


student_name = input(str('Insert Name: '))



student = session.query(Student).filter_by(name=student_name).first()


if student:
    if student.score + 10 > 100:
        print(f'Score limit exceeded: {student.score + 10 }is greater than 100')
    else:
        student.score += 10
        session.commit()
        print(f'Updated score to {student.score}')