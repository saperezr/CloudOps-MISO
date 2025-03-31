from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from config import Config
from blueprints import main, blacklists

jwt = JWTManager()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  
  db.init_app(app)
  jwt.init_app(app)  
  
  with app.app_context():
    db.create_all()
 
  app.register_blueprint(main)
  app.register_blueprint(blacklists)

  return app