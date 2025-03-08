import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate  # Importer Migrate
from models import db
from config import Config
from routes import bp as routes_bp
load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] =  os.getenv("DATABASE_URL")
CORS(app, resources={r"/*": {"origins": "http://162.19.154.218:6200"}})
db.init_app(app)

migrate = Migrate(app, db)  # Initialiser Migrate avec l'application et la base de données

app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run(debug=True)