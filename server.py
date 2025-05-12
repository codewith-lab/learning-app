
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Track user status
tutorial_progress = {
    "stressed-fearful": {
        'explored_parts': [],
        'explored_sounds': [],
        'finished': False
    },
    "painful-sick": {
        'explored_parts': [],
        'explored_sounds': [],
        'finished': False
    },
    "curious-playful": {
        'explored_parts': [],
        'explored_sounds': [],
        'finished': False
    },
    "happy-relaxed": {
        'explored_parts': [],
        'explored_sounds': [],
        'finished': False
    },
}
quiz_results = {}  

# Load scenario data
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
    "sound": "Hissing (defensive warning), or growling (aggression from fear)",
    "sound-file": "stressed-hiss.mp3, stressed-growl.mp3",
    "cat-image": "stressed-cat.png",
    "env-image": "https://i5.walmartimages.com/asr/50d6a74d-aedf-4907-ad67-66dc36b251c2.51983cf5dbd54c51ae2be5cc6d40da83.jpeg?odnHeight=640&odnWidth=640&odnBg=FFFFFF",
    "image-ctrl": {
          "top": "28%",
          "left": "43%",
          "width": "28%",
          "height": "28%"
        },
    "positions": {
            "ear": {"top": "28%", "left": "38%"},
            "eye": {"top": "33%", "left": "42%"},
            "tail": {"top": "50%", "left": "13%"},
            "body": {"top": "25%", "left": "25%"},
            "paw": {"top": "", "left": ""},
            "sound": {"top": "43%", "left": "43%"},
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
    "sound": "Barely audible, or no sound at all",
    "sound-file": "",
    "cat-image": "sick-cat.png",
    "env-image": "https://www.maupets.com/cdn/shop/files/Bao_Modern_Solid_Wood_Cat_Tree_For_Large_Cats_main_1200x.jpg?v=1723223489",
    "image-ctrl": {
          "top": "35%",
          "left": "28%",
          "width": "30%",
          "height": "30%"
        },
    "positions": {
            "ear": {"top": "20%", "left": "30%"},
            "eye": {"top": "30%", "left": "35%"},
            "tail": {"top": "70%", "left": "25%"},
            "body": {"top": "40%", "left": "25%"},
            "paw": {"top": "", "left": ""},
            "sound": {"top": "38%", "left": "35%"},
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
    "sound-file": "playful-chirp.mp3, playful-trill.mp3",
    "cat-image": "playful-cat.png",
    "env-image": "https://www.thespruce.com/thmb/R-M6g-5koC4oSLQ1CeIQ-bsBQVA=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/cat-climbing-shelf-wall-8b636cf12c4347d5a1b71266f42586f8.jpeg",
    "image-ctrl": {
          "top": "35%",
          "left": "58%",
          "width": "25%",
          "height": "25%"
        },
    "positions": {
            "ear": {"top": "26%", "left": "8%"},
            "eye": {"top": "35%", "left": "10%"},
            "tail": {"top": "18%", "left": "38%"},
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
    "eye": "Round or partially closed, pupils narrow like slits, blinks slowly at you (\"cat kisses\" of trust)",
    "tail": "Pointed straight up, may sway gently like a metronome",
    "body": "Rolling belly-up, stretching out fully",
    "paw": "Kneading (\"making biscuits\" with paws)",
    "sound": "Gentle purring",
    "sound-file": "happy-purr.mp3",
    "cat-image": "happy-cat.png",
    "env-image": "https://www.thespruce.com/thmb/nMb1vvPeJdpvNsZVAiswHhry1iM=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/cat-playroom-1448b64778434eaf88b3dcf2695bde2e.jpeg",
    "image-ctrl": {
          "top": "55%",
          "left": "40%",
          "width": "30%",
          "height": "30%"
        },
    "positions": {
            "ear": {"top": "18%", "left": "22%"},
            "eye": {"top": "26%", "left": "22%"},
            "tail": {"top": "28%", "left": "32%"},
            "body": {"top": "46%", "left": "30%"},
            "paw": {"top": "76%", "left": "28%"},
            "sound": {"top": "33%", "left": "23%"},
        },
    "next": "end",
    "prev": "3"
  },
}

# Quiz Data Structure - stored as JSON instead of in the database
quiz_data = {
    "title": "Cat Body Language Quiz",
    "drag_drop": {
        "title": "Categorize Cats by Body Language",
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
    "questions": [
        {
            "id": "q1",
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
# Function to save quiz results to JSON file
def save_quiz_result(user_id, score, total, answers):
    result = {
        "user_id": user_id,
        "score": score,
        "total": total,
        "answers": answers,
        "timestamp": f"{datetime.now()}"
    }
    
    # Store directly in the global dictionary instead of writing to file
    global quiz_results
    quiz_results[user_id] = result
    
    return user_id

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tutorial')
def tutorial():
    return render_template('scenario.html')

@app.route('/tutorial/<category>')
def tutorial_category(category):
    global scenarios, tutorial_progress

    if category == 'end':
        return redirect(url_for('quiz_start'))
    if category == 'begin':
        return render_template('index.html')

    if category not in tutorial_progress:
        tutorial_progress[category] = {
            'explored_parts': [],
            'explored_sounds': [],
            'finished': False
    }
    
    explored_parts = tutorial_progress[category].get('explored_parts', [])
    explored_sounds = tutorial_progress[category].get('explored_sounds', [])
    finished_sessions = [cat for cat, info in tutorial_progress.items() if info.get("finished", False)]

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
                              prev_category = prev_category,
                              explored_parts = explored_parts,
                              explored_sounds = explored_sounds,
                              finished_sessions = finished_sessions)
    
    return render_template('index.html')

# AJAX FUNCTIONS
@app.route('/save_tutorial_progress', methods=['POST'])
def save_tutorial_progress():
    data = request.get_json()
    category = data.get('category')
    
    if data.get('part') and data['part'] not in tutorial_progress[category]['explored_parts']:
        tutorial_progress[category]['explored_parts'].append(data['part'])
    
    if data.get('sound') and data['sound'] not in tutorial_progress[category]['explored_sounds']:
        tutorial_progress[category]['explored_sounds'].append(data['sound'])
    
    if data.get('finished'):
        tutorial_progress[category]['finished'] = data['finished']

    return jsonify({'status': 'success'})

@app.route('/quiz')
def quiz():
    # Initialize quiz session
    session['quiz_started'] = True
    session['quiz_answers'] = {}
    
    # Redirect to the first step (drag and drop)
    return redirect(url_for('quiz_step', step='drag_drop'))

@app.route('/quiz/step/<step>')
def quiz_step(step):
    if not session.get('quiz_started', False):
        return redirect(url_for('quiz'))
    
    # Calculate total steps: 1 for drag and drop + number of questions
    total_steps = 1 + len(quiz_data['questions'])
    total_possible = len(quiz_data['drag_drop']['drag_items']) + len(quiz_data['questions'])
    
    # Calculate current score from existing answers
    answers = session.get('quiz_answers', {})
    current_score = 0
    
    # Count correct drag and drop items
    if 'drag_drop' in answers:
        for item in answers.get('drag_drop', []):
            if item.get('category') == item.get('correctCategory'):
                current_score += 1
    
    # Count correct multiple choice answers
    for question in quiz_data['questions']:
        question_id = question['id']
        if question_id in answers:
            user_answer = answers.get(question_id)
            correct_answer = quiz_data['answer_key'].get(question_id)
            if user_answer == correct_answer:
                current_score += 1
    
    # Handle drag and drop step
    if step == 'drag_drop':
        current_step = 0
        prev_url = url_for('tutorial_category', category='happy-relaxed')  # Go back to tutorials
        next_url = url_for('quiz_step', step='q1')  # First question
        
        return render_template('quiz_questions/drag_drop.html',
                              quiz=quiz_data,
                              current_step=current_step,
                              total_steps=total_steps,
                              prev_url=prev_url,
                              next_url=next_url,
                              current_score=current_score,
                              total_possible=total_possible)
    
    # Handle question steps
    else:
        # Find question index
        question_index = -1
        for i, question in enumerate(quiz_data['questions']):
            if question['id'] == step:
                question_index = i
                break
        
        # If question not found, redirect to quiz start
        if question_index == -1:
            return redirect(url_for('quiz'))
        
        # Calculate current step (drag_drop is step 0, first question is step 1)
        current_step = question_index + 1
        
        # Determine prev/next URLs
        if question_index == 0:
            prev_url = url_for('quiz_step', step='drag_drop')
        else:
            prev_url = url_for('quiz_step', step=quiz_data['questions'][question_index-1]['id'])
        
        if question_index == len(quiz_data['questions']) - 1:
            is_last_question = True
        else:
            is_last_question = False
        
        return render_template('quiz_questions/quiz_questions.html',
                              quiz=quiz_data,
                              question=quiz_data['questions'][question_index],
                              question_number=question_index + 1,
                              current_step=current_step,
                              total_steps=total_steps,
                              prev_url=prev_url,
                              is_last_question=is_last_question,
                              current_score=current_score,
                              total_possible=total_possible)

@app.route('/quiz/submit', methods=['POST'])
def quiz_submit_step():
    if not session.get('quiz_started', False):
        return jsonify({'status': 'error', 'message': 'Quiz not started'})
    
    data = request.get_json()
    answers = session.get('quiz_answers', {})
    
    step_type = data.get('step_type')
    
    if step_type == 'drag_drop':
        # Save drag and drop selections
        drag_drop_selections = data.get('drag_drop_selections', [])
        answers['drag_drop'] = drag_drop_selections
        
        # Next step is first question
        next_url = url_for('quiz_step', step=quiz_data['questions'][0]['id'])
    
    elif step_type == 'question':
        # Save question answer
        question_id = data.get('question_id')
        selected_option = data.get('selected_option')
        answers[question_id] = selected_option
        
        # Find question index
        question_index = -1
        for i, question in enumerate(quiz_data['questions']):
            if question['id'] == question_id:
                question_index = i
                break
        
        if question_index == -1:
            return jsonify({'status': 'error', 'message': 'Invalid question ID'})
        
        # If this is the last question, go to results
        if question_index == len(quiz_data['questions']) - 1:
            # Calculate score
            score = calculate_quiz_score(answers)
            
            # Save results
            user_id = session.get('user_id', os.urandom(8).hex())
            session['user_id'] = user_id
            save_quiz_result(user_id, score['total_score'], score['possible_score'], answers)
            
            # Save to session for results page
            session['final_score'] = score['total_score']
            session['final_total'] = score['possible_score']
            
            next_url = url_for('quiz_result')
        else:
            # Next question
            next_url = url_for('quiz_step', step=quiz_data['questions'][question_index + 1]['id'])
    
    else:
        return jsonify({'status': 'error', 'message': 'Invalid step type'})
    
    # Update session answers
    session['quiz_answers'] = answers
    
    return jsonify({
        'status': 'success',
        'next_url': next_url
    })

def calculate_quiz_score(answers):
    # Score drag and drop section
    drag_drop_score = 0
    drag_drop_total = len(quiz_data['drag_drop']['drag_items'])
    
    for item in answers.get('drag_drop', []):
        if item.get('category') == item.get('correctCategory'):
            drag_drop_score += 1
    
    # Score multiple choice questions
    mc_score = 0
    mc_total = len(quiz_data['questions'])
    
    for question in quiz_data['questions']:
        question_id = question['id']
        user_answer = answers.get(question_id)
        correct_answer = quiz_data['answer_key'].get(question_id)
        
        if user_answer == correct_answer:
            mc_score += 1
    
    # Total score
    total_score = drag_drop_score + mc_score
    possible_score = drag_drop_total + mc_total
    
    return {
        'drag_drop_score': drag_drop_score,
        'drag_drop_total': drag_drop_total,
        'mc_score': mc_score,
        'mc_total': mc_total,
        'total_score': total_score,
        'possible_score': possible_score
    }

@app.route('/quiz/result')
def quiz_result():
    # Check for score in session
    score = session.get('final_score')
    total = session.get('final_total')
    
    # If we can't find the score, redirect to quiz
    if score is None or total is None:
        return redirect(url_for('quiz'))
    
    # Calculate percentage
    percentage = (score / total * 100) if total > 0 else 0
    
    return render_template('quiz_result.html', 
                          score=score, 
                          total=total,
                          percentage=percentage,
                          quiz=quiz_data)

@app.route('/quiz/start')
def quiz_start():
    global tutorial_progress
    all_finished = all(category['finished'] for category in tutorial_progress.values())
    unfinished_cat = list( filter(
        lambda category: not tutorial_progress[category]['finished'],
        tutorial_progress ))

    return render_template('quiz_start.html',
                           all_finished=all_finished,
                           unfinished_cat=unfinished_cat)

if __name__ == '__main__':
   app.run(debug = True, port = 5002)
