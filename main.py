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
    "ear": "Rotated to the sides (in an \"airplane ears\" pose), or angled backward",
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
    "tail": "Upright with curled tip (\"question mark\" shape), quickly flick their tail from side to side in hunting and watching whatever is captivating their attention",
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

# Quiz Data Structure
quiz_data = {
    "title": "Cat Body Language Quiz",
    "steps": [
        {
            "id": "drag_drop",
            "type": "drag_drop",
            "title": "Drag and Drop",
            "instruction": "Drag each cat image to the correct category based on their body language",
            "categories": {
                "positive": {
                    "title": "Positive/Happy Body Language",
                    "style": "bg-success"
                },
                "negative": {
                    "title": "Negative/Stressed Body Language",
                    "style": "bg-danger"
                }
            },
            "drag_items": [
                {
                    "id": "happy-cat",
                    "image": "happy-cat.png",
                    "caption": "Cat with upright tail",
                    "category": "positive"
                },
                {
                    "id": "stressed-cat",
                    "image": "stressed-cat.png",
                    "caption": "Cat with flattened ears",
                    "category": "negative"
                },
                {
                    "id": "playful-cat",
                    "image": "playful-cat.png",
                    "caption": "Cat kneading with paws",
                    "category": "positive"
                },
                {
                    "id": "sick-cat",
                    "image": "sick-cat.png",
                    "caption": "Cat with tail tucked",
                    "category": "negative"
                }
            ],
            "feedback": {
                "success": "Great job! You correctly categorized all the cats based on their body language!",
                "error": "You got {score}/{total} cats correct. Green borders indicate correct placements, red borders indicate incorrect placements."
            }
        },
        {
            "id": "q1",
            "type": "multiple_choice",
            "question": "Which tail position indicates a happy, confident cat?",
            "options": [
                {"id": "a", "text": "Tucked between legs", "correct": False},
                {"id": "b", "text": "Puffed up and bristled", "correct": False},
                {"id": "c", "text": "Upright with a slight curl at the tip", "correct": True},
                {"id": "d", "text": "Thrashing from side to side", "correct": False}
            ],
            "feedback": {
                "correct": "Correct! A tail held high with a slight curl at the tip is a sign of a happy, confident cat.",
                "incorrect": "Not quite. A happy, confident cat holds its tail upright with a slight curl at the tip."
            }
        },
        {
            "id": "q2",
            "type": "multiple_choice",
            "question": "When a cat's ears are flattened against their head, it usually means:",
            "options": [
                {"id": "a", "text": "They're happy", "correct": False},
                {"id": "b", "text": "They're afraid or angry", "correct": True},
                {"id": "c", "text": "They're curious", "correct": False},
                {"id": "d", "text": "They're sleepy", "correct": False}
            ],
            "feedback": {
                "correct": "Correct! Flattened ears indicate fear or anger in cats.",
                "incorrect": "That's not right. When a cat flattens its ears against its head, it's usually afraid or angry."
            }
        },
        {
            "id": "q3",
            "type": "multiple_choice",
            "question": "Slow blinking from a cat is often a sign of:",
            "options": [
                {"id": "a", "text": "Boredom", "correct": False},
                {"id": "b", "text": "Hunger", "correct": False},
                {"id": "c", "text": "Trust and affection", "correct": True},
                {"id": "d", "text": "Irritation", "correct": False}
            ],
            "feedback": {
                "correct": "Correct! Slow blinking is a sign of trust and affection, sometimes called 'cat kisses'.",
                "incorrect": "Not quite. Slow blinking from a cat is a sign of trust and affection, often called 'cat kisses'."
            }
        },
        {
            "id": "q4",
            "type": "multiple_choice",
            "question": "A cat crouched low to the ground with dilated pupils is likely:",
            "options": [
                {"id": "a", "text": "Ready to pounce in play", "correct": False},
                {"id": "b", "text": "Feeling stressed or fearful", "correct": True},
                {"id": "c", "text": "Looking for attention", "correct": False},
                {"id": "d", "text": "Feeling sick", "correct": False}
            ],
            "feedback": {
                "correct": "Correct! A crouched position with dilated pupils typically indicates stress or fear.",
                "incorrect": "That's not right. A cat crouched low with dilated pupils is usually feeling stressed or fearful."
            }
        },
        {
            "id": "q5",
            "type": "multiple_choice",
            "question": "Kneading behavior (pushing paws against a soft surface) in cats originates from:",
            "options": [
                {"id": "a", "text": "Marking territory", "correct": False},
                {"id": "b", "text": "Nursing behavior as kittens", "correct": True},
                {"id": "c", "text": "Stretching muscles", "correct": False},
                {"id": "d", "text": "Learned from watching humans", "correct": False}
            ],
            "feedback": {
                "correct": "Correct! Kneading behavior originates from kittenhood when they knead their mother's belly while nursing.",
                "incorrect": "Not quite. Kneading comes from nursing behavior as kittens."
            }
        }
    ],
    "answer_key": {
        "q1": "c",
        "q2": "b",
        "q3": "c",
        "q4": "b",
        "q5": "b"
    },
    "results": {
        "key_takeaways": [
            "A happy cat holds its tail upright with a slight curl at the tip",
            "Flattened ears indicate fear or anger in cats",
            "Slow blinking is a sign of trust and affection (\"cat kisses\")",
            "A crouched position with dilated pupils typically indicates stress or fear",
            "Kneading behavior originates from nursing as kittens"
        ],
        "feedback_levels": [
            {
                "min_percentage": 80,
                "title": "Excellent!",
                "message": "You have a great understanding of cat body language!",
                "image": "happy-cat.png",
                "style": "alert-success"
            },
            {
                "min_percentage": 60,
                "title": "Good job!",
                "message": "You understand the basics of cat body language.",
                "image": "playful-cat.png",
                "style": "alert-info"
            },
            {
                "min_percentage": 0,
                "title": "Keep learning!",
                "message": "You might want to review the cat body language tutorials again.",
                "image": "stressed-cat.png",
                "style": "alert-warning"
            }
        ]
    }
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
        return redirect(url_for('quiz'))
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
    session['current_step'] = 0
    session['quiz_started'] = True
    session['quiz_score'] = 0
    
    # Redirect to the first step of the quiz
    return redirect(url_for('quiz_step', step_id=quiz_data['steps'][0]['id']))

@app.route('/quiz/step/<step_id>', methods=['GET'])
def quiz_step(step_id):
    if not session.get('quiz_started', False):
        return redirect(url_for('quiz'))
    
    # Find current step data
    current_step = None
    step_index = 0
    for i, step in enumerate(quiz_data['steps']):
        if step['id'] == step_id:
            current_step = step
            step_index = i
            break
    
    if not current_step:
        return redirect(url_for('quiz'))
    
    # Determine next and previous steps
    next_step = None
    prev_step = None
    if step_index < len(quiz_data['steps']) - 1:
        next_step = quiz_data['steps'][step_index + 1]['id']
    if step_index > 0:
        prev_step = quiz_data['steps'][step_index - 1]['id']
    
    # Store current step in session
    session['current_step'] = step_index
    
    # Render appropriate template based on step type
    if current_step['type'] == 'drag_drop':
        return render_template('quiz_drag_drop.html', 
                              quiz=quiz_data, 
                              step=current_step,
                              next_step=next_step,
                              prev_step=prev_step)
    else:  # multiple_choice
        return render_template('quiz_question.html', 
                              quiz=quiz_data, 
                              step=current_step,
                              next_step=next_step,
                              prev_step=prev_step)

@app.route('/quiz/submit_step/<step_id>', methods=['POST'])
def submit_step(step_id):
    if not session.get('quiz_started', False):
        return jsonify({'status': 'error', 'message': 'Quiz not started'})
    
    data = request.get_json()
    
    # Store answer in session
    answers = session.get('quiz_answers', {})
    answers[step_id] = data
    session['quiz_answers'] = answers
    
    # Update score if answer is correct
    if 'is_correct' in data and data['is_correct']:
        session['quiz_score'] = session.get('quiz_score', 0) + 1
    
    # Find next step
    current_step_index = 0
    for i, step in enumerate(quiz_data['steps']):
        if step['id'] == step_id:
            current_step_index = i
            break
    
    # Determine if this is the last step
    if current_step_index >= len(quiz_data['steps']) - 1:
        return jsonify({'status': 'success', 'next': url_for('quiz_result')})
    else:
        next_step_id = quiz_data['steps'][current_step_index + 1]['id']
        return jsonify({'status': 'success', 'next': url_for('quiz_step', step_id=next_step_id)})

@app.route('/quiz/result')
def quiz_result():
    if not session.get('quiz_started', False):
        return redirect(url_for('quiz'))
    
    # Calculate total score
    all_answers = session.get('quiz_answers', {})
    total = len(quiz_data['steps'])
    score = session.get('quiz_score', 0)
    
    percentage = (score / total * 100) if total > 0 else 0
    
    # Save results to database
    conn = get_db_connection()
    user_id = session.get('user_id', os.urandom(8).hex())
    session['user_id'] = user_id
    
    conn.execute(
        'INSERT INTO quiz_results (user_id, score, total, answers, timestamp) VALUES (?, ?, ?, ?, ?)',
        (user_id, score, total, json.dumps(all_answers), datetime.now())
    )
    conn.commit()
    conn.close()
    
    # Clear quiz session
    session['quiz_started'] = False
    
    return render_template('quiz_result.html', 
                          score=score, 
                          total=total,
                          percentage=percentage,
                          quiz=quiz_data)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
