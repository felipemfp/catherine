import sys
from flask import Flask, json
from models import db
from apis import InvalidUsage
import routes

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)

db.init_app(app)
routes.init_app(app)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return json.jsonify({'error': str(error)}), error.status_code

@app.errorhandler(405)
def handle_not_allowed(error):
    return json.jsonify({'error': str(error)}), 405


@app.errorhandler(404)
def handle_not_found(error):
    return json.jsonify({'error': str(error)}), 404


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else 'run'
    if command == 'run':
        app.run()
    elif command == 'migrate':
        db.create_all(app=app)
