from flask import Blueprint, jsonify
from flask_restx import Api, Resource, fields
from models.project import Project
from models.timelog import TimeLog
from models import db
from sqlalchemy import func

# Create a new Blueprint for reports
reports_bp = Blueprint('reports', __name__)

# Create the API instance for Swagger
api = Api(reports_bp)

# Define the report model for Swagger documentation
report_model = api.model('Report', {
    'project': fields.String(description='Name of the project'),
    'total_hours': fields.Float(description='Total hours worked on the project')
})

# Endpoint to get the total time worked on each project
@api.route('/total-time')
class TotalTimeReport(Resource):
    @api.doc('get_total_time')
    @api.marshal_list_with(report_model)
    def get(self):
        # Query to calculate total hours worked per project
        result = db.session.query(
            Project.name,
            func.sum(TimeLog.hours).label('total_hours')
        ).join(TimeLog, TimeLog.project_id == Project.id) \
         .group_by(Project.id).all()

        # Prepare response data
        total_time_report = []
        for row in result:
            total_time_report.append({
                'project': row.name,
                'total_hours': row.total_hours
            })

        return total_time_report


# Endpoint to get the time logs for a specific day
@api.route('/time-log/<date>')
class TimeLogReport(Resource):
    @api.doc('get_time_log')
    def get(self, date):
        # Query to get all time logs for a specific day
        logs = TimeLog.query.filter(TimeLog.date == date).all()

        # Prepare response data
        time_logs = []
        for log in logs:
            time_logs.append({
                'project': log.project.name,
                'hours': log.hours,
                'date': log.date
            })

        return jsonify(time_logs)


# Endpoint to get the weekly total time worked
@api.route('/weekly-time/<start_date>/<end_date>')
class WeeklyTimeReport(Resource):
    @api.doc('get_weekly_time')
    @api.marshal_list_with(report_model)
    def get(self, start_date, end_date):
        # Query to calculate the total hours worked within a specific date range
        result = db.session.query(
            Project.name,
            func.sum(TimeLog.hours).label('total_hours')
        ).join(TimeLog, TimeLog.project_id == Project.id) \
         .filter(TimeLog.date.between(start_date, end_date)) \
         .group_by(Project.id).all()

        # Prepare response data
        weekly_report = []
        for row in result:
            weekly_report.append({
                'project': row.name,
                'total_hours': row.total_hours
            })

        return weekly_report
