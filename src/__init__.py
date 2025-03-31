from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from models import db
from config import Config

jwt = JWTManager()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  
  db.init_app(app)
  jwt.init_app(app)  
  
  with app.app_context():
    db.create_all()

  from blueprints import main
  app.register_blueprint(main)

  from errors.errors import ApiError
  @app.errorhandler(ApiError)
  def handle_exception(err):
      response = {
          "msg": err.description,
      }
      return jsonify(response), err.code

  return app