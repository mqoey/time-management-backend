from flask_restx import Namespace, Resource, fields
from models.project import Project
from models.timelog import TimeLog
from models import db
from sqlalchemy import func

# Create Namespace for reports
reports_ns = Namespace('reports', description='Report Generation')

# Define the report model for Swagger documentation
report_model = reports_ns.model('Report', {
    'project': fields.String(description='Name of the project'),
    'total_hours': fields.Float(description='Total hours worked on the project')
})

@reports_ns.route('/total-time')
class TotalTimeReport(Resource):
    @reports_ns.marshal_list_with(report_model)
    def get(self):
        result = db.session.query(
            Project.name,
            func.sum(TimeLog.hours).label('total_hours')
        ).join(TimeLog, TimeLog.project_id == Project.id) \
         .group_by(Project.id).all()

        return [{'project': row.name, 'total_hours': row.total_hours} for row in result]

@reports_ns.route('/time-log/<date>')
class TimeLogReport(Resource):
    def get(self, date):
        logs = TimeLog.query.filter(TimeLog.date == date).all()
        return [{'project': log.project.name, 'hours': log.hours, 'date': log.date} for log in logs]

@reports_ns.route('/weekly-time/<start_date>/<end_date>')
class WeeklyTimeReport(Resource):
    @reports_ns.marshal_list_with(report_model)
    def get(self, start_date, end_date):
        result = db.session.query(
            Project.name,
            func.sum(TimeLog.hours).label('total_hours')
        ).join(TimeLog, TimeLog.project_id == Project.id) \
         .filter(TimeLog.date.between(start_date, end_date)) \
         .group_by(Project.id).all()

        return [{'project': row.name, 'total_hours': row.total_hours} for row in result]
