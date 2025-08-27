from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from flask_cors import CORS
import os
import json
import random
from datetime import datetime
import sys
sys.path.append('/home/ubuntu/houc-website')

# Import models and auth
from models import db, User, GameScore, UserAchievement, check_and_award_achievements
from auth import auth_bp
from ocean_cleanup_data import OCEAN_WASTE_TYPES, ENVIRONMENTAL_QUESTIONS, COMPLETION_MESSAGES, GAME_CONFIG

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubuntu/houc-website/web_xanh.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
CORS(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

@app.route('/waste-sorting')
def waste_sorting():
    """Trang phân loại rác"""
    return render_template('waste_sorting.html')

@app.route('/bottle-game')
def bottle_game():
    """Trang game nhặt chai nhựa"""
    return render_template('bottle_game.html')

@app.route('/plastic-reduction')
def plastic_reduction():
    """Trang hạn chế túi nilon"""
    return render_template('plastic_reduction.html')

@app.route('/ai-consultant')
def ai_consultant():
    """Trang AI tư vấn môi trường"""
    return render_template('ai_consultant.html')

@app.route('/diy-recycling')
def diy_recycling():
    """Trang DIY tái chế"""
    return render_template('diy_recycling.html')

@app.route('/video-search')
def video_search():
    """Trang tìm kiếm video DIY"""
    return render_template('video_search.html')

@app.route('/ocean-cleanup')
def ocean_cleanup():
    """Trang game nhặt rác thải dưới đại dương"""
    return render_template('ocean_cleanup.html')

@app.route('/games')
def games():
    """Trang danh sách các trò chơi"""
    return render_template('games.html')

@app.route('/leaderboard')
def leaderboard():
    """Trang bảng xếp hạng tổng hợp"""
    return render_template('leaderboard.html')

# API Routes for Ocean Cleanup Game
@app.route('/api/ocean-cleanup/start', methods=['POST'])
@login_required
def start_ocean_cleanup():
    """Bắt đầu game nhặt rác đại dương"""
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 'easy')
        
        if difficulty not in GAME_CONFIG['difficulty_levels']:
            difficulty = 'easy'
        
        # Tạo session game mới
        game_session = {
            'session_id': f"ocean_{current_user.id}_{int(datetime.now().timestamp())}",
            'user_id': current_user.id,
            'difficulty': difficulty,
            'start_time': datetime.now().isoformat(),
            'score': 0,
            'waste_collected': 0,
            'questions_answered': 0,
            'correct_answers': 0,
            'current_streak': 0,
            'max_streak': 0,
            'is_active': True
        }
        
        # Lưu vào session
        session['ocean_game'] = game_session
        
        return jsonify({
            'success': True,
            'session_id': game_session['session_id'],
            'difficulty': difficulty,
            'config': GAME_CONFIG['difficulty_levels'][difficulty],
            'total_waste_items': GAME_CONFIG['total_waste_items']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi khởi tạo game: {str(e)}'
        }), 500

@app.route('/api/ocean-cleanup/collect-waste', methods=['POST'])
@login_required
def collect_waste():
    """Thu thập rác thải và trả về câu hỏi"""
    try:
        data = request.get_json()
        waste_type = data.get('waste_type')
        
        if 'ocean_game' not in session:
            return jsonify({
                'success': False,
                'message': 'Game session không tồn tại'
            }), 400
        
        game_session = session['ocean_game']
        
        if not game_session['is_active']:
            return jsonify({
                'success': False,
                'message': 'Game đã kết thúc'
            }), 400
        
        if waste_type not in OCEAN_WASTE_TYPES:
            return jsonify({
                'success': False,
                'message': 'Loại rác không hợp lệ'
            }), 400
        
        # Chọn câu hỏi ngẫu nhiên
        question = random.choice(ENVIRONMENTAL_QUESTIONS)
        
        # Cập nhật session
        game_session['waste_collected'] += 1
        session['ocean_game'] = game_session
        
        return jsonify({
            'success': True,
            'waste_info': OCEAN_WASTE_TYPES[waste_type],
            'question': {
                'id': question['id'],
                'question': question['question'],
                'options': question['options']
            },
            'waste_collected': game_session['waste_collected'],
            'total_waste_items': GAME_CONFIG['total_waste_items']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi thu thập rác: {str(e)}'
        }), 500

