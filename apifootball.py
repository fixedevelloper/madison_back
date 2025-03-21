from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import flask
import pandas as pd
import requests

from config import Config
from models import Fixture, db, League

load_dotenv()
app = flask.Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

api_key = os.getenv("API_FOOT")
base_url = os.getenv("URL_FOOT")

headers = {
    'x-rapidapi-key': api_key,
    'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
}


def load_fixture(date_match):
    response = requests.get(base_url + f'fixtures?date='+date_match, headers=headers)
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        data = response.json()
        # Vous pouvez maintenant convertir cela en DataFrame
        fixtures = data['response']  # Supposons que les données des matches sont sous la clé 'response'

        # Créer le DataFrame
        df = pd.DataFrame(fixtures)

        # Afficher les premières lignes
        with app.app_context():
            for index, row in df.iterrows():
                fixture = Fixture.query.filter_by(fixture_id=row['fixture']['id']).first()
                if fixture:
                    fixture.fixture_id = row['fixture']['id']
                else:
                    fixture = Fixture()
                print(str.split(row['fixture']['date'], 'T')[0])
                fixture.date = row['fixture']['date']
                fixture.fixture_id = row['fixture']['id']
                fixture.goal_away = row['goals']['away']
                fixture.goal_home = row['goals']['home']
                fixture.referee = row['fixture']['referee']
                fixture.timezone = row['fixture']['timezone']
                fixture.timestamp = row['fixture']['timestamp']
                fixture.st_elapsed = row['fixture']['status']['elapsed']
                fixture.st_long = row['fixture']['status']['long']
                fixture.st_short = row['fixture']['status']['short']
                fixture.league_id = row['league']['id']
                fixture.league_round = row['league']['round']
                fixture.league_season = row['league']['season']
                fixture.league_name = row['league']['name']
                fixture.team_away_id = row['teams']['away']['id']
                fixture.team_away_winner = row['teams']['away']['winner']
                fixture.team_home_id = row['teams']['home']['id']
                fixture.team_home_winner = row['teams']['home']['winner']
                fixture.team_away_name = row['teams']['away']['name']
                fixture.team_home_name = row['teams']['home']['name']
                fixture.score_ext_away = row['score']['extratime']['away']
                fixture.score_ext_home = row['score']['extratime']['home']
                fixture.score_ft_away = row['score']['fulltime']['away']
                fixture.score_ft_home = row['score']['fulltime']['home']
                fixture.score_ht_away = row['score']['halftime']['away']
                fixture.score_ht_home = row['score']['halftime']['home']
                fixture.score_pt_away = row['score']['penalty']['away']
                fixture.score_pt_home = row['score']['penalty']['home']
                fixture.team_away_logo = row['teams']['away']['logo']
                fixture.team_home_logo = row['teams']['home']['logo']
                print(fixture)
                db.session.add(fixture)
                prediction = fixture.prediction;
                if prediction and fixture.st_short == 'FT':
                    if fixture.score_ft_away > fixture.score_ft_home and prediction.goal_away > prediction.goal_home:
                        prediction.resultStatus = 'success'
                    elif fixture.score_ft_away < fixture.score_ft_home and prediction.goal_away < prediction.goal_home:
                        prediction.resultStatus = 'success'
                    elif fixture.score_ft_away == fixture.score_ft_home and prediction.goal_away == prediction.goal_home:
                        prediction.resultStatus = 'success'
                    else:
                        prediction.resultStatus = 'fail'
                    db.session.commit()
                db.session.commit()
                db.session.close()
    else:
        print(f"Erreur lors de la récupération des données: {response}")


def load_league():
    response_leaugues = requests.get(base_url + 'leagues', headers=headers)
    if response_leaugues.status_code == 200:
        data = response_leaugues.json()
        leagues = data['response']
        df = pd.DataFrame(leagues)
        print(df)
        with app.app_context():
            for index, row in df.iterrows():
                league = League.query.filter_by(league_id=row['league']['id']).first()
                if league:
                    league.league_id = row['league']['id']
                else:
                    print(str.split(row['league']['name'], 'T')[0])
                    league = League()
                league.league_id = row['league']['id']
                league.name = row['league']['name']
                league.logo = row['league']['logo']
                league.type = row['league']['type']
                league.countryName = row['country']['name']
                league.countryCode = row['country']['code']
                db.session.add(league)
            db.session.commit()

dates=[datetime.now(), datetime.now() + timedelta(days=1)]
for date in dates:
    load_fixture(date.strftime("%Y-%m-%d"))
#load_league()
