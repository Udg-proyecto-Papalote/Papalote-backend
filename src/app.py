from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from config import MONGODB_URI

# Create the Flask app
app = Flask(__name__)

# Configure the database
app.config['MONGO_URI'] = MONGODB_URI

# Create the PyMongo instance
mongo = PyMongo(app)



# Define the route
@app.route('/users', methods=['POST'])
def create_user():
    # Receive the data
    email = request.json['email']
    password = request.json['password']
    name = request.json['name']

    if email and password and name:
        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the data
        id = mongo.db.users.insert_one({
            'email': email,
            'password': hashed_password,
            'name': name
        })

        # Return the id
        return jsonify({'id': str(id.inserted_id)})
    else:
        return jsonify({'error': 'Missing parameters'})

# Define the route
@app.route('/users', methods=['GET'])
def get_users():
    # Get the data from the database
    users = mongo.db.users.find()

    # Convert the data to JSON
    response = json_util.dumps(users)

    # Return the response
    return Response(response, mimetype='application/json')


# Error handler
@app.errorhandler(404)
def not_found(error=None):
    message = jsonify({
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    })

    message.status_code = 404

    return message

# Error handler: missing parameters
@app.errorhandler(400)
def bad_request(error=None):
    message = jsonify({
        'message': 'Missing parameters',
        'status': 400
    })

    message.status_code = 400

    return message

# Debug mode
if __name__ == '__main__':
    app.run(debug=True)