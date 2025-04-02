from models import db, BlackListedEmail
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import MissingFieldsError, InvalidUUIDError, InvalidSearchFieldsError, ApiError, InvalidReasonFieldsError
import re
import uuid

def addBlacklistEmail(email_data, ip_address):
  email = email_data.get('email')
  app_id = email_data.get('appId')
  reason = email_data.get('reason')

  if not email or not app_id:
    raise MissingFieldsError

  email_regex = r"[^@]+@[^@]+\.[^@]+"
  if not re.match(email_regex, email):
    raise InvalidSearchFieldsError

  try:
    uuid.UUID(str(app_id))
  except ValueError:
    raise InvalidUUIDError

  if reason and len(reason) > 255:
    raise InvalidReasonFieldsError

  try:
    record = BlackListedEmail(
      email = email_data['email'],
      appId = email_data['app_uuid'],
      reason = email_data['blocked_reason'],
      ipAddress = ip_address
    )
    
    db.session.add(record)
    db.session.commit()
    
    return record
  except SQLAlchemyError as e:
    db.session.rollback()
    return None
  
  except KeyError as e:
    return None


def getEmailFromBlacklist(email):
  if not email:
    return None

  return BlackListedEmail.query.filter_by(email = email).first()

