import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from services import addBlacklistEmail, getEmailFromBlacklist
from errors.errors import ApiError

main = Blueprint("main", __name__, url_prefix='/blacklists')


@main.route("/ping", methods=(['GET']))
def ping():
  return {"msg": "Solo para confirmar que el servicio está arriba."}, 200


@main.route("/token", methods=["GET"])
def get_token():
  JWT_TOKEN = create_access_token(
    identity="testuser",
    expires_delta=datetime.timedelta(days=7)
  )
  
  return jsonify({"token": JWT_TOKEN})


@main.route("/", methods=(['POST']))
@jwt_required()
def addEmailToBlacklist():
  try:
    data = request.get_json()
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    result = addBlacklistEmail(data, ip_address)
    return jsonify({"msg": "El email fue agregado existosamente."}), 200
  except ApiError as err:
    return jsonify({"msg": err.description}), err.code

@main.route("/<string:email>", methods=(['GET']))
@jwt_required()
def getEmailInfo(email):
  result = getEmailFromBlacklist(email)
  
  return jsonify({"blacklisted": result is not None}), 200
