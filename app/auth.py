from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, db
from app.models import Board  # For navigation

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    boards = Board.query.all()  # For navigation
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple validation
        if not username or not password:
            flash('Please fill all fields')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        user = User(
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('main.index'))
        
    return render_template('auth/register.html', boards=boards)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    boards = Board.query.all()  # For navigation
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again')
            return redirect(url_for('auth.login'))
            
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.index'))
        
    return render_template('auth/login.html', boards=boards)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
