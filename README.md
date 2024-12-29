# Yusen Imageboard

A lightweight imageboard built with Flask, JINJA2 and SQLite.

## Features

- A clean and modern interface
- Multiple boards with unique topics
- Thread creation with image support
- Reply functionality with optional images
- Automatic image optimization
- Mobile-responsive design
- Activity statistics and recent posts tracking

## Tech Stack

- **Backend**: Flask, JINJA2 (For HTML templating)
- **Database**: SQLite with SQLAlchemy
- **Image Processing**: Pillow
- **Frontend**: HTML5, CSS3

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python run.py
```

The server will start at `http://127.0.0.1:5000`.
The SQLite database will be automatically created and initialized with default boards.
If an `app.db` file is found, then this file will be used instead of creating a new db.

## Project Structure

```
imageboard/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── routes.py            # Route handlers
│   ├── static/
│   │   ├── css/             # Stylesheets
│   │   └── uploads/         # User uploaded images
│   └── templates/           # Jinja2 templates
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
└── run.py                   # Application entry point
```

## Notes

- SQLite is part of the python standard library, and as such does not need to be installed separately.
  Database creation and configuration happens in `run.py`. DB interaction happens through the python package `SQLAlchemy`.
- Image uploads are automatically optimized using `pillow` and stored in `app/static/uploads/`.
- Flask debug mode is enabled by default in development.
- Default maximum file size for uploads is 16MB.
- Images are automatically resized to max dimensions of 2000x2000 pixels.
