from flask import Blueprint, request, jsonify
from models import db
from models.timelog import TimeLog
from models.project import Project

# Create a Blueprint for timelogs
timelogs_bp = Blueprint('timelogs', __name__)


# Route to get all timelogs
@timelogs_bp.route('/', methods=['GET'])
def get_timelogs():
    timelogs = TimeLog.query.all()
    return jsonify([timelog.to_dict() for timelog in timelogs]), 200


# Route to get a single timelog by ID
@timelogs_bp.route('/<int:id>', methods=['GET'])
def get_timelog(id):
    timelog = TimeLog.query.get_or_404(id)
    return jsonify(timelog.to_dict()), 200


# Route to create a new timelog
@timelogs_bp.route('/', methods=['POST'])
def create_timelog():
    data = request.get_json()
    project_id = data.get('project_id')
    hours = data.get('hours')
    date = data.get('date')

    if not project_id or not hours or not date:
        return jsonify({'error': 'Missing required fields'}), 400

    project = Project.query.get_or_404(project_id)
    new_timelog = TimeLog(project_id=project_id, hours=hours, date=date)

    db.session.add(new_timelog)
    db.session.commit()

    return jsonify(new_timelog.to_dict()), 201


# Route to update a timelog
@timelogs_bp.route('/<int:id>', methods=['PUT'])
def update_timelog(id):
    data = request.get_json()
    timelog = TimeLog.query.get_or_404(id)

    project_id = data.get('project_id', timelog.project_id)
    hours = data.get('hours', timelog.hours)
    date = data.get('date', timelog.date)

    timelog.project_id = project_id
    timelog.hours = hours
    timelog.date = date

    db.session.commit()

    return jsonify(timelog.to_dict()), 200


# Route to delete a timelog
@timelogs_bp.route('/<int:id>', methods=['DELETE'])
def delete_timelog(id):
    timelog = TimeLog.query.get_or_404(id)
    db.session.delete(timelog)
    db.session.commit()

    return jsonify({'message': 'Timelog deleted successfully'}), 200
