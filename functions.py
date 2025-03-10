from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import flask
from sqlalchemy import desc
from sqlalchemy.dialects.mysql import match

from models import db, Fixture

load_dotenv()
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
league_sesson=2025
class Team:
    def __init__(self, name):
        self.name = name
        self.matches_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_scored = 0
        self.goals_conceded = 0
        self.points = 0

    def add_match(self, scored, conceded):
        self.matches_played += 1
        self.goals_scored += scored
        self.goals_conceded += conceded

        if scored > conceded:
            self.wins += 1
            self.points += 3
        elif scored < conceded:
            self.losses += 1
        else:
            self.draws += 1
            self.points += 1

    def goal_difference(self):
        return self.goals_scored - self.goals_conceded

def print_standings(teams):
    print("Classement de la ligue:")
    teams.sort(key=lambda t: (t.points, t.goal_difference(), t.goals_scored), reverse=True)

    print(f"{'Position':<10} {'Équipe':<20} {'Points':<10} {'Différence de buts':<20} {'Buts marqués':<15} {'Match joues':<15}")
    for position, team in enumerate(teams, start=1):
        print(f"{position:<10} {team.name:<20} {team.points:<10} {team.goal_difference():<20} {team.goals_scored:<15} {team.matches_played:<15}")

# Connexion à la base de données




# Afficher le classement

def standing_team(league_id,league_sesson):
    with (app.app_context()):
        # Récupérer les résultats des matches
        fixtures = db.session.query(Fixture).filter(Fixture.league_id == league_id,Fixture.league_season==league_sesson,Fixture.st_short=='FT').all()

        teams_dict = {}

        # Traiter les résultats des matches
        for match in fixtures:
            team_home_name=match.team_home_name
            team_away_name=match.team_away_name
            score_ft_home=match.goal_home
            score_ft_away = match.goal_away

            # Créer les équipes si elles n'existent pas déjà
            if team_home_name not in teams_dict:
                teams_dict[team_home_name] = Team(team_home_name)
            if team_away_name not in teams_dict:
                teams_dict[team_away_name] = Team(team_away_name)

            # Ajouter les résultats des matches
            teams_dict[team_home_name].add_match(score_ft_home, score_ft_away)
            teams_dict[team_away_name].add_match(score_ft_away, score_ft_home)
        return teams_dict
def get_team_stats(team_name,league_id,league_sesson):
    with (app.app_context()):
        # Récupérer les 5 derniers matchs de l'équipe
        matches = db.session.query(Fixture).filter(Fixture.league_id == league_id, Fixture.league_season == league_sesson,
                                                    Fixture.st_short == 'FT',(Fixture.team_home_name == team_name) | (Fixture.team_away_name == team_name)).order_by(desc(Fixture.fixture_id)).limit(5).all()

        stats = {
            'matches_played': 0,
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'goals_scored': 0,
            'goals_conceded': 0,
        }

        for match in matches:
            stats['matches_played'] += 1
            if match.team_home_name == team_name:
                stats['goals_scored'] += match.goal_home
                stats['goals_conceded'] += match.goal_away
                if match.goal_home > match.goal_away:
                    stats['wins'] += 1
                elif match.goal_home < match.goal_away:
                    stats['losses'] += 1
                else:
                    stats['draws'] += 1
            else:
                stats['goals_scored'] += match.goal_away
                stats['goals_conceded'] += match.goal_home
                if match.goal_away > match.goal_home:
                    stats['wins'] += 1
                elif match.goal_away < match.goal_home:
                    stats['losses'] += 1
                else:
                    stats['draws'] += 1

        return stats
#print_standings(list(standing_team(39,2020).values()))
#team_name = "Real Madrid"
#team_stats = get_team_stats(team_name,140,2020)

# Afficher les statistiques
# print(f"Statistiques pour l'équipe {team_name}:")
# print(f"Matchs joués : {team_stats['matches_played']}")
# print(f"Gagnés : {team_stats['wins']}")
# print(f"Nuls : {team_stats['draws']}")
# print(f"Perdus : {team_stats['losses']}")
# print(f"Buts marqués : {team_stats['goals_scored']}")
# print(f"Buts encaissés : {team_stats['goals_conceded']}")
