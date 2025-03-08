from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from sqlalchemy import alias
from sqlalchemy.orm import aliased

from models import Prediction, db, Fixture, League

bp = Blueprint('routes', __name__)


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = Fixture(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id}), 201


@bp.route('/fixtures', methods=['GET'])
def get_fixtures():
    now = datetime.now()
    date = request.args.get('date', now.strftime("%Y-%m-%d %H:%M:%S"))
    league=request.args.get('league')
    start_date = datetime.strptime(date + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
    start_1 = start_date + timedelta(days=1)
    end_date = start_1
    if league is not None:
        a1=aliased(Fixture)
        predictions = Prediction.query.join(a1,Prediction.fixture).filter(Prediction.date.between(start_date, end_date),a1.league_id == league).all()
    else:
        predictions = Prediction.query.filter(Prediction.date.between(start_date, end_date))
    return jsonify([f.to_dict() for f in predictions])


@bp.route('/fixtures/<int:id>', methods=['GET'])
def get_fixture(id):
    fixture = Prediction.query.get(id)
    if fixture:
        return jsonify(fixture.to_dict())
    return jsonify({'message': 'Fixture not found'}), 404
@bp.route('/leagues', methods=['GET'])
def getTopLeague ():
    leagues=League.query.filter_by(is_favorite=True).all()
    return jsonify([l.to_dict() for l in leagues])
@bp.route('/leagues/<string:name>', methods=['GET'])
def getLeagueByName(name):
    leagues = League.query.filter_by(countryName=name).all()
    return jsonify([l.to_dict() for l in leagues])