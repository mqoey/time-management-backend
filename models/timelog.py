from models import db

class TimeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    hours = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(10), nullable=False)

    # Method to return model as a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'hours': self.hours,
            'date': self.date
        }