from data import session,Student

student = session.query(Student).filter_by(name='Bob').first()


if student:
    if student.score + 10 > 100:
        print(f'Score limit exceeded: {student.score + 10} is greater than 100')
    else:
        student.score += 10
        session.commit()
        print(f'Updated score to {student.score}')