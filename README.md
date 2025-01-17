# Time Management API

A RESTful API built with Flask to manage time logs, projects, and generate reports for a time management application. This API allows users to create, read, update, and delete projects and time logs, as well as view reports.

## Features

- Manage Projects: Create, update, delete, and retrieve projects.
- Manage Time Logs: Create, update, and retrieve time logs.
- Generate Reports: Generate reports based on projects and time logs.
- API Documentation: Swagger-based API documentation.

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-RESTX
- Gunicorn (for production)
- PostgreSQL (for production) or SQLite (for local development)

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/mqoeyyy/time-management-api.git
cd time-management-api
```

### 2. Create a Virtual Environment

For local development, create a virtual environment and activate it:

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Configure the Database

- In the `config.py`, configure the database URL for local development or production.
- For local development, you can use SQLite:
  ```python
  SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_db.sqlite'
  ```
- For production (e.g., PostgreSQL on Render), use:
  ```python
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
  ```

### 5. Initialize the Database

Run the following commands to initialize the database and apply migrations:

```bash
# Initialize the migration folder
flask db init

# Generate the migration file
flask db migrate -m "Initial migration"

# Apply the migration to the database
flask db upgrade
```

### 6. Run the Application Locally

To start the Flask app locally:

```bash
flask run
```

By default, it will run on `http://127.0.0.1:5000/`.

### 7. Access the API Documentation

Once the app is running, you can access the Swagger-based API documentation at:

```
http://127.0.0.1:5000/swagger
```

## Deployment

### 1. Deploy to Render

If deploying to Render, make sure to:

1. Set the environment variable `DATABASE_URL` with your PostgreSQL connection string (from Render or other providers).
2. Set up automatic migrations as part of the deployment process (in your `render.yaml` or through manual deployment).

### 2. Deployment Commands

In your `render.yaml` file (for Render deployments):

```yaml
services:
  - type: web
    name: time-management-api
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn 'app:create_app()'"
    plan: free
    envVars:
      - key: DATABASE_URL
        value: "<your_database_url>"
    autoDeploy: true
    deploy:
      postDeploy:
        - "flask db upgrade"
```

This will ensure that migrations are applied automatically after each deployment.

## API Endpoints

### Projects

- **GET `/api/projects/`** - Get all projects
- **POST `/api/projects/create`** - Create a new project
- **GET `/api/projects/<id>`** - Get a project by ID
- **PUT `/api/projects/<id>`** - Update a project
- **DELETE `/api/projects/<id>`** - Delete a project

### Time Logs

- **GET `/api/timelogs/`** - Get all time logs
- **POST `/api/timelogs/create`** - Create a new time log
- **GET `/api/timelogs/<id>`** - Get a time log by ID
- **PUT `/api/timelogs/<id>`** - Update a time log
- **DELETE `/api/timelogs/<id>`** - Delete a time log

### Reports

- **GET `/api/reports/`** - Generate reports based on projects and time logs

## Testing

To run the tests, first, install testing dependencies:

```bash
pip install -r requirements-dev.txt
```

Then run:

```bash
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [Flask-RESTX](https://flask-restx.readthedocs.io/)
