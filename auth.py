from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Patient, Doctor
from db import db

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', help='Username is required', required=True)
register_parser.add_argument('password', help='Password is required', required=True)
register_parser.add_argument('role', help='Role is required (patient or doctor)', required=True)
register_parser.add_argument('name', help='Name is required', required=True)
register_parser.add_argument('age', type=int, help='Age is required for patients')
register_parser.add_argument('gender', help='Gender is required for patients')
register_parser.add_argument('contact', help='Contact is required', required=True)
register_parser.add_argument('specialty', help='Specialty is required for doctors')

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', help='Username is required', required=True)
login_parser.add_argument('password', help='Password is required', required=True)

class Register(Resource):
    def post(self):
        data = register_parser.parse_args()

        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Username already exists'}, 400

        hashed_password = generate_password_hash(data['password'])

        user = User(username=data['username'], password_hash=hashed_password, role=data['role'])
        db.session.add(user)
        db.session.flush()  # To get user.id

        if data['role'] == 'patient':
            if not data.get('age') or not data.get('gender'):
                db.session.rollback()
                return {'message': 'Age and gender required for patients'}, 400
            patient = Patient(name=data['name'], age=data['age'], gender=data['gender'], contact=data['contact'], user_id=user.id)
            db.session.add(patient)
        elif data['role'] == 'doctor':
            if not data.get('specialty'):
                db.session.rollback()
                return {'message': 'Specialty required for doctors'}, 400
            doctor = Doctor(name=data['name'], specialty=data['specialty'], contact=data['contact'], user_id=user.id)
            db.session.add(doctor)
        else:
            db.session.rollback()
            return {'message': 'Invalid role'}, 400

        db.session.commit()
        return {'message': 'User registered successfully'}, 201

class Login(Resource):
    def post(self):
        data = login_parser.parse_args()

        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password_hash, data['password']):
            return {'message': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200
