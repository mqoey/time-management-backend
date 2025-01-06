from app import create_app, db

# Create the app instance using the create_app function
app = create_app()

# Use the application context
with app.app_context():
    # Create all tables defined in the models
    db.create_all()

print("Database initialized successfully.")