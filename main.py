from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import json
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

scenarios = {
  "1": {
    "id": "1",
    "emotion": "stressed-fearful",
    "title": "Stressed / Fearful",
    "ear": "Rotated to the sides (in an “airplane ears” pose), or angled backward",
    "eye": "Wide pupils",
    "tail": "Hold low to the body, tuck under body, or thrash and thump",
    "body": "Arched back (to look bigger), or crouch low to ground (to hide), grooming more than usual, hide under furniture or in corners",
    "paw": "",
    "sound": "",
    "cat-image": "stressed-cat.png",
    "env-image": "https://i5.walmartimages.com/asr/50d6a74d-aedf-4907-ad67-66dc36b251c2.51983cf5dbd54c51ae2be5cc6d40da83.jpeg?odnHeight=640&odnWidth=640&odnBg=FFFFFF",
    "image-ctrl": {
          "top": "32%",
          "left": "33%",
          "width": "30%",
          "height": "30%"
        },
    "positions": {
            "ear": {"top": "28%", "left": "40%"},
            "eye": {"top": "36%", "left": "44%"},
            "tail": {"top": "50%", "left": "14%"},
            "body": {"top": "25%", "left": "25%"},
            "paw": {"top": "", "left": ""},
            "sound": {"top": "", "left": ""},
        },
    "next": "2",
    "prev": "begin",
  },
  "2": {
    "id": "2",
    "emotion": "painful-sick",
    "title": "Painful / Sick",
    "ear": "Flattened, or rotated outward, less responsive to sounds",
    "eye": "Squinting or half-closed, uneven pupil sizes",
    "tail": "Hold stiffly, low to ground, or tucked under body",
    "body": "Stiff and hunched posture, legs tucked, reluctant to move",
    "paw": "",
    "sound": "",
    "cat-image": "sick-cat.png",
    "env-image": "https://www.maupets.com/cdn/shop/files/Bao_Modern_Solid_Wood_Cat_Tree_For_Large_Cats_main_1200x.jpg?v=1723223489",
    "image-ctrl": {
          "top": "40%",
          "left": "25%",
          "width": "30%",
          "height": "30%"
        },
    "positions": {
            "ear": {"top": "20%", "left": "33%"},
            "eye": {"top": "30%", "left": "35%"},
            "tail": {"top": "70%", "left": "25%"},
            "body": {"top": "40%", "left": "25%"},
            "paw": {"top": "", "left": ""},
            "sound": {"top": "", "left": ""},
        },
    "next": "3",
    "prev": "1",
  },
  "3": {
    "id": "3",
    "emotion": "curious-playful",
    "title": "Curious / Playful",
    "ear": "Up and forward facing",
    "eye": "Big and bright, might be slightly dilated",
    "tail": "Upright with curled tip (“question mark” shape), quickly flick their tail from side to side in hunting and watching whatever is captivating their attention",
    "body": "Slight arched back, Slow stalking movements, crouched with butt wiggles, short bursts of running",
    "paw": "Occasional paw bats at objects",
    "sound": "Soft chirps, trills",
    "cat-image": "playful-cat.png",
    "env-image": "https://www.thespruce.com/thmb/R-M6g-5koC4oSLQ1CeIQ-bsBQVA=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/cat-climbing-shelf-wall-8b636cf12c4347d5a1b71266f42586f8.jpeg",
    "image-ctrl": {
          "top": "42%",
          "left": "52%",
          "width": "25%",
          "height": "25%"
        },
    "positions": {
            "ear": {"top": "26%", "left": "10%"},
            "eye": {"top": "35%", "left": "10%"},
            "tail": {"top": "20%", "left": "42%"},
            "body": {"top": "40%", "left": "30%"},
            "paw": {"top": "76%", "left": "18%"},
            "sound": {"top": "43%", "left": "12%"},
        },
    "next": "4",
    "prev": "2",
  },
  "4": {
    "id": "4",
    "emotion": "happy-relaxed",
    "title": "Happy / Relaxed",
    "ear": "Upright and forward facing",
    "eye": "Round or partially closed, pupils narrow like slits, blinks slowly at you ('cat kisses' of trust)",
    "tail": "Pointed straight up, may sway gently like a metronome",
    "body": "Rolling belly-up, stretching out fully",
    "paw": "Kneading ('making biscuits' with paws)",
    "sound": "Gentle purring, short and melodic meows",
    "cat-image": "happy-cat.png",
    "env-image": "https://www.thespruce.com/thmb/nMb1vvPeJdpvNsZVAiswHhry1iM=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/cat-playroom-1448b64778434eaf88b3dcf2695bde2e.jpeg",
    "image-ctrl": {
          "top": "65%",
          "left": "35%",
          "width": "30%",
          "height": "30%"
        },
    "positions": {
            "ear": {"top": "20%", "left": "24%"},
            "eye": {"top": "28%", "left": "24%"},
            "tail": {"top": "30%", "left": "35%"},
            "body": {"top": "50%", "left": "33%"},
            "paw": {"top": "76%", "left": "30%"},
            "sound": {"top": "33%", "left": "26%"},
        },
    "next": "end",
    "prev": "3"
  },
}
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
    return render_template('scenario.html')

@app.route('/tutorial/<category>')
def tutorial_category(category):
    if category == 'end':
        return render_template('quiz.html')
    if category == 'begin':
        return render_template('index.html')
    
    global scenarios
    scenario = [scenario for scenario in scenarios.values() if scenario['emotion'] == category][0]
    if scenario['next'] != "end":
        next_category = scenarios[scenario['next']]['emotion']
    else:
        next_category = "end"
    if scenario['prev'] != "begin":
        prev_category = scenarios[scenario['prev']]['emotion']
    else:
        prev_category = "begin"

    if category in [scenario['emotion'] for scenario in scenarios.values()]:
        return render_template('scenario.html', 
                              category = category, 
                              scenario = scenario,
                              next_category = next_category,
                              prev_category = prev_category)
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
