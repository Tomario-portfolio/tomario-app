import os
from datetime import date
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}"
    f"@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT', '3306')}/{os.environ.get('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

CORS(app, supports_credentials=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    price_per_night = db.Column(db.Numeric(10, 2), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'room_number': self.room_number,
            'room_type': self.room_type,
            'price_per_night': float(self.price_per_night),
            'capacity': self.capacity,
            'description': self.description,
            'image_url': self.image_url,
        }


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='confirmed')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        room = db.session.get(Room, self.room_id)
        return {
            'id': self.id,
            'room': room.to_dict() if room else None,
            'check_in_date': self.check_in_date.isoformat(),
            'check_out_date': self.check_out_date.isoformat(),
            'total_price': float(self.total_price),
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'error': 'ログインが必要です'}), 401


# ------------------------------------------------------------
# Health Check
# ------------------------------------------------------------

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


# ------------------------------------------------------------
# Auth
# ------------------------------------------------------------

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'リクエストが不正です'}), 400

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({'error': '全項目を入力してください'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'そのメールアドレスは既に登録されています'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'そのユーザー名は既に使用されています'}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': '登録が完了しました'}), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'リクエストが不正です'}), 400

    email = data.get('email', '').strip()
    password = data.get('password', '')
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'メールアドレスまたはパスワードが正しくありません'}), 401

    login_user(user)
    return jsonify({'user': user.to_dict()})


@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'ログアウトしました'})


@app.route('/api/auth/me')
def me():
    if current_user.is_authenticated:
        return jsonify({'user': current_user.to_dict()})
    return jsonify({'error': '未ログイン'}), 401


# ------------------------------------------------------------
# Rooms
# ------------------------------------------------------------

@app.route('/api/rooms')
def rooms():
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')

    if check_in and check_out:
        check_in_date = date.fromisoformat(check_in)
        check_out_date = date.fromisoformat(check_out)
        booked_room_ids = db.session.query(Booking.room_id).filter(
            Booking.status == 'confirmed',
            Booking.check_in_date < check_out_date,
            Booking.check_out_date > check_in_date
        ).subquery()
        available_rooms = Room.query.filter(~Room.id.in_(booked_room_ids)).all()
    else:
        available_rooms = Room.query.all()

    return jsonify({'rooms': [r.to_dict() for r in available_rooms]})


@app.route('/api/rooms/<int:room_id>')
def room_detail(room_id):
    room = db.get_or_404(Room, room_id)
    return jsonify({'room': room.to_dict()})


# ------------------------------------------------------------
# Bookings
# ------------------------------------------------------------

@app.route('/api/bookings', methods=['GET'])
@login_required
def get_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return jsonify({'bookings': [b.to_dict() for b in bookings]})


@app.route('/api/bookings', methods=['POST'])
@login_required
def create_booking():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'リクエストが不正です'}), 400

    room_id = data.get('room_id')
    check_in = data.get('check_in')
    check_out = data.get('check_out')

    if not room_id or not check_in or not check_out:
        return jsonify({'error': '全項目を入力してください'}), 400

    room = db.get_or_404(Room, room_id)
    check_in_date = date.fromisoformat(check_in)
    check_out_date = date.fromisoformat(check_out)

    if check_in_date >= check_out_date:
        return jsonify({'error': 'チェックアウト日はチェックイン日より後にしてください'}), 400

    conflict = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.status == 'confirmed',
        Booking.check_in_date < check_out_date,
        Booking.check_out_date > check_in_date
    ).first()
    if conflict:
        return jsonify({'error': 'その期間は既に予約が入っています'}), 400

    nights = (check_out_date - check_in_date).days
    total_price = float(room.price_per_night) * nights
    booking = Booking(
        user_id=current_user.id,
        room_id=room_id,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        total_price=total_price
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({'booking': booking.to_dict()}), 201


@app.route('/api/bookings/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = db.get_or_404(Booking, booking_id)

    if booking.user_id != current_user.id:
        return jsonify({'error': '権限がありません'}), 403
    if booking.check_in_date <= date.today():
        return jsonify({'error': 'チェックイン日以降はキャンセルできません'}), 400

    days_until_checkin = (booking.check_in_date - date.today()).days
    if days_until_checkin >= 3:
        fee_rate = 0
    elif days_until_checkin == 2:
        fee_rate = 0.3
    else:
        fee_rate = 0.5

    cancellation_fee = round(float(booking.total_price) * fee_rate)

    booking.status = 'cancelled'
    db.session.commit()
    return jsonify({
        'message': '予約をキャンセルしました',
        'cancellation_fee': cancellation_fee,
        'fee_rate': fee_rate
    })


def seed_rooms():
    if Room.query.count() == 0:
        rooms = [
            Room(room_number='101', room_type='シングル', price_per_night=8000, capacity=1,
                 description='落ち着いた雰囲気のシングルルームです。',
                 image_url='https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80'),
            Room(room_number='102', room_type='シングル', price_per_night=8000, capacity=1,
                 description='落ち着いた雰囲気のシングルルームです。',
                 image_url='https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80'),
            Room(room_number='201', room_type='ダブル', price_per_night=12000, capacity=2,
                 description='ゆったりとしたダブルルームです。',
                 image_url='https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80'),
            Room(room_number='202', room_type='ダブル', price_per_night=12000, capacity=2,
                 description='ゆったりとしたダブルルームです。',
                 image_url='https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80'),
            Room(room_number='301', room_type='スイート', price_per_night=25000, capacity=3,
                 description='豪華なスイートルームです。特別なひとときをお過ごしください。',
                 image_url='https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80'),
        ]
        db.session.add_all(rooms)
        db.session.commit()


with app.app_context():
    db.create_all()
    seed_rooms()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
