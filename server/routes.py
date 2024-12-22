from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from .server import app
from .. import db
from .models import Admin, Voter, Position, Candidate, Vote

# Admin login route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.password == password:  # Use bcrypt for secure passwords
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('admin_login.html')

# Admin dashboard route
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Display registered voters and positions
    voters = Voter.query.all()
    positions = Position.query.all()
    return render_template('admin_dashboard.html', voters=voters, positions=positions)

# Voter registration route (Admin only)
@app.route('/admin/register_voter', methods=['GET', 'POST'])
@login_required
def register_voter():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        voter_unique_id = request.form['voter_unique_id']

        # Check if the Voter ID is already registered
        if Voter.query.filter_by(voter_unique_id=voter_unique_id).first():
            flash('Voter ID already exists', 'danger')
            return redirect(url_for('register_voter'))

        # Add new voter to the database
        new_voter = Voter(name=name, email=email, password=password, voter_unique_id=voter_unique_id)
        db.session.add(new_voter)
        db.session.commit()
        flash('Voter registered successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('register_voter.html')

# Voter login route
@app.route('/voter/login', methods=['GET', 'POST'])
def voter_login():
    if request.method == 'POST':
        voter_id = request.form['voter_unique_id']
        password = request.form['password']
        voter = Voter.query.filter_by(voter_unique_id=voter_id).first()
        if voter and voter.password == password:  # Replace with hashed password check
            login_user(voter)
            return redirect(url_for('voter_dashboard'))
        flash('Invalid Voter ID or Password', 'danger')
    return render_template('voter_login.html')

# Voter dashboard route (after login)
@app.route('/voter/dashboard')
@login_required
def voter_dashboard():
    positions = Position.query.all()  # Display positions to vote for
    return render_template('voter_dashboard.html', positions=positions)

# Voting route (submit vote)
@app.route('/vote/<int:candidate_id>', methods=['POST'])
@login_required
def vote(candidate_id):
    candidate = Candidate.query.get(candidate_id)
    if candidate:
        vote = Vote(voter_id=current_user.voter_id, candidate_id=candidate_id)
        db.session.add(vote)
        db.session.commit()
        flash('Your vote has been successfully cast!', 'success')
    return redirect(url_for('voter_dashboard'))
# Example route for voter list
@app.route("/voter/list")
def voter_list():
    voters = [
        {"name": "John Doe", "id": 1, "email": "john@example.com"},
        {"name": "Jane Smith", "id": 2, "email": "jane@example.com"},
    ]
    return render_template("voter_list.html", voters=voters)

# Vote tally route (Admin view to count votes)
@app.route('/admin/tally_votes')
@login_required
def tally_votes():
    # Fetch total votes for each candidate
    results = db.session.query(Candidate, db.func.count(Vote.candidate_id).label('vote_count')) \
        .join(Vote, Vote.candidate_id == Candidate.id) \
        .group_by(Candidate.id).all()
    
    return render_template('vote_tally.html', results=results)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



# from flask import render_template, request, redirect, url_for, flash
# from flask_login import login_user, login_required, current_user, logout_user
# from .server import app
# from .. import db
# from .models import Admin, Voter, Position, Candidate, Vote

# # Admin login route
# @app.route('/admin/login', methods=['GET', 'POST'])
# def admin_login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         admin = Admin.query.filter_by(username=username).first()
#         if admin and admin.password == password:  # Use bcrypt for secure passwords
#             login_user(admin)
#             return redirect(url_for('admin_dashboard'))
#         flash('Invalid credentials', 'danger')
#     return render_template('admin_login.html')

# # Admin dashboard route
# @app.route('/admin/dashboard')
# @login_required
# def admin_dashboard():
#     return render_template('admin_dashboard.html')

# # Voter login route
# @app.route('/voter/login', methods=['GET', 'POST'])
# def voter_login():
#     if request.method == 'POST':
#         voter_id = request.form['voter_unique_id']
#         voter = Voter.query.filter_by(voter_unique_id=voter_id).first()
#         if voter:
#             login_user(voter)
#             return redirect(url_for('voter_dashboard'))
#         flash('Invalid Voter ID', 'danger')
#     return render_template('voter_login.html')

# # Voter dashboard route
# @app.route('/voter/dashboard')
# @login_required
# def voter_dashboard():
#     positions = Position.query.all()  # Display positions to vote for
#     return render_template('voter_dashboard.html', positions=positions)

# # Vote route
# @app.route('/vote/<int:candidate_id>', methods=['POST'])
# @login_required
# def vote(candidate_id):
#     candidate = Candidate.query.get(candidate_id)
#     if candidate:
#         vote = Vote(voter_id=current_user.voter_id, candidate_id=candidate_id)
#         db.session.add(vote)
#         db.session.commit()
#         flash('Your vote has been successfully cast!', 'success')
#     return redirect(url_for('voter_dashboard'))
