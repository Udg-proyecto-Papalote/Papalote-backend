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



# Register a new user
@app.route('/users', methods=['POST'])
def create_user():
    # Receive the data
    email = request.json['email']
    password = request.json['password']
    name = request.json['name']

    response = None

    if email and password and name:
        # Hash the password
        hashed_password = generate_password_hash(password)

        # Check if the user already exists
        user = mongo.db.users.find_one({'email': email})

        if user:
            response = jsonify({'message': 'User already exists'})
            response.status_code = 400
            return response

        # Insert the data
        id = mongo.db.users.insert_one({
            'email': email,
            'password': hashed_password,
            'name': name
        })

        response = jsonify({
            'message': 'User created successfully',
            'id': str(id)
        })
        response.status_code = 201
    
    return response
    

# Login
@app.route('/login', methods=['POST'])
def login():
    # Receive the data
    email = request.json['email']
    password = request.json['password']

    response = None

    if email and password:
        # Get the user from the database
        user = mongo.db.users.find_one({'email': email})

        if user:
            # Check the password
            if check_password_hash(user['password'], password):
                # Add the user ID and name to the headers
                response.headers['user_id'] = str(user['_id'])
                response.headers['name'] = user['name']
                response = jsonify({'message': 'Login successful'})
                response.status_code = 200
                

            else:
                response = jsonify({'message': 'Wrong password'})
                response.status_code = 400
        else:
            response = jsonify({'message': 'User not found'})
            response.status_code = 400

    return response

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