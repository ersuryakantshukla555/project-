import os

# Vercel's Python runtime expects a WSGI-compatible 'app' variable.
# We import the Flask app from the project root app.py
from app import app as flask_app
from app import db

# Ensure DB file path is writable in serverless by redirecting sqlite file into /tmp when needed
if flask_app.config.get('SQLALCHEMY_DATABASE_URI', '').startswith('sqlite:///'):
    db_uri = flask_app.config['SQLALCHEMY_DATABASE_URI']
    path = db_uri.replace('sqlite:///','')
    # If path is relative and not writable, move to /tmp
    if not os.path.isabs(path):
        abs_path = os.path.join(os.getcwd(), path)
    else:
        abs_path = path
    try:
        os.makedirs(os.path.dirname(abs_path) or '.', exist_ok=True)
        test_path = os.path.join(os.path.dirname(abs_path) or '.', '.write_test')
        with open(test_path, 'w') as f:
            f.write('ok')
        os.remove(test_path)
    except Exception:
        tmp_db = os.path.join('/tmp', os.path.basename(path))
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{tmp_db}'

with flask_app.app_context():
    try:
        db.create_all()
    except Exception:
        # Ignore if DB is read-only or unreachable in serverless cold start
        pass

app = flask_app

