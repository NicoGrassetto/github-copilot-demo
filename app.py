from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask API!"

@app.route('/data')
def data():
    return jsonify({"message": "Hello, World!", "status": "success"})

@app.route('/user/<username>')
def user(username):
    return jsonify({"message": f"Hello, {username}!", "status": "success"})

@app.route('/query')
def query():
    name = request.args.get('name', 'Guest')
    age = request.args.get('age', 'unknown')
    return jsonify({"message": f"Hello, {name}!", "age": age, "status": "success"})

if __name__ == '__main__':
    app.run(debug=True)