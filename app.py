from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import json
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database setup
def get_db_connection():
    conn = sqlite3.connect('cat_tutorial.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS quiz_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        score INTEGER,
        total INTEGER,
        answers TEXT,
        timestamp DATETIME
    )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.route('/tutorial/<category>')
def tutorial_category(category):
    categories = {
        'stressed-fearful': 'Stressed / Fearful',
        'painful-sick': 'Painful / Sick',
        'curious-playful': 'Curious / Playful',
        'happy-relaxed': 'Happy / Relaxed'
    }
    
    if category in categories:
        return render_template('scenario.html', 
                              category=category, 
                              title=categories[category])
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    # Initialize quiz session
    session['quiz_answers'] = {}
    session['quiz_started'] = True
    return render_template('quiz.html')

@app.route('/quiz/<part>')
def quiz_part(part):
    if not session.get('quiz_started', False):
        return redirect(url_for('quiz'))
    
    return render_template('quiz_part.html', part=part)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if not session.get('quiz_started', False):
        return jsonify({'status': 'error', 'message': 'Quiz not started'})
    
    data = request.get_json()
    question_id = data.get('question_id')
    answer = data.get('answer')
    is_correct = data.get('is_correct', False)
    
    if not question_id or answer is None:
        return jsonify({'status': 'error', 'message': 'Invalid data'})
    
    # Store answer in session
    if 'quiz_answers' not in session:
        session['quiz_answers'] = {}
    
    session['quiz_answers'][question_id] = {
        'answer': answer,
        'is_correct': is_correct
    }
    session.modified = True
    
    return jsonify({'status': 'success'})

@app.route('/quiz/result')
def quiz_result():
    if not session.get('quiz_started', False) or not session.get('quiz_answers'):
        return redirect(url_for('quiz'))
    
    # Calculate score
    answers = session.get('quiz_answers', {})
    correct_count = sum(1 for answer in answers.values() if answer.get('is_correct', False))
    total_count = len(answers)
    
    # Generate a random user ID if not exists
    if 'user_id' not in session:
        session['user_id'] = os.urandom(8).hex()
    
    # Save to database
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO quiz_results (user_id, score, total, answers, timestamp) VALUES (?, ?, ?, ?, ?)',
        (session['user_id'], correct_count, total_count, json.dumps(answers), datetime.now())
    )
    conn.commit()
    conn.close()
    
    # Clear quiz session
    session['quiz_started'] = False
    
    return render_template('quiz_result.html', 
                          score=correct_count, 
                          total=total_count,
                          percentage=(correct_count / total_count * 100) if total_count > 0 else 0)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
