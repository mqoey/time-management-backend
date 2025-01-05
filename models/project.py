from models import db

class Project(db.Model):
    class Project(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), unique=True, nullable=False)
        color = db.Column(db.String(7), nullable=False)

        # Relationship with TimeLog model
        timelogs = db.relationship('TimeLog', backref='project', lazy=True)

        # Method to return model as a dictionary
        def to_dict(self):
            return {
                'id': self.id,
                'name': self.name,
                'color': self.color
            }