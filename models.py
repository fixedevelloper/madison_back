from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, Boolean, Column, Double, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

db = SQLAlchemy()


class Fixture(db.Model):
    __tablename__ = 'fixtures'
    id = Column(Integer, primary_key=True)
    fixture_id = Column('fixture_id', Integer)
    referee = Column('referee', String(240))
    timezone = Column('timezone', String(200))
    timestamp = Column('timestamp', Numeric)
    date = Column('date', String(80))
    st_long = Column('st_long', String(32))
    st_short = Column('st_short', String(32))
    st_elapsed = Column('st_elapsed', String(32))
    league_id = Column('league_id', Integer)
    league_season = Column('league_season', Integer)
    league_round = Column('league_round', String(240))
    league_name = Column('league_name', String(240))
    team_home_id = Column('team_home_id', Integer)
    team_away_id = Column('team_away_id', Integer)
    team_away_winner = Column('team_away_winner', Boolean)
    team_home_winner = Column('team_home_winner', Boolean)
    team_home_name = Column('team_home_name', String(240))
    team_away_name = Column('team_away_name', String(240))
    team_home_logo = Column('team_home_logo', String(240))
    team_away_logo = Column('team_away_logo', String(240))
    goal_home = Column('goal_home', Integer, nullable=True)
    goal_away = Column('goal_away', Integer, nullable=True)
    score_ht_home = Column('score_ht_home', Integer, nullable=True)
    score_ht_away = Column('score_ht_away', Integer, nullable=True)
    score_ft_home = Column('score_ft_home', Integer, nullable=True)
    score_ft_away = Column('score_ft_away', Integer, nullable=True)
    score_ext_home = Column('score_ext_home', Integer, nullable=True)
    score_ext_away = Column('score_ext_away', Integer, nullable=True)
    score_pt_home = Column('score_pt_home', Integer, nullable=True)
    score_pt_away = Column('score_pt_away', Integer, nullable=True)
    prediction = relationship("Prediction", uselist=False, back_populates="fixture")

    def to_dict(self):
        return {
            'id': self.id,
            'fixture_id': self.fixture_id,
            'homeTeam': self.team_home_name,
            'awayTeam': self.team_away_name,
            'date': self.date,
            'homeTeamLogo': self.team_home_logo,
            'awayTeamLogo': self.team_away_logo,
            'homeScore': self.score_ft_home,
            'awayScore': self.score_ft_away,
            'competition': self.league_name
        }


class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    score_exact = Column('score_exact', JSON)
    fixture_id = Column('fixture_id', Integer, ForeignKey('fixtures.id'))
    fixture = relationship("Fixture", back_populates="prediction")
    goal_home = Column('goal_home', Integer)
    goal_away = Column('goal_away', Integer)
    probabity_home_win = Column('probabity_home_win', Double)
    probabity_away_win = Column('probabity_away_win', Double)
    probabity_draw = Column('probabity_draw', Double)
    twoteams_score = Column('twoteams_score', Boolean)
    mitemps_score = Column('mitemps_score', Boolean)
    probabity_homescore = Column('probabity_homescore', Double, default=0.0)
    probabity_awayscore = Column('probabity_awayscore', Double, default=0.0)
    resultStatus = Column('result_status', String(200))
    date = Column('date', String(80))

    def to_dict(self):
        return {

            'id': self.id,
            'fixture_id': self.fixture_id,
            'homeTeam': self.fixture.team_home_name,
            'awayTeam': self.fixture.team_away_name,
            'date': self.fixture.date,
            'homeTeamLogo': self.fixture.team_home_logo,
            'awayTeamLogo': self.fixture.team_away_logo,
            'homeScore': self.fixture.score_ft_home,
            'awayScore': self.fixture.score_ft_away,
            'competition': self.fixture.league_name,
            'pronostic1x2': {
                'goal_home': self.goal_home,
                'goal_away': self.goal_away,
                'probabity_home_win': self.probabity_home_win,
                'probabity_away_win': self.probabity_away_win,
                'probabity_draw': self.probabity_draw,
                'status': self.resultStatus,
            },
            'pronostic2teamscore': {
                'probabity_awayscore': self.probabity_awayscore,
                'probabity_homescore': self.probabity_homescore,
                'twoteams_score': self.twoteams_score,
            },
        }

class League(db.Model):
    __tablename__ = 'leagues'
    id = Column(Integer, primary_key=True)
    league_id = Column(Integer)
    name = Column(String(242))
    logo = Column(String(242))
    type = Column(String(242))
    countryName = Column(String(242))
    countryCode = Column(String(242))
    is_favorite = Column(Boolean)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'logo': self.logo,
            'type': self.type,
            'league_id': self.league_id,
            'countryCode': self.countryCode,
            'countryName': self.countryName,

        }