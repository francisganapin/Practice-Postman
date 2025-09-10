from extensions import ma
from models import Teacher

class TeacherSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field(required=True)
    position = ma.auto_field(required=True)
    salary = ma.auto_field(required=True)
