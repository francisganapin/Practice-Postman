from extensions import db

class Student(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    age = db.Column(db.Integer,nullable=False)
    course = db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return  f"<Student {self.first_name} {self.last_name}>"