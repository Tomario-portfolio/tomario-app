import os
from datetime import date
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
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

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'ログインしてください。'


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


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    price_per_night = db.Column(db.Numeric(10, 2), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    bookings = db.relationship('Booking', backref='room', lazy=True)


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


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('そのメールアドレスは既に登録されています。')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('そのユーザー名は既に使用されています。')
            return redirect(url_for('register'))
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('登録が完了しました。ログインしてください。')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('メールアドレスまたはパスワードが正しくありません。')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/rooms')
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
        check_in = ''
        check_out = ''

    return render_template('rooms.html', rooms=available_rooms, check_in=check_in, check_out=check_out)


@app.route('/rooms/<int:room_id>')
def room_detail(room_id):
    room = db.get_or_404(Room, room_id)
    check_in = request.args.get('check_in', '')
    check_out = request.args.get('check_out', '')
    return render_template('room_detail.html', room=room, check_in=check_in, check_out=check_out)


@app.route('/booking/<int:room_id>', methods=['GET', 'POST'])
@login_required
def booking(room_id):
    room = db.get_or_404(Room, room_id)
    if request.method == 'POST':
        check_in = date.fromisoformat(request.form['check_in'])
        check_out = date.fromisoformat(request.form['check_out'])

        if check_in >= check_out:
            flash('チェックアウト日はチェックイン日より後にしてください。')
            return redirect(url_for('booking', room_id=room_id))

        conflict = Booking.query.filter(
            Booking.room_id == room_id,
            Booking.status == 'confirmed',
            Booking.check_in_date < check_out,
            Booking.check_out_date > check_in
        ).first()
        if conflict:
            flash('その期間は既に予約が入っています。')
            return redirect(url_for('booking', room_id=room_id))

        nights = (check_out - check_in).days
        total_price = float(room.price_per_night) * nights
        new_booking = Booking(
            user_id=current_user.id,
            room_id=room_id,
            check_in_date=check_in,
            check_out_date=check_out,
            total_price=total_price
        )
        db.session.add(new_booking)
        db.session.commit()
        flash('予約が完了しました。')
        return redirect(url_for('my_bookings'))

    check_in = request.args.get('check_in', '')
    check_out = request.args.get('check_out', '')
    return render_template('booking.html', room=room, check_in=check_in, check_out=check_out)


@app.route('/my_bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template('my_bookings.html', bookings=bookings)


@app.route('/cancel/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = db.get_or_404(Booking, booking_id)
    if booking.user_id != current_user.id:
        flash('権限がありません。')
        return redirect(url_for('my_bookings'))
    if booking.check_in_date <= date.today():
        flash('チェックイン日以降はキャンセルできません。')
        return redirect(url_for('my_bookings'))
    booking.status = 'cancelled'
    db.session.commit()
    flash('予約をキャンセルしました。')
    return redirect(url_for('my_bookings'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
