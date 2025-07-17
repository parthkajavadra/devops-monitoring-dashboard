from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from models import db, Pipeline, DeploymentMetric
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = SQLAlchemy(app)
migrate = Migrate(app, db) 
@app.route('/')
def home():
    return jsonify({"message": "DevOps Monitoring Backend Running"}), 200

# API endpoints will be here...

if __name__ == "__main__":
    app.run(debug=True)
# Get all pipelines
@app.route('/api/pipelines', methods=['GET'])
def get_pipelines():
    pipelines = Pipeline.query.all()
    result = [pipeline_to_dict(p) for p in pipelines]
    return jsonify(result), 200

# Helper to convert Pipeline model to dict
def pipeline_to_dict(pipeline):
    return {
        "id": pipeline.id,
        "name": pipeline.name,
        "source": pipeline.source,
        "status": pipeline.status,
        "duration": pipeline.duration,
        "started_at": pipeline.started_at.isoformat() if pipeline.started_at else None,
        "completed_at": pipeline.completed_at.isoformat() if pipeline.completed_at else None,
        "commit_hash": pipeline.commit_hash,
        "branch": pipeline.branch,
        "author": pipeline.author,
        "test_coverage": pipeline.test_coverage,
        "code_quality_score": pipeline.code_quality_score,
        "security_vulnerabilities": pipeline.security_vulnerabilities,
    }

# Create new pipeline
@app.route('/api/pipelines', methods=['POST'])
def create_pipeline():
    data = request.json
    if not data or not 'name' in data:
        abort(400, "Pipeline name is required")
    pipeline = Pipeline(
        name=data.get('name'),
        source=data.get('source'),
        status=data.get('status'),
        duration=data.get('duration'),
        started_at=data.get('started_at'),
        completed_at=data.get('completed_at'),
        commit_hash=data.get('commit_hash'),
        branch=data.get('branch'),
        author=data.get('author'),
        test_coverage=data.get('test_coverage'),
        code_quality_score=data.get('code_quality_score'),
        security_vulnerabilities=data.get('security_vulnerabilities'),
    )
    db.session.add(pipeline)
    db.session.commit()
    return jsonify(pipeline_to_dict(pipeline)), 201

# Get pipeline by id
@app.route('/api/pipelines/<string:pipeline_id>', methods=['GET'])
def get_pipeline(pipeline_id):
    pipeline = Pipeline.query.get_or_404(pipeline_id)
    return jsonify(pipeline_to_dict(pipeline)), 200

# Update pipeline
@app.route('/api/pipelines/<string:pipeline_id>', methods=['PUT'])
def update_pipeline(pipeline_id):
    pipeline = Pipeline.query.get_or_404(pipeline_id)
    data = request.json
    for field in [
        "name", "source", "status", "duration", "started_at", "completed_at",
        "commit_hash", "branch", "author", "test_coverage", "code_quality_score",
        "security_vulnerabilities"
    ]:
        if field in data:
            setattr(pipeline, field, data[field])
    db.session.commit()
    return jsonify(pipeline_to_dict(pipeline)), 200

# Delete pipeline
@app.route('/api/pipelines/<string:pipeline_id>', methods=['DELETE'])
def delete_pipeline(pipeline_id):
    pipeline = Pipeline.query.get_or_404(pipeline_id)
    db.session.delete(pipeline)
    db.session.commit()
    return jsonify({"message": "Pipeline deleted"}), 200
