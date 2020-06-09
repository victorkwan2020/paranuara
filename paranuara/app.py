from flask import Flask, Response, jsonify
from werkzeug.exceptions import HTTPException
import logging
import os
import json

from .db import initialize_db
from . import people_info as pi

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost/testdb")
app.config['MONGODB_SETTINGS'] = {'host': MONGODB_URI,
                                  'connect': False
                                  }
app.config["JSON_SORT_KEYS"] = False


def handle_httpexception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name
    })
    response.content_type = "application/json"
    return response


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return handle_httpexception(e)
    app.logger.error(e)
    resp = json.dumps({'Internal Error': str(e)})
    return Response(resp, status=500, mimetype='application/json')


@app.route('/alive')
def alive():
    return 'Alive', 200


@app.route('/people/<index1>/common_friends_with/<index2>')
def common_friends(index1, index2):
    resp = pi.common_friends_alive_brown_eyes(index1, index2)
    return jsonify(resp)


@app.route('/people/<index>/favourite_food')
def handle_favourite_food(index):
    resp = pi.get_favourite_food(index)
    return jsonify(resp)


@app.route('/company/<index>/employees')
def handle_get_company_employee(index):
    resp = pi.get_employees_from_company(index)
    return jsonify(resp)


if __name__ == '__main__':
    initialize_db(app)
    app.run(host="0.0.0.0",port=27016)
