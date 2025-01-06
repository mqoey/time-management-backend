from flask_restx import Namespace, Resource
from flask import request
from models.timelog import TimeLog
from models.project import Project
from models import db

# Create Namespace for timelogs
timelogs_ns = Namespace('timelogs', description='Time Log Management')

@timelogs_ns.route('/')
class TimeLogList(Resource):
    def get(self):
        timelogs = TimeLog.query.all()
        return [timelog.to_dict() for timelog in timelogs], 200

    def post(self):
        data = request.get_json()
        project_id = data.get('project_id')
        hours = data.get('hours')
        date = data.get('date')

        if not project_id or not hours or not date:
            return {'error': 'Missing required fields'}, 400

        Project.query.get_or_404(project_id)
        new_timelog = TimeLog(project_id=project_id, hours=hours, date=date)
        db.session.add(new_timelog)
        db.session.commit()

        return new_timelog.to_dict(), 201

@timelogs_ns.route('/<int:id>')
class TimeLogDetail(Resource):
    def get(self, id):
        timelog = TimeLog.query.get_or_404(id)
        return timelog.to_dict(), 200

    def put(self, id):
        data = request.get_json()
        timelog = TimeLog.query.get_or_404(id)

        timelog.project_id = data.get('project_id', timelog.project_id)
        timelog.hours = data.get('hours', timelog.hours)
        timelog.date = data.get('date', timelog.date)

        db.session.commit()
        return timelog.to_dict(), 200

    def delete(self, id):
        timelog = TimeLog.query.get_or_404(id)
        db.session.delete(timelog)
        db.session.commit()
        return {'message': 'Timelog deleted successfully'}, 200
