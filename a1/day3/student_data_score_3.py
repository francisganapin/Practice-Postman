from data import session,Student


while True:
    student_name = input('Insert Name: ').strip()

    if not student_name:
        print('No name entered. Please try again. \n')
        continue

    student = session.query(Student).filter_by(name=student_name).first()

    if not student:
        print(f'Student named "{student_name}" does not exist.\n')
        continue


    if student.score + 10 > 100:
        print(f'Score limit exceeded: {student.score + 10} is already greater than 100')
    else:
        student.score += 10
        session.commit()
        print(f'Updated score to {student.score}')
    break