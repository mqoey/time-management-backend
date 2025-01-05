from flask import Blueprint, request, jsonify
from models import db
from models.project import Project

# Create a Blueprint for projects
projects_bp = Blueprint('projects', __name__)


# Route to get all projects
@projects_bp.route('/', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects]), 200


# Route to get a single project by ID
@projects_bp.route('/<int:id>', methods=['GET'])
def get_project(id):
    project = Project.query.get_or_404(id)
    return jsonify(project.to_dict()), 200


# Route to create a new project
@projects_bp.route('/', methods=['POST'])
def create_project():
    data = request.get_json()
    name = data.get('name')
    color = data.get('color')

    if not name or not color:
        return jsonify({'error': 'Missing required fields'}), 400

    new_project = Project(name=name, color=color)
    db.session.add(new_project)
    db.session.commit()

    return jsonify(new_project.to_dict()), 201


# Route to update a project
@projects_bp.route('/<int:id>', methods=['PUT'])
def update_project(id):
    data = request.get_json()
    project = Project.query.get_or_404(id)

    name = data.get('name', project.name)
    color = data.get('color', project.color)

    project.name = name
    project.color = color
    db.session.commit()

    return jsonify(project.to_dict()), 200


# Route to delete a project
@projects_bp.route('/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()

    return jsonify({'message': 'Project deleted successfully'}), 200
