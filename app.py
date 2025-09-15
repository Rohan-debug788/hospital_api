from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from auth import Register, Login
from appointment import AppointmentResource, AppointmentListResource
from schedule import ScheduleResource, ScheduleListResource

#function for creating the app
def create_app():
    app = Flask(__name__)
    
    #--->configurations<---
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret" # will change this later during production

    db.init_app(app)
    with app.app_context():
        db.create_all()
    api = Api(app)
    jwt = JWTManager(app)

    # Register resources
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(AppointmentListResource, '/appointments')
    api.add_resource(AppointmentResource, '/appointments/<int:appointment_id>')
    api.add_resource(ScheduleListResource, '/schedules')
    api.add_resource(ScheduleResource, '/schedules/<int:schedule_id>')

    @app.route("/")
    def home():
        return {"message": "Hospital API running"}

    return app




if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
