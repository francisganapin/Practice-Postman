from sqlmodel import create_engine,Session
from member_model import Member
from datetime import date


engine = create_engine('sqlite:///members.db')


from sqlmodel import SQLModel
SQLModel.metadata.create_all(engine)


with Session(engine) as session:
    member = Member(
        first_name='Samson',
        last_name='Castro',
        phone_number='09123456789',
        start_date=date.today()
    )
    session.add(member)
    session.commit()
    session.refresh(member)
    print('new member added with ID:',member.id)