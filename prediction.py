import os
from datetime import datetime, timedelta
from decimal import Decimal
from dotenv import load_dotenv
import flask
import numpy as np
import pandas as pd
from sqlalchemy import func, or_
from config import Config
from models import Fixture, Prediction,db
from scipy.stats import poisson
load_dotenv()
app = flask.Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db.init_app(app)


def team_scoring_prediction(fixture:Fixture):
     #try: 
      average_homeH=db.session.query(func.avg(Fixture.goal_home)).filter(or_(Fixture.team_away_id==fixture.team_home_id, Fixture.team_home_id==fixture.team_home_id,Fixture.st_short=='FT')).order_by(Fixture.date).scalar() or 0.0
      average_homeA=db.session.query(func.avg(Fixture.goal_away)).filter(or_(Fixture.team_away_id==fixture.team_home_id, Fixture.team_home_id==fixture.team_home_id,Fixture.st_short=='FT')).order_by(Fixture.date).scalar() or 0.0
      average_home=(Decimal(average_homeA)+Decimal(average_homeH))/2
      #average_is_home=db.session.query(func.avg(Fixture.goal_home)).filter_by(team_home_id=fixture.team_home_id).order_by(Fixture.date).scalar()

      average_home_concededH=db.session.query(func.avg(Fixture.goal_away)).filter_by(team_home_id=fixture.team_home_id,st_short='FT').order_by(Fixture.date).scalar()or 0.0
      average_home_concededA=db.session.query(func.avg(Fixture.goal_home)).filter_by(team_away_id=fixture.team_home_id,st_short='FT').order_by(Fixture.date).scalar() or 0.0
      average_home_conceded=(Decimal(average_home_concededH)+Decimal(average_home_concededA))/2
#####################################################################################################################

      average_awayH=db.session.query(func.avg(Fixture.goal_home)).filter(or_(Fixture.team_away_id==fixture.team_away_id, Fixture.team_home_id==fixture.team_away_id),Fixture.st_short=='FT').order_by(Fixture.date).scalar() or 0.0
      average_awayA=db.session.query(func.avg(Fixture.goal_away)).filter(or_(Fixture.team_away_id==fixture.team_away_id, Fixture.team_home_id==fixture.team_away_id),Fixture.st_short=='FT').order_by(Fixture.date).scalar() or 0.0
      average_away=(Decimal(average_awayH)+Decimal(average_awayA))/2
      #average_is_away=db.session.query(func.avg(Fixture.goal_away)).filter_by(team_away_id=fixture.team_away_id).order_by(Fixture.date).scalar()

      average_away_concededH=db.session.query(func.avg(Fixture.goal_away)).filter_by(team_home_id=fixture.team_away_id,st_short='FT').order_by(Fixture.date).scalar() or 0.0
      average_away_concededA=db.session.query(func.avg(Fixture.goal_home)).filter_by(team_away_id=fixture.team_away_id,st_short='FT').order_by(Fixture.date).scalar() or 0.0
      average_away_conceded=((Decimal(average_away_concededH)+Decimal(average_away_concededA))/2)
      if average_home>0.0 and average_away>0.0 and average_away_conceded>0.0 and average_home_conceded>0.0:
            
        #######################################################
        home_team_att_strength = (Decimal(average_homeH) / Decimal(average_home)).quantize(Decimal('0.01'))
        print("Home team attacking strength: " + str(home_team_att_strength))
        #Home team defensive strength 
        home_team_def_strength = (Decimal(average_home_concededH)/ Decimal(average_home_conceded)).quantize(Decimal('0.01'))
        print("Home team defensive strength: " + str(home_team_def_strength))
        #Away goals scored by away team and mean
        
        
        #Away team attacking strength 
        away_team_att_strength = (Decimal(average_awayA)/ Decimal(average_away)).quantize(Decimal('0.01'))
        print("Away team attacking strength: " + str(away_team_att_strength))
        
        #Away team defensive strength
        away_team_def_strength = (Decimal(average_away_concededA)/ Decimal(average_away_conceded)).quantize(Decimal('0.01'))
        print("Away team defensive strength: " + str(away_team_def_strength))
        
        #Home team scoring strength
        home_team_goal_exp = (home_team_att_strength * away_team_def_strength * average_home).quantize(Decimal('0.01'))
        #home_team_goal_exp = (home_team_att_strength * away_team_def_strength).round(2)
        print("Home team goal expectance: "+ str(home_team_goal_exp))
        #Away team scoring strength
        away_team_goal_exp = (away_team_att_strength * home_team_def_strength * average_away).quantize(Decimal('0.01'))
        #away_team_goal_exp = (away_team_att_strength * home_team_def_strength).round(2)
        print("Away team goal expectance: " + str(away_team_goal_exp))
        return home_team_goal_exp, away_team_goal_exp
     #except:
        #print(fixture.fixture_id) 
