from flask import Flask,request,jsonify
from model import db,GymMember
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/api/gym-member/<int:member_id>/update-expiry',methods=['POST'])
def update_expiry(member_id):

    member = GymMember.query.get(member_id)

    if not member:
        return jsonify({'error':"Member not Found"}),404
    
    data = request.get_json()
    new_expiry = data.get('expiry')


    if not new_expiry:
        return jsonify({'error':'expiry is required'}),400
    
    try:
        member.expiry = datetime.strptime(new_expiry,"%Y-%m-%d").date()
        db.session.commit()
    except ValueError:
        return jsonify({"error":"Invalid date format,use YYYY-MM-DD"}),400
    
    return jsonify({
        'success':True,
        'id':member.id,
        'first_name':member.first_name,
        'last_name':member.last_name,
        'expiry':member.expiry.strftime("%Y-%m-%d")
    }),200


@app.route('/api/gym-member',methods=['GET'])
def get__all_member():
    member = GymMember.query.all()
    result = []

    for m in member:
        result.append({
            'id':m.id,
            'first_name':m.first_name,
            'last_name':m.last_name,
            'expiry':m.expiry.strftime('%Y-%m-%d') if m.expiry else None
        })

    return jsonify(result),200


@app.route('/api/gym-member/<int:member_id>',methods=['DELETE'])
def delete_member(member_id):
    member = GymMember.query.get(member_id)
    if not member:
        return jsonify({"error":"Member not Found"}),404
    
    db.session.delete(member)
    db.session.commit()
    
    return jsonify({"success":True,"message":"Member deleted"}),200

@app.route('/api/gym-members/search',methods=['GET'])
def search_members():
    q = request.args.get('q','')
    members = GymMember.query.filter(
        (GymMember.first_name.ilike(f"%{q}%")) |
        (GymMember.last_name.ilike(f"{q}")) |
        (GymMember.id.ilike(f"%{q}"))
        
    ).all()

    return jsonify([{
        'id':m.id,
        'expiry':m.expiry,
        'name': f"{m.first_name} {m.last_name}",
    } for m in members]),200

if __name__ == '__main__':
    app.run(debug=True)