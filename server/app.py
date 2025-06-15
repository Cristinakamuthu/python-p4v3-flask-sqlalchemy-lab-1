#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(jsonify(body), 200)


@app.route('/earthquakes/<int:id>')
def get_earthquakes(id):
    quake = Earthquake.query.get(id)

    if quake:
        response_body = {
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }
        return make_response(jsonify(response_body), 200)

    return make_response(jsonify({"message": f"Earthquake {id} not found."}), 404)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    magnites = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    results = []
    for magnite in magnites:
        results.append({
            "id": magnite.id,
            "location": magnite.location,
            "magnitude": magnite.magnitude,
            "year": magnite.year
        })

    response_body = {
        "count": len(results),
        "quakes": results
    }

    return make_response(jsonify(response_body), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
