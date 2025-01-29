from app import create_app, db
from app.models import Board

app = create_app()

def init_db():
    with app.app_context():
        # Create initial boards if they don't exist
        if Board.query.count() == 0:
            boards = [
                Board(name='random', description='Random Discussion'),
                Board(name='tech', description='Technology'),
                Board(name='music', description='Music Discussion'),
            ]
            for board in boards:
                db.session.add(board)
            db.session.commit()

if __name__ == '__main__':
    init_db()  # Initialize the database with some boards
    app.run(debug=True)