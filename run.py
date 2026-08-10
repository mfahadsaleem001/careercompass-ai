import os
from app import create_app
from app.extensions import db

app = create_app(
    os.environ.get(
        'FLASK_ENV',
        'production' if os.environ.get('VERCEL') == '1' else 'development'
    )
)

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', True))