from datetime import datetime
from app.extensions import db


class CareerReport(db.Model):
    __tablename__ = 'career_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Input snapshot (so history is self-contained even if user edits profile later)
    education_level = db.Column(db.String(50), nullable=False)
    marks_cgpa = db.Column(db.String(50), nullable=True)
    interests = db.Column(db.String(300), nullable=False)
    skills = db.Column(db.String(300), nullable=True)
    career_goal = db.Column(db.String(200), nullable=True)
    budget = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(80), nullable=True)
    preferred_industry = db.Column(db.String(120), nullable=True)

    # AI output (stored as JSON text)
    result_json = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('career_reports', lazy=True))

    def __repr__(self):
        return f'<CareerReport {self.id} user={self.user_id}>'