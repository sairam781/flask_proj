"""JWT based authentication"""
from flask import *
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,get_jwt_identity
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '12345678'  # Change this to your desired secret key
jwt = JWTManager(app)
# Example users database (for demonstration purposes)
users = {
    'john': 'password123',
    'mary': 'pass123'
}
# Endpoint to generate access token
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    if users.get(username) != password:
        return jsonify({"msg": "Invalid username or password"}), 401
    access_token = create_access_token(identity=username)
    print("AccessToken",access_token)
    return jsonify(access_token=access_token), 200
# Protected route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    print("Protected ROute")
    current_user = get_jwt_identity()
    print("Current User",current_user)
    return jsonify(logged_in_as=current_user), 200
if __name__ == '__main__':
    app.run(debug=True)


