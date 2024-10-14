from flask import Flask, jsonify, request, abort
import logging

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask API!"

@app.route('/data', methods=['GET'])
def data():
    return jsonify({"message": "Hello, World!", "status": "success"})

@app.route('/user/<username>', methods=['GET'])
def user(username):
    return jsonify({"message": f"Hello, {username}!", "status": "success"})

@app.route('/query', methods=['GET'])
def query():
    name = request.args.get('name', 'Guest')
    age = request.args.get('age', 'unknown')
    return jsonify({"message": f"Hello, {name}!", "age": age, "status": "success"})

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    if not data:
        abort(400, description="Invalid data")
    return jsonify({"message": "Data received", "data": data, "status": "success"})

@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    if not data:
        abort(400, description="Invalid data")
    return jsonify({"message": f"Data with id {id} updated", "data": data, "status": "success"})

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    return jsonify({"message": f"Data with id {id} deleted", "status": "success"})

# Configure logging
logging.basicConfig(level=logging.ERROR)

@app.errorhandler(404)
def not_found(error):
    logging.error(f"404 error: {error}")
    return jsonify({"message": "Resource not found", "status": "error"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"message": error.description, "status": "error"}), 400

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    if not data or 'password' not in data:
        abort(400, description="Password is required")
    
    password = data['password']
    if len(password) < 8:
        return jsonify({"message": "Password is too short", "status": "error"}), 400
    if not any(char.isdigit() for char in password):
        return jsonify({"message": "Password must contain at least one digit", "status": "error"}), 400
    if not any(char.isupper() for char in password):
        return jsonify({"message": "Password must contain at least one uppercase letter", "status": "error"}), 400
    if not any(char.islower() for char in password):
        return jsonify({"message": "Password must contain at least one lowercase letter", "status": "error"}), 400
    if not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?/' for char in password):
        return jsonify({"message": "Password must contain at least one special character", "status": "error"}), 400
    
    return jsonify({"message": "Password is valid", "status": "success"})
if __name__ == '__main__':
    app.run(debug=True)