from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create Flask app instance
app = Flask(__name__)

# Load configurations first
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Ensure you set this in your .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Ensure this is correct
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and login manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "admin_login"  # Default login view for the app

# Define models
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Voter(db.Model):
    voter_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    voter_unique_id = db.Column(db.String(50), unique=True, nullable=False)

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# Define routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.password == password:  # Replace with hashed password check
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    voters = Voter.query.all()
    return render_template('admin_dashboard.html', voters=voters)

@app.route('/voter/register', methods=['GET', 'POST'])
def register_voter():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        voter_unique_id = request.form['voter_unique_id']

        new_voter = Voter(name=name, email=email, password=password, voter_unique_id=voter_unique_id)
        db.session.add(new_voter)
        db.session.commit()
        flash('Voter registered successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('register_voter.html')

@app.route('/voter/login', methods=['GET', 'POST'])
def voter_login():
    if request.method == 'POST':
        voter_unique_id = request.form['voter_unique_id']
        password = request.form['password']
        voter = Voter.query.filter_by(voter_unique_id=voter_unique_id).first()

        if voter and voter.password == password:  # Replace with hashed password check
            flash('Logged in successfully!', 'success')
            return redirect(url_for('vote'))
        else:
            flash('Invalid Voter ID or Password', 'danger')
    
    return render_template('voter_login.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    # Add functionality to list candidates and record vote
    return render_template('vote.html')

@app.route('/voter/dashboard')
@login_required
def voter_dashboard():
    return render_template('voter_dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)



