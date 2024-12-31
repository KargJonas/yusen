import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user, login_required
from app.models import User, Vote, db, Board, Thread, Post
from PIL import Image
import uuid

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_image(file):
    if not file:
        return None
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Save and optimize image
        image = Image.open(file)
        image.thumbnail((2000, 2000))  # Max dimensions
        image.save(filepath, optimize=True, quality=85)
        
        return filename
    return None

@main.route('/')
def index():
    boards = Board.query.all()
    
    # Get recent threads across all boards
    recent_threads = (Thread.query
        .order_by(Thread.created_at.desc())
        .limit(5)
        .all())
    
    # Get stats for each board
    board_stats = {}
    for board in boards:
        thread_count = Thread.query.filter_by(board_id=board.id).count()
        post_count = (Post.query
            .join(Thread)
            .filter(Thread.board_id == board.id)
            .count())
        last_post = (Post.query
            .join(Thread)
            .filter(Thread.board_id == board.id)
            .order_by(Post.created_at.desc())
            .first())
        
        board_stats[board.id] = {
            'threads': thread_count,
            'posts': post_count,
            'last_post': last_post
        }
    
    # Get total site stats
    total_stats = {
        'total_posts': Post.query.count() + Thread.query.count(),  # Threads count as posts too
        'total_images': (
            db.session.query(db.func.count(Thread.image_path))
            .filter(Thread.image_path.isnot(None))
            .scalar() +
            db.session.query(db.func.count(Post.image_path))
            .filter(Post.image_path.isnot(None))
            .scalar()
        )
    }
    
    return render_template('index.html', 
                         boards=boards, 
                         recent_threads=recent_threads,
                         board_stats=board_stats,
                         total_stats=total_stats)

@main.route('/<board_name>')
def board(board_name):
    board = Board.query.filter_by(name=board_name).first_or_404()
    threads = Thread.query.filter_by(board_id=board.id).order_by(Thread.created_at.desc()).all()
    boards = Board.query.all()  # Get all boards for the navigation
    return render_template('board.html', board=board, threads=threads, boards=boards)

@main.route('/<board_name>/thread/new', methods=['POST'])
@login_required
def new_thread(board_name):
    board = Board.query.filter_by(name=board_name).first_or_404()
    
    image_path = save_image(request.files.get('image'))
    
    thread = Thread(
        subject=request.form.get('subject'),
        content=request.form.get('content'),
        image_path=image_path,
        board_id=board.id,
        user_id=current_user.id
    )
    
    db.session.add(thread)
    db.session.commit()
    
    return redirect(url_for('main.thread', board_name=board_name, thread_id=thread.id))

@main.route('/<board_name>/thread/<int:thread_id>')
def thread(board_name, thread_id):
    board = Board.query.filter_by(name=board_name).first_or_404()
    thread = Thread.query.filter_by(id=thread_id, board_id=board.id).first_or_404()
    op_user = User.query.filter_by(id=thread.user_id).first_or_404()
    boards = Board.query.all()  # Get all boards for the navigation
    return render_template('thread.html', board=board, thread=thread, boards=boards, op_user=op_user)

@main.route('/<board_name>/thread/<int:thread_id>/reply', methods=['POST'])
@login_required
def reply(board_name, thread_id):
    thread = Thread.query.get_or_404(thread_id)
    
    image_path = save_image(request.files.get('image'))
    
    post = Post(
        content=request.form.get('content'),
        image_path=image_path,
        thread_id=thread.id
    )
    
    db.session.add(post)
    db.session.commit()
    
    return redirect(url_for('main.thread', board_name=board_name, thread_id=thread_id))

@main.route('/vote/<string:target_type>/<int:target_id>/<int:value>', methods=['POST'])
@login_required
def vote(target_type, target_id, value):
    if value not in [-1, 1]:
        return 'Invalid vote value', 400

    # Find existing vote
    if target_type == 'thread':
        existing_vote = Vote.query.filter_by(thread_id=target_id, user_id=current_user.id).first()
        target = Thread.query.get_or_404(target_id)
        new_vote = Vote(user_id=current_user.id, thread_id=target_id, value=value)
    elif target_type == 'post':
        existing_vote = Vote.query.filter_by(post_id=target_id, user_id=current_user.id).first()
        target = Post.query.get_or_404(target_id)
        new_vote = Vote(user_id=current_user.id, post_id=target_id, value=value)
    else:
        return 'Invalid target type', 400
    
    if existing_vote:
        if existing_vote.value == value:
            db.session.delete(existing_vote)  # Remove vote if same value clicked
        else:
            existing_vote.value = value  # Change vote if different value
    else:
        db.session.add(new_vote)
    
    db.session.commit()
    return str(target.score)
