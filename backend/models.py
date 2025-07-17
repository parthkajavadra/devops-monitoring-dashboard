from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class Pipeline(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(50))  # jenkins, gitlab, github
    status = db.Column(db.String(20))  # success, failed, running
    duration = db.Column(db.Integer)   # seconds
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    commit_hash = db.Column(db.String(40))
    branch = db.Column(db.String(100))
    author = db.Column(db.String(100))
    test_coverage = db.Column(db.Float)
    code_quality_score = db.Column(db.Float)
    security_vulnerabilities = db.Column(db.Integer)

class DeploymentMetric(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    environment = db.Column(db.String(50))  # dev, staging, prod
    service_name = db.Column(db.String(100))
    version = db.Column(db.String(50))
    deployed_at = db.Column(db.DateTime, default=datetime.utcnow)
    deployment_duration = db.Column(db.Integer)
    rollback_count = db.Column(db.Integer, default=0)
    success_rate = db.Column(db.Float)
