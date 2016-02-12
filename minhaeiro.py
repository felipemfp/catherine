from flask import Flask, json
from models import db
import routes

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)

db.init_app(app)
routes.init_app(app)


@app.errorhandler(405)
def not_allowed(error):
    return json.jsonify({'error': str(error)}), 405


@app.errorhandler(404)
def not_found(error):
    return json.jsonify({'error': str(error)}), 404


@app.route('/api/')
def api():
    return '<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>'


if __name__ == '__main__':
    app.run()