@app.route('/api/ocean-cleanup/answer-question', methods=['POST'])
@login_required
def answer_question():
    """Trả lời câu hỏi môi trường"""
    try:
        data = request.get_json()
        question_id = data.get('question_id')
        selected_answer = data.get('selected_answer')
        waste_type = data.get('waste_type')
        response_time = data.get('response_time', 30)  # seconds
        
        if 'ocean_game' not in session:
            return jsonify({
                'success': False,
                'message': 'Game session không tồn tại'
            }), 400
        
        game_session = session['ocean_game']
        
        # Tìm câu hỏi
        question = next((q for q in ENVIRONMENTAL_QUESTIONS if q['id'] == question_id), None)
        if not question:
            return jsonify({
                'success': False,
                'message': 'Câu hỏi không tồn tại'
            }), 400
        
        # Kiểm tra đáp án
        is_correct = selected_answer == question['correct']
        
        # Tính điểm
        base_points = OCEAN_WASTE_TYPES[waste_type]['points']
        difficulty_multiplier = GAME_CONFIG['difficulty_levels'][game_session['difficulty']]['points_multiplier']
        
        points_earned = 0
        if is_correct:
            points_earned = int(base_points * difficulty_multiplier)
            
            # Bonus điểm cho tốc độ
            if response_time < 10:
                points_earned += GAME_CONFIG['bonus_points']['speed_bonus']
            
            # Cập nhật streak
            game_session['current_streak'] += 1
            game_session['max_streak'] = max(game_session['max_streak'], game_session['current_streak'])
            
            # Bonus điểm cho streak
            if game_session['current_streak'] >= 3:
                points_earned += GAME_CONFIG['bonus_points']['streak_bonus']
            
            game_session['correct_answers'] += 1
        else:
            game_session['current_streak'] = 0
        
        # Cập nhật session
        game_session['score'] += points_earned
        game_session['questions_answered'] += 1
        session['ocean_game'] = game_session
        
        # Kiểm tra hoàn thành game
        is_completed = game_session['waste_collected'] >= GAME_CONFIG['total_waste_items']
        completion_message = ""
        
        if is_completed:
            # Bonus điểm hoàn thành
            completion_bonus = GAME_CONFIG['bonus_points']['completion_bonus']
            game_session['score'] += completion_bonus
            game_session['is_active'] = False
            session['ocean_game'] = game_session
            
            # Chọn thông điệp hoàn thành ngẫu nhiên
            completion_message = random.choice(COMPLETION_MESSAGES)
            
            # Lưu điểm vào database
            try:
                game_score = GameScore(
                    user_id=current_user.id,
                    game_type='ocean_cleanup',
                    score=game_session['score'],
                    level_reached=1,
                    time_played=int((datetime.now() - datetime.fromisoformat(game_session['start_time'])).total_seconds())
                )
                db.session.add(game_score)
                db.session.commit()
                
                # Kiểm tra achievements
                new_achievements = check_and_award_achievements(
                    current_user.id,
                    game_type='ocean_cleanup',
                    score=game_session['score']
                )
                
            except Exception as e:
                print(f"Lỗi lưu điểm: {e}")
        
        return jsonify({
            'success': True,
            'is_correct': is_correct,
            'correct_answer': question['options'][question['correct']],
            'explanation': question['explanation'],
            'points_earned': points_earned,
            'total_score': game_session['score'],
            'current_streak': game_session['current_streak'],
            'is_completed': is_completed,
            'completion_message': completion_message,
            'game_stats': {
                'waste_collected': game_session['waste_collected'],
                'questions_answered': game_session['questions_answered'],
                'correct_answers': game_session['correct_answers'],
                'accuracy': round((game_session['correct_answers'] / game_session['questions_answered']) * 100, 1) if game_session['questions_answered'] > 0 else 0,
                'max_streak': game_session['max_streak']
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi xử lý câu trả lời: {str(e)}'
        }), 500

@app.route('/api/ocean-cleanup/get-waste-types')
def get_waste_types():
    """Lấy danh sách các loại rác thải"""
    return jsonify({
        'success': True,
        'waste_types': OCEAN_WASTE_TYPES
    })

@app.route('/api/ocean-cleanup/leaderboard')
def ocean_cleanup_leaderboard():
    """Bảng xếp hạng game nhặt rác đại dương"""
    try:
        # Lấy top 50 điểm cao nhất
        top_scores = db.session.query(
            GameScore.score,
            GameScore.created_at,
            User.username,
            User.full_name,
            User.avatar_url
        ).join(User).filter(
            GameScore.game_type == 'ocean_cleanup'
        ).order_by(GameScore.score.desc()).limit(50).all()
        
        leaderboard = []
        for i, (score, created_at, username, full_name, avatar_url) in enumerate(top_scores):
            leaderboard.append({
                'rank': i + 1,
                'username': username,
                'full_name': full_name or username,
                'avatar_url': avatar_url,
                'score': score,
                'created_at': created_at.isoformat() if created_at else None
            })
        
        return jsonify({
            'success': True,
            'leaderboard': leaderboard
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi tải bảng xếp hạng: {str(e)}'
        }), 500

# API cho các game khác (giữ nguyên từ version cũ)
@app.route('/api/bottle-game/save-score', methods=['POST'])
def save_bottle_game_score():
    """Lưu điểm game nhặt chai (cho cả user và guest)"""
    try:
        data = request.get_json()
        score = data.get('score', 0)
        time_played = data.get('time_played', 0)
        
        if current_user.is_authenticated:
            # Lưu vào database cho user đã đăng nhập
            game_score = GameScore(
                user_id=current_user.id,
                game_type='bottle_game',
                score=score,
                time_played=time_played
            )
            db.session.add(game_score)
            db.session.commit()
            
            # Kiểm tra achievements
            new_achievements = check_and_award_achievements(
                current_user.id,
                game_type='bottle_game',
                score=score
            )
            
            return jsonify({
                'success': True,
                'message': 'Lưu điểm thành công',
                'user_logged_in': True,
                'new_achievements': [ach.to_dict() for ach in new_achievements]
            })
        else:
            # Chỉ trả về thông báo cho guest
            return jsonify({
                'success': True,
                'message': 'Điểm đã được ghi nhận',
                'user_logged_in': False,
                'suggestion': 'Đăng ký tài khoản để lưu điểm và tham gia bảng xếp hạng!'
            })
            
    except Exception as e:
        if current_user.is_authenticated:
            db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi lưu điểm: {str(e)}'
        }), 500

@app.route("/api/ai-chat", methods=["POST"])
def ai_chat():
    # This would integrate with OpenAI API in a real implementation
    data = request.get_json()
    message = data.get("message", "")
    
    # Simple mock response
    response = {
        "response": "Cảm ơn bạn đã quan tâm đến môi trường! Đây là phản hồi mẫu từ AI."
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

