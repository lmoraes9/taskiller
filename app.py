import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import datetime
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Load configurations from environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migration tool
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- Database Models ---

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=3)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.description}>'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Event {self.description}>'

# Add other models for Routine and Finance later

# --- Routes ---

@app.route('/')
def index():
    # Redirect index to the main dashboard
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # This is our new main page
    all_tasks = Task.query.order_by(Task.created_at.desc()).all()
    all_events = Event.query.order_by(Event.date.asc()).all()
    return render_template('dashboard.html', tasks=all_tasks, events=all_events)

@app.route('/tasks-events') # Keeping this route for now in case of old bookmarks
def tasks_events_redirect():
    return redirect(url_for('dashboard'))

@app.route('/add-task', methods=['POST'])
def add_task():
    description = request.form.get('description')
    priority = int(request.form.get('priority', 3)) # Default to 3 if not provided
    
    new_task = Task(description=description, priority=priority)
    db.session.add(new_task)
    db.session.commit()
    
    return redirect(url_for('dashboard')) # Redirect back to the dashboard

@app.route('/add-event', methods=['POST'])
def add_event():
    description = request.form.get('description')
    date_str = request.form.get('date')
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    
    new_event = Event(description=description, date=date)
    db.session.add(new_event)
    db.session.commit()

    return redirect(url_for('dashboard')) # Redirect back to the dashboard

# --- Placeholder Routes for other pages ---
@app.route('/routines')
def routines_page():
    return render_template('routines.html')

@app.route('/finances')
def finances_page():
    return render_template('finances.html')


if __name__ == '__main__':
    app.run(debug=True)