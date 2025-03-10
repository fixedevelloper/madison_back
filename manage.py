from datetime import datetime, timedelta

dates=[datetime.now(),datetime.now()-timedelta(days=1)]
for date in dates:
    print(date.strftime("%Y-%m-%d"))

#/www/wwwroot/madisonapi.creativsoftcm.com/6464f9c7948b7ebb0f21ecf83d84aa8f_venv/bin/python3 apifootball.py
#/www/wwwroot/madisonapi.creativsoftcm.com/6464f9c7948b7ebb0f21ecf83d84aa8f_venv/bin/python3 prediction.py
# cd /www/wwwroot/madisonapi.creativsoftcm.com/ && 6464f9c7948b7ebb0f21ecf83d84aa8f_venv/bin/python3 updatefootball.py
#/www/wwwroot/madisonapi.creativsoftcm.com/6464f9c7948b7ebb0f21ecf83d84aa8f_venv/bin/python3 /www/wwwroot/madisonapi.creativsoftcm.com/prediction.py