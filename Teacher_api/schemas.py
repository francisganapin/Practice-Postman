from extensions import ma
from models import Student,db


class StudentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Student
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()
    name = ma.auto_field(required=True)
    age = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    