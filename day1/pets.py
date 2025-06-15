from flask import Flask,jsonify,request

app = Flask(__name__)


pets = []
pet_id_counter = 1


@app.route('/pets',methods=['GET'])
def get_pets():

    if not pets:
        return jsonify({"message": "No pets found"}), 200
    else:
        return jsonify(pets)
    


@app.route('/pets',methods=['GET'])
def get_pet(pet_id):
    pet = next((pet for pet in pets if pet['id'] == pet_id),None)
    if pet:
        return jsonify(pet),200
    return jsonify({'error':'Pet not found'}),404


@app.route('/pets',methods=['POST'])
def add_pet():
    global pet_id_counter
    data = request.get_json()
    pet = {
        "id":pet_id_counter,
        'name':data.get('name'),
        'species':data.get('species'),
        'age':data.get('age'),
        'owner':data.get('owner')
    }
    pets.append(pet)
    pet_id_counter += 1
    return jsonify(pet),201

@app.route('/pets/<int:pet_id>',methods=['PUT'])
def update_pet(pet_id):
    data = request.get_json()
    pet  = next((pet for pet in pets if pet['id']==pet_id),None)
    if not pet:
        return jsonify({'error':'Pet not found'}),404
    
    pet.update({
        'name':data.get('name',pet['name']),
        'species':data.get('species',pet['species']),
        "age":data.get("age",pet['age']),
        "owner":data.get('owner',pet['owner'])
    })
    return jsonify(pet),200

@app.route('/pets/<int:pet_id>',methods=['DELETE'])
def delete_pet(pet_id):
    global pets
    pets = [pet for pet in pets if pet['id'] != pet_id]
    return jsonify({'message':'Pet deleted'}),200


if __name__ == '__main__':
    app.run(debug=True)