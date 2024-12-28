import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from app.models import db, Board, Thread, Post
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
    return render_template('index.html', boards=boards)


@main.route('/<board_name>')
def board(board_name):
    board = Board.query.filter_by(name=board_name).first_or_404()
    threads = Thread.query.filter_by(board_id=board.id).order_by(Thread.created_at.desc()).all()
    boards = Board.query.all()  # Get all boards for the navigation
    return render_template('board.html', board=board, threads=threads, boards=boards)


@main.route('/<board_name>/thread/new', methods=['POST'])
def new_thread(board_name):
    board = Board.query.filter_by(name=board_name).first_or_404()

    image_path = save_image(request.files.get('image'))

    thread = Thread(
        subject=request.form.get('subject'),
        content=request.form.get('content'),
        image_path=image_path,
        board_id=board.id
    )

    db.session.add(thread)
    db.session.commit()

    return redirect(url_for('main.thread', board_name=board_name, thread_id=thread.id))


@main.route('/<board_name>/thread/<int:thread_id>')
def thread(board_name, thread_id):
    boards = Board.query.all()
    board = Board.query.filter_by(name=board_name).first_or_404()
    thread = Thread.query.filter_by(id=thread_id, board_id=board.id).first_or_404()
    return render_template('thread.html', board=board, boards=boards, thread=thread)


@main.route('/<board_name>/thread/<int:thread_id>/reply', methods=['POST'])
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
