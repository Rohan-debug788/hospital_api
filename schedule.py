from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Schedule, Doctor
from db import db
from datetime import time

schedule_parser = reqparse.RequestParser()
schedule_parser.add_argument('day_of_week', required=True, help='Day of week is required')
schedule_parser.add_argument('start_time', required=True, help='Start time is required in HH:MM format')
schedule_parser.add_argument('end_time', required=True, help='End time is required in HH:MM format')

class ScheduleResource(Resource):
    @jwt_required()
    def get(self, schedule_id):
        schedule = Schedule.query.get(schedule_id)
        if not schedule:
            return {'message': 'Schedule not found'}, 404
        return {
            'id': schedule.id,
            'doctor_id': schedule.doctor_id,
            'day_of_week': schedule.day_of_week,
            'start_time': schedule.start_time.isoformat(),
            'end_time': schedule.end_time.isoformat()
        }

    @jwt_required()
    def delete(self, schedule_id):
        schedule = Schedule.query.get(schedule_id)
        if not schedule:
            return {'message': 'Schedule not found'}, 404
        db.session.delete(schedule)
        db.session.commit()
        return {'message': 'Schedule deleted'}

    @jwt_required()
    def put(self, schedule_id):
        data = schedule_parser.parse_args()
        schedule = Schedule.query.get(schedule_id)
        if not schedule:
            return {'message': 'Schedule not found'}, 404
        try:
            schedule.start_time = time.fromisoformat(data['start_time'])
            schedule.end_time = time.fromisoformat(data['end_time'])
        except ValueError:
            return {'message': 'Invalid time format'}, 400
        schedule.day_of_week = data['day_of_week']
        db.session.commit()
        return {'message': 'Schedule updated'}

class ScheduleListResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        if not doctor:
            return {'message': 'Doctor not found'}, 404
        schedules = Schedule.query.filter_by(doctor_id=doctor.id).all()
        return [{
            'id': s.id,
            'doctor_id': s.doctor_id,
            'day_of_week': s.day_of_week,
            'start_time': s.start_time.isoformat(),
            'end_time': s.end_time.isoformat()
        } for s in schedules]

    @jwt_required()
    def post(self):
        data = schedule_parser.parse_args()
        user_id = get_jwt_identity()
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        if not doctor:
            return {'message': 'Doctor not found'}, 404
        try:
            start_time = time.fromisoformat(data['start_time'])
            end_time = time.fromisoformat(data['end_time'])
        except ValueError:
            return {'message': 'Invalid time format'}, 400
        schedule = Schedule(doctor_id=doctor.id, day_of_week=data['day_of_week'], start_time=start_time, end_time=end_time)
        db.session.add(schedule)
        db.session.commit()
        return {'message': 'Schedule created', 'id': schedule.id}, 201
