from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///petsalon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Our model
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    species = db.Column(db.String(50))
    age = db.Column(db.Integer)
    owner = db.Column(db.String(100))

with app.app_context():
    db.create_all()


@app.route('/pets',methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    pets_list = [
        {"id": pet.id, "name": pet.name, "species": pet.species, "age": pet.age, "owner": pet.owner}
        for pet in pets
    ]
    return jsonify(pets_list)

@app.route('/pets/<int:pet_id>',methods=['GET'])
def get_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if not pet:
        return jsonify({'error':"Pet not Found"}),404
    return jsonify({"id": pet.id, "name": pet.name, "species": pet.species, "age": pet.age, "owner": pet.owner})

@app.route('/pets',methods=['POST'])
def add_pet():
    data = request.get_json()
    pet = Pet(
        name=data.get('name'),
        species=data.get('species'),
        age=data.get('age'),
        owner=data.get('owner')
    )
    db.session.add(pet)
    db.session.commit()
    return jsonify({'message':'Pet added','id':pet.id}),201

@app.route('/pets/<int:pet_id>',methods=['GET'])
def update_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if not pet:
        return jsonify({'error':'Pet not found'}),404

    data = request.get_json()
    pet.name = data.get('name',pet.name)
    pet.species = data.get('species',pet.species)
    pet.age = data.get('age',pet.age)
    pet.owner = data.get('owner',pet.owner)
    
    db.session.commit()
    return jsonify({'message':'Pet update'})

@app.route('/pets/<int:pet_id>',methods=['DELETE'])
def delete_pet(pet_id):
    pet = Pet.query.get(pet_id)

    if not pet:
        return jsonify({'error':'Pet not found'}),404

    db.session.delete(pet)
    db.session.commit()
    return jsonify({'message':'Pet deleted'})

if __name__ == '__main__':
    app.run(debug=True)