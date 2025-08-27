from flask import Blueprint, request, jsonify, session, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, GameScore, UserAchievement, check_and_award_achievements
from datetime import datetime
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Mật khẩu phải có ít nhất 6 ký tự"
    if not re.search(r'[A-Za-z]', password):
        return False, "Mật khẩu phải chứa ít nhất 1 chữ cái"
    if not re.search(r'[0-9]', password):
        return False, "Mật khẩu phải chứa ít nhất 1 số"
    return True, "Mật khẩu hợp lệ"

def validate_username(username):
    """Validate username format"""
    if len(username) < 3:
        return False, "Tên đăng nhập phải có ít nhất 3 ký tự"
    if len(username) > 20:
        return False, "Tên đăng nhập không được quá 20 ký tự"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Tên đăng nhập chỉ được chứa chữ cái, số và dấu gạch dưới"
    return True, "Tên đăng nhập hợp lệ"

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'GET':
        return render_template('auth/register.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        full_name = data.get('full_name', '').strip()
        
        # Validation
        if not username or not email or not password:
            return jsonify({
                'success': False,
                'message': 'Vui lòng điền đầy đủ thông tin'
            }), 400
        
        # Validate username
        valid_username, username_msg = validate_username(username)
        if not valid_username:
            return jsonify({
                'success': False,
                'message': username_msg
            }), 400
        
        # Validate email
        if not validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Email không hợp lệ'
            }), 400
        
        # Validate password
        valid_password, password_msg = validate_password(password)
        if not valid_password:
            return jsonify({
                'success': False,
                'message': password_msg
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'message': 'Tên đăng nhập đã tồn tại'
            }), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'message': 'Email đã được sử dụng'
            }), 400
        
        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=full_name if full_name else username
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Auto login after registration
        login_user(user, remember=True)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Đăng ký thành công!',
            'user': user.to_dict(),
            'redirect': url_for('dashboard')
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi hệ thống: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        username_or_email = data.get('username', '').strip()
        password = data.get('password', '')
        remember = data.get('remember', False)
        
        if not username_or_email or not password:
            return jsonify({
                'success': False,
                'message': 'Vui lòng điền đầy đủ thông tin'
            }), 400
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username_or_email) | 
            (User.email == username_or_email.lower())
        ).first()
        
        if not user or not user.check_password(password):
            return jsonify({
                'success': False,
                'message': 'Tên đăng nhập hoặc mật khẩu không đúng'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'message': 'Tài khoản đã bị khóa'
            }), 401
        
        # Login user
        login_user(user, remember=remember)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Đăng nhập thành công!',
            'user': user.to_dict(),
            'redirect': url_for('dashboard')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi hệ thống: {str(e)}'
        }), 500

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('Đã đăng xuất thành công', 'success')
    return redirect(url_for('index'))

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    try:
        # Get user's game statistics
        game_stats = {}
        game_types = ['bottle_game', 'eco_quiz', 'carbon_calculator', 'waste_sorting', 'memory_game']
        
        for game_type in game_types:
            best_score = current_user.get_best_score(game_type)
            total_games = GameScore.query.filter_by(
                user_id=current_user.id, 
                game_type=game_type
            ).count()
            
            game_stats[game_type] = {
                'best_score': best_score,
                'total_games': total_games
            }
        
        # Get recent achievements
        recent_achievements = UserAchievement.query.filter_by(
            user_id=current_user.id
        ).order_by(UserAchievement.earned_at.desc()).limit(5).all()
        
        # Get recent game scores
        recent_scores = GameScore.query.filter_by(
            user_id=current_user.id
        ).order_by(GameScore.created_at.desc()).limit(10).all()
        
        return render_template('auth/profile.html',
            user=current_user,
            game_stats=game_stats,
            recent_achievements=recent_achievements,
            recent_scores=recent_scores
        )
        
    except Exception as e:
        flash(f'Lỗi tải trang cá nhân: {str(e)}', 'error')
        return redirect(url_for('index'))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    try:
        # Get user statistics
        total_games = current_user.get_total_games_played()
        total_achievements = current_user.get_achievements_count()
        
        # Get best scores for each game
        best_scores = {}
        game_types = ['bottle_game', 'eco_quiz', 'carbon_calculator', 'waste_sorting', 'memory_game']
        
        for game_type in game_types:
            best_scores[game_type] = current_user.get_best_score(game_type)
        
        # Get recent activities
        recent_scores = GameScore.query.filter_by(
            user_id=current_user.id
        ).order_by(GameScore.created_at.desc()).limit(5).all()
        
        # Get recent achievements
        recent_achievements = UserAchievement.query.filter_by(
            user_id=current_user.id
        ).order_by(UserAchievement.earned_at.desc()).limit(3).all()
        
        return render_template('auth/dashboard.html',
            user=current_user,
            total_games=total_games,
            total_achievements=total_achievements,
            best_scores=best_scores,
            recent_scores=recent_scores,
            recent_achievements=recent_achievements
        )
        
    except Exception as e:
        flash(f'Lỗi tải dashboard: {str(e)}', 'error')
        return redirect(url_for('index'))

