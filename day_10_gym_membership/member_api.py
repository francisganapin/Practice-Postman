from flask import Flask,request,jsonify
from instance.member_model import db,Member



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///members.db'
app.config['SQLALCHMEY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return 'Welcome to the Member Api'


#get list of all member
@app.route('/member/list',methods=['GET'])
def get_member():
    member_list = Member.query.all()
    serialized = []
    for m in member_list:
        serialized.append({
            'id':m.id,
            'first_name':m.first_name,
            'last_name':m.last_name,
            'phone_number':m.phone_number,
            'start_date':m.start_date.isoformat()
        })
    return jsonify(serialized)



if __name__ == '__main__':
    app.run(debug=True)