def goal_prob(n,team_poission):
    goals,prob = 0,0
    for i in range(0, 10000):
        if team_poission[i] == n:
            goals = goals+1
            prob = goals/ 10000     
    return prob, goals
def printDiagonalSums(mat, n):
 
    principal = 0
    secondary = 0;
    for i in range(0, n):
        for j in range(0, n):
 
            # Condition for principal diagonal
            if (i == j):
                principal += mat[i][j]
 
            # Condition for secondary diagonal
            if (i + j) == (n - 1):
                secondary += mat[i][j]
         
    return principal
def prediction(date_prediction):
    print(date_prediction)
    start_date = datetime.strptime(date_prediction+ ' 00:00:00', "%Y-%m-%d %H:%M:%S")
    start_1=start_date + timedelta(days=1)
    end_date = start_1
    with app.app_context():

      fixtures=Fixture.query.filter(Fixture.date.between(start_date,end_date))
      for f in fixtures:
          result = team_scoring_prediction(f)
          if result is None:
            home_team_goal, away_team_goal=0,0
            print("The function returned None.")
            print(result)
          else:
            home_team_goal, away_team_goal= result  # Safe unpacking
          #home_team_goal, away_team_goal = team_scoring_prediction(f)
            print(home_team_goal)
            home_team_poission = poisson.rvs(float(home_team_goal), size=100000)
            away_team_poission = poisson.rvs(float(away_team_goal), size=100000)

            home_0, g = goal_prob(0,home_team_poission)
            print(home_0, g)

            home_1, g = goal_prob(1,home_team_poission)
            print(home_1, g)

            home_2, g = goal_prob(2,home_team_poission)
            print(home_2, g)

            home_3, g = goal_prob(3,home_team_poission)
            print(home_3, g)

            home_4, g =goal_prob(4,home_team_poission)
            print(home_4, g)

            home_5, g =goal_prob(5,home_team_poission)
            print(home_5, g)
        ####################################
            away_0, g = goal_prob(0,away_team_poission)
            print(away_0, g)

            away_1, g = goal_prob(1,away_team_poission)
            print(away_1, g)

            away_2, g = goal_prob(2,away_team_poission)
            print(away_2, g)

            away_3, g = goal_prob(3,away_team_poission)
            print(away_3, g)

            away_4, g = goal_prob(4,away_team_poission)
            print(away_4, g)

            away_5, g = goal_prob(5,away_team_poission)
            print(away_5, g)
            home_chance = [home_0, home_1, home_2, home_3, home_4, home_5]
            home_chance_frame = pd.DataFrame(home_chance, columns=['Probs'])
            home_chance_frame = home_chance_frame
            home_chance_frame


            away_chance= [away_0, away_1, away_2, away_3, away_4, away_5]
            away_chance_frame = pd.DataFrame(away_chance, columns=['Probs'])
            away_chance_frame = away_chance_frame
            away_chance_frame

            df_cross = home_chance_frame.dot(away_chance_frame.T)
            df_cross = df_cross.round(3)
            principal = printDiagonalSums(df_cross, 5)
            print(principal)

            df_cross_up = df_cross.where(np.triu(np.ones(df_cross.shape)).astype(np.bool))
            print(df_cross_up)
            draw = principal

            home_team_win = df_cross.sum().sum() - df_cross_up.sum().sum()
            away_team_win = df_cross_up.sum().sum() - principal


            print("machineball home win chance: " + str(np.round(home_team_win, 3)*100))
            print("machineball draw chance: " + str(np.round(draw, 3)*100))
            print("machineball away chance: " + str(np.round(away_team_win, 3)*100))

            print("machineball total chance: " + str(np.round(home_team_win, 3)*100 + np.round(draw, 3)*100 + np.round(away_team_win, 3)*100))

            prediction=Prediction.query.filter_by(fixture_id=f.id).first()
            if not prediction:
                prediction=Prediction()
                prediction.fixture_id=f.id
            prediction.goal_home=round(home_team_goal)
            prediction.goal_away=round(away_team_goal)
            prediction.probabity_home_win=round(np.round(home_team_win, 3)*100)
            prediction.probabity_away_win=round(np.round(away_team_win, 3)*100)
            prediction.probabity_draw=round(np.round(draw, 3)*100)
            prediction.date=f.date
            db.session.add(prediction)
            db.session.commit()
            #db.session.close()

dates=[datetime.now(), datetime.now() + timedelta(days=1)]
for date in dates:
    prediction(date.strftime("%Y-%m-%d"))
