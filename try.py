from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
import bcrypt
import jwt
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB and JWT configuration
app.config['MONGO_URI'] = 'mongodb+srv://ifty:nxzhhhlWutt7PcMh@cluster0.bd9ywas.mongodb.net/mydatabase?retryWrites=true&w=majority&appName=Cluster0'
app.config['SECRET_KEY'] = 'your_secret_key'

mongo = PyMongo(app)

# HTML Page Routes
@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/signup-page')
def signup_page():
    return render_template('signup.html')

@app.route('/login-page')
def login_page():
    return render_template('login.html')

@app.route('/profile-page')
def profile_page():
    return render_template('profile.html')

# API: Signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    if mongo.db.users.find_one({'email': email}):
        return jsonify({'message': 'User already exists'}), 409

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    mongo.db.users.insert_one({
        'email': email,
        'password': hashed_pw,
        'first_name': data.get('firstName'),
        'last_name': data.get('lastName'),
        'phone': data.get('phone'),
        'district': data.get('district'),
        'gender': data.get('gender'),
        'created_at': datetime.datetime.utcnow()
    })

    return jsonify({'message': 'Signup successful'}), 201

# API: Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = mongo.db.users.find_one({'email': email})
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    stored_password = user.get('password')
    if isinstance(stored_password, str):
        stored_password = stored_password.encode('utf-8')

    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
        token = jwt.encode(
            {'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# API: Profile
@app.route('/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 403

    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': f"Welcome {decoded['email']}!"})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

# API: Logout
@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