@auth_bp.route('/api/user/current')
@login_required
def get_current_user():
    """Get current user info via API"""
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    })

@auth_bp.route('/api/user/update', methods=['POST'])
@login_required
def update_user():
    """Update user profile"""
    try:
        data = request.get_json()
        
        full_name = data.get('full_name', '').strip()
        avatar_url = data.get('avatar_url', '').strip()
        
        if full_name:
            current_user.full_name = full_name
        
        if avatar_url:
            current_user.avatar_url = avatar_url
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cập nhật thông tin thành công',
            'user': current_user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi cập nhật: {str(e)}'
        }), 500

@auth_bp.route('/api/user/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    try:
        data = request.get_json()
        
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        confirm_password = data.get('confirm_password', '')
        
        if not current_password or not new_password or not confirm_password:
            return jsonify({
                'success': False,
                'message': 'Vui lòng điền đầy đủ thông tin'
            }), 400
        
        if not current_user.check_password(current_password):
            return jsonify({
                'success': False,
                'message': 'Mật khẩu hiện tại không đúng'
            }), 400
        
        if new_password != confirm_password:
            return jsonify({
                'success': False,
                'message': 'Mật khẩu mới không khớp'
            }), 400
        
        # Validate new password
        valid_password, password_msg = validate_password(new_password)
        if not valid_password:
            return jsonify({
                'success': False,
                'message': password_msg
            }), 400
        
        current_user.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Đổi mật khẩu thành công'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi đổi mật khẩu: {str(e)}'
        }), 500

@auth_bp.route('/api/leaderboard/<game_type>')
def get_leaderboard(game_type):
    """Get leaderboard for specific game"""
    try:
        # Get top 50 scores for the game type
        top_scores = db.session.query(
            GameScore.score,
            GameScore.created_at,
            User.username,
            User.full_name,
            User.avatar_url
        ).join(User).filter(
            GameScore.game_type == game_type
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
            'leaderboard': leaderboard,
            'game_type': game_type
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi tải bảng xếp hạng: {str(e)}'
        }), 500

@auth_bp.route('/api/game/save-score', methods=['POST'])
@login_required
def save_game_score():
    """Save game score for current user"""
    try:
        data = request.get_json()
        
        game_type = data.get('game_type')
        score = data.get('score')
        level_reached = data.get('level_reached', 1)
        time_played = data.get('time_played')
        
        if not game_type or score is None:
            return jsonify({
                'success': False,
                'message': 'Thiếu thông tin game'
            }), 400
        
        # Save score
        game_score = GameScore(
            user_id=current_user.id,
            game_type=game_type,
            score=score,
            level_reached=level_reached,
            time_played=time_played
        )
        
        db.session.add(game_score)
        db.session.commit()
        
        # Check for achievements
        new_achievements = check_and_award_achievements(
            current_user.id, 
            game_type=game_type, 
            score=score
        )
        
        return jsonify({
            'success': True,
            'message': 'Lưu điểm thành công',
            'score_id': game_score.id,
            'new_achievements': [ach.to_dict() for ach in new_achievements]
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi lưu điểm: {str(e)}'
        }), 500

