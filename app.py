from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from config import Config
from models import db
from api.projects import projects_ns
from api.timelogs import timelogs_ns
from api.reports import reports_ns

# Create app function to avoid circular imports
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)

    # Initialize Flask-Migrate
    Migrate(app, db)

    # Initialize Flask-RESTX API
    api = Api(app, version='1.0', title='Time Management API', description='An API to manage time logs and reports')

    # Add namespaces
    api.add_namespace(projects_ns, path='/api/projects')
    api.add_namespace(timelogs_ns, path='/api/timelogs')
    api.add_namespace(reports_ns, path='/api/reports')

    return app

# Only run the app when this file is executed directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
