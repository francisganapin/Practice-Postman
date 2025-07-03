from sqlalchemy import Column,Integer,String,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import CheckConstraint

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    score = Column(Integer)

    __table_args__ = (
    CheckConstraint('score <= 100',name='check_score_max'),
)


engine = create_engine('sqlite:///students.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()