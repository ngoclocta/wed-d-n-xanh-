from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import bcrypt
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    avatar_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    game_scores = db.relationship('GameScore', backref='user', lazy=True, cascade='all, delete-orphan')
    achievements = db.relationship('UserAchievement', backref='user', lazy=True, cascade='all, delete-orphan')
    activities = db.relationship('UserActivity', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def get_best_score(self, game_type):
        """Get user's best score for a specific game"""
        best_score = GameScore.query.filter_by(
            user_id=self.id, 
            game_type=game_type
        ).order_by(GameScore.score.desc()).first()
        return best_score.score if best_score else 0
    
    def get_total_games_played(self):
        """Get total number of games played by user"""
        return GameScore.query.filter_by(user_id=self.id).count()
    
    def get_achievements_count(self):
        """Get total number of achievements earned"""
        return UserAchievement.query.filter_by(user_id=self.id).count()
    
    def to_dict(self):
        """Convert user to dictionary for JSON response"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'total_games': self.get_total_games_played(),
            'achievements': self.get_achievements_count()
        }

class GameScore(db.Model):
    __tablename__ = 'game_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_type = db.Column(db.String(50), nullable=False)  # 'bottle_game', 'eco_quiz', 'carbon_calculator', etc.
    score = db.Column(db.Integer, nullable=False)
    level_reached = db.Column(db.Integer, default=1)
    time_played = db.Column(db.Integer)  # seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert game score to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'game_type': self.game_type,
            'score': self.score,
            'level_reached': self.level_reached,
            'time_played': self.time_played,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_type = db.Column(db.String(50), nullable=False)
    achievement_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert achievement to dictionary"""
        return {
            'id': self.id,
            'achievement_type': self.achievement_type,
            'achievement_name': self.achievement_name,
            'description': self.description,
            'earned_at': self.earned_at.isoformat() if self.earned_at else None
        }

class UserActivity(db.Model):
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # 'plastic_reduction', 'waste_sorting', etc.
    data = db.Column(db.Text)  # JSON string for activity-specific data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_data(self, data_dict):
        """Set activity data as JSON string"""
        self.data = json.dumps(data_dict)
    
    def get_data(self):
        """Get activity data as dictionary"""
        try:
            return json.loads(self.data) if self.data else {}
        except json.JSONDecodeError:
            return {}
    
    def to_dict(self):
        """Convert activity to dictionary"""
        return {
            'id': self.id,
            'activity_type': self.activity_type,
            'data': self.get_data(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Achievement definitions
ACHIEVEMENTS = {
    'first_game': {
        'name': 'Người Chơi Mới',
        'description': 'Chơi game đầu tiên',
        'icon': '🎮'
    },
    'bottle_collector': {
        'name': 'Thợ Nhặt Chai',
        'description': 'Nhặt được 50 chai nhựa',
        'icon': '🍼'
    },
    'eco_expert': {
        'name': 'Chuyên Gia Môi Trường',
        'description': 'Đạt 80% độ chính xác trong quiz',
        'icon': '🌱'
    },
    'carbon_saver': {
        'name': 'Người Tiết Kiệm Carbon',
        'description': 'Giảm 10kg CO2 trong tháng',
        'icon': '🌍'
    },
    'waste_master': {
        'name': 'Bậc Thầy Phân Loại',
        'description': 'Phân loại đúng 100 món rác',
        'icon': '♻️'
    },
    'memory_champion': {
        'name': 'Nhà Vô Địch Trí Nhớ',
        'description': 'Hoàn thành memory game trong 30 giây',
        'icon': '🧠'
    },
    'green_builder': {
        'name': 'Kiến Trúc Sư Xanh',
        'description': 'Xây dựng thành phố 100% năng lượng tái tạo',
        'icon': '🏗️'
    },
    'daily_player': {
        'name': 'Người Chơi Hàng Ngày',
        'description': 'Chơi game 7 ngày liên tiếp',
        'icon': '📅'
    },
    'social_butterfly': {
        'name': 'Bướm Xã Hội',
        'description': 'Kết bạn với 10 người chơi',
        'icon': '👥'
    },
    'top_scorer': {
        'name': 'Điểm Số Cao Nhất',
        'description': 'Đứng top 10 bảng xếp hạng',
        'icon': '🏆'
    }
}

def check_and_award_achievements(user_id, game_type=None, score=None):
    """Check and award achievements to user"""
    user = User.query.get(user_id)
    if not user:
        return []
    
    new_achievements = []
    
    # Check first game achievement
    if user.get_total_games_played() == 1:
        if not UserAchievement.query.filter_by(user_id=user_id, achievement_type='first_game').first():
            achievement = UserAchievement(
                user_id=user_id,
                achievement_type='first_game',
                achievement_name=ACHIEVEMENTS['first_game']['name'],
                description=ACHIEVEMENTS['first_game']['description']
            )
            db.session.add(achievement)
            new_achievements.append(achievement)
    
    # Check bottle collector achievement
    if game_type == 'bottle_game':
        total_bottles = db.session.query(db.func.sum(GameScore.score)).filter_by(
            user_id=user_id, game_type='bottle_game'
        ).scalar() or 0
        
        if total_bottles >= 50:
            if not UserAchievement.query.filter_by(user_id=user_id, achievement_type='bottle_collector').first():
                achievement = UserAchievement(
                    user_id=user_id,
                    achievement_type='bottle_collector',
                    achievement_name=ACHIEVEMENTS['bottle_collector']['name'],
                    description=ACHIEVEMENTS['bottle_collector']['description']
                )
                db.session.add(achievement)
                new_achievements.append(achievement)
    
    # Check daily player achievement
    recent_games = GameScore.query.filter_by(user_id=user_id).filter(
        GameScore.created_at >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    ).count()
    
    if recent_games > 0:
        # Check if user played for 7 consecutive days (simplified check)
        daily_count = db.session.query(
            db.func.date(GameScore.created_at)
        ).filter_by(user_id=user_id).distinct().count()
        
        if daily_count >= 7:
            if not UserAchievement.query.filter_by(user_id=user_id, achievement_type='daily_player').first():
                achievement = UserAchievement(
                    user_id=user_id,
                    achievement_type='daily_player',
                    achievement_name=ACHIEVEMENTS['daily_player']['name'],
                    description=ACHIEVEMENTS['daily_player']['description']
                )
                db.session.add(achievement)
                new_achievements.append(achievement)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error awarding achievements: {e}")
    
    return new_achievements

