from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.user import User
from app import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user is not None and user.check_password(password):
            # Log the user in
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('user.login'))

    return render_template('user/login.html')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User(email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Log the user in
        return redirect(url_for('index'))

    return render_template('user/register.html')
