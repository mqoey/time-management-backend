from flask_restx import Namespace, Resource, fields
from flask import request
from models.project import Project
from models import db

# Create Namespace for projects
projects_ns = Namespace('projects', description='Project Management')

# Define a request model for Swagger
project_model = projects_ns.model('Project', {
    'name': fields.String(required=True, description='The name of the project'),
    'color': fields.String(required=True, description='The color of the project'),
})

@projects_ns.route('/')
class ProjectList(Resource):
    @projects_ns.doc(description="Get a list of all projects")
    def get(self):
        projects = Project.query.all()
        return [project.to_dict() for project in projects], 200

    @projects_ns.expect(project_model)  # Attach the request model for POST
    @projects_ns.doc(description="Create a new project")
    def post(self):
        data = request.get_json()

        name = data.get('name')
        color = data.get('color')

        if not name or not color:
            return {'error': 'Missing required fields'}, 400

        new_project = Project(name=name, color=color)
        db.session.add(new_project)
        db.session.commit()

        return new_project.to_dict(), 201

@projects_ns.route('/<int:id>')
class ProjectDetail(Resource):
    @projects_ns.doc(description="Get details of a specific project by ID")
    def get(self, id):
        project = Project.query.get_or_404(id)
        return project.to_dict(), 200

    @projects_ns.expect(project_model)  # Attach the request model for PUT
    @projects_ns.doc(description="Update an existing project by ID")
    def put(self, id):
        data = request.get_json()

        project = Project.query.get_or_404(id)
        project.name = data.get('name', project.name)
        project.color = data.get('color', project.color)
        db.session.commit()

        return project.to_dict(), 200

    @projects_ns.doc(description="Delete a project by ID")
    def delete(self, id):
        project = Project.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()

        return {'message': 'Project deleted successfully'}, 200
