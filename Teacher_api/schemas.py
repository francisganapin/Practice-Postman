from extensions import ma
from models import Student


class StudentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Student
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field(required=True)
    age = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    