from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Appointment, Patient, Doctor
from db import db
from datetime import datetime

appointment_parser = reqparse.RequestParser()
appointment_parser.add_argument('doctor_id', type=int, required=True, help='Doctor ID is required')
appointment_parser.add_argument('date_time', required=True, help='Date and time is required in ISO format')

class AppointmentResource(Resource):
    @jwt_required()
    def get(self, appointment_id):
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return {'message': 'Appointment not found'}, 404
        return {
            'id': appointment.id,
            'patient_id': appointment.patient_id,
            'doctor_id': appointment.doctor_id,
            'date_time': appointment.date_time.isoformat(),
            'status': appointment.status
        }

    @jwt_required()
    def delete(self, appointment_id):
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return {'message': 'Appointment not found'}, 404
        db.session.delete(appointment)
        db.session.commit()
        return {'message': 'Appointment deleted'}

    @jwt_required()
    def put(self, appointment_id):
        data = appointment_parser.parse_args()
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return {'message': 'Appointment not found'}, 404
        try:
            appointment.date_time = datetime.fromisoformat(data['date_time'])
        except ValueError:
            return {'message': 'Invalid date_time format'}, 400
        appointment.doctor_id = data['doctor_id']
        db.session.commit()
        return {'message': 'Appointment updated'}

class AppointmentListResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        # For simplicity, return all appointments
        appointments = Appointment.query.all()
        return [{
            'id': a.id,
            'patient_id': a.patient_id,
            'doctor_id': a.doctor_id,
            'date_time': a.date_time.isoformat(),
            'status': a.status
        } for a in appointments]

    @jwt_required()
    def post(self):
        data = appointment_parser.parse_args()
        user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=user_id).first()
        if not patient:
            return {'message': 'Patient not found'}, 404
        try:
            date_time = datetime.fromisoformat(data['date_time'])
        except ValueError:
            return {'message': 'Invalid date_time format'}, 400
        appointment = Appointment(patient_id=patient.id, doctor_id=data['doctor_id'], date_time=date_time)
        db.session.add(appointment)
        db.session.commit()
        return {'message': 'Appointment created', 'id': appointment.id}, 201
