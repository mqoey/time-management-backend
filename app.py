from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from config import Config
from models import db
from api.projects import projects_bp
from api.timelogs import timelogs_bp
from api.reports import reports_bp

# Create app function to avoid circular imports
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Set up Swagger (API Documentation)
    api = Api(app, version='1.0', title='Time Management API', description='An API to manage time logs and reports')

    # Register Blueprints
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(timelogs_bp, url_prefix='/api/timelogs')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')

    return app

# Only run the app when this file is executed directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
