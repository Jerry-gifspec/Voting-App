from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

# Admin Table
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

# Voter Table
class Voter(db.Model):
    voter_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    voter_unique_id = db.Column(db.String(50), nullable=False, unique=True)

# Positions Table
class Position(db.Model):
    position_id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String(100), nullable=False)

# Candidates Table
class Candidate(db.Model):
    candidate_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.position_id'), nullable=False)
    position = db.relationship('Position', backref=db.backref('candidates', lazy=True))

# Votes Table
class Vote(db.Model):
    vote_id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('voter.voter_id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.candidate_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

