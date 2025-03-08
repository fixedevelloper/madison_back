import os

class Config:
    base_url = os.getenv("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = base_url  # Utiliser SQLite pour commencer
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_FOOT='dfd41df72fmsh420e0852071496cp12d2cajsn9a365373ca59'
    URL_FOOT='https://api-football-v1.p.rapidapi.com/v3/'