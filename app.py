from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['user_db']
users_collection = db['users']

# Helper function to convert ObjectId to string
def serialize_id(document):
    document['_id'] = str(document['_id'])
    return document

# GET all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = list(users_collection.find())
    serialized_users = [serialize_id(user) for user in users]
    return jsonify(serialized_users), 200

# GET a specific user by ID
@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    if user:
        serialized_user = serialize_id(user)
        return jsonify(serialized_user), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# POST a new user
@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    new_user = {
        'name': user_data['name'],
        'email': user_data['email'],
        'password': user_data['password']
    }
    result = users_collection.insert_one(new_user)
    return jsonify({'message': 'User created successfully', 'id': str(result.inserted_id)}), 201

# PUT/update a user by ID
@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    updated_user = {
        'name': user_data['name'],
        'email': user_data['email'],
        'password': user_data['password']
    }
    result = users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': updated_user})
    if result.modified_count > 0:
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# DELETE a user by ID
@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = users_collection.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
