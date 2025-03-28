from models import db, BlackListedEmail
from sqlalchemy.exc import SQLAlchemyError

def addBlacklistEmail(email_data, ip_address):
  try:
    record = BlackListedEmail(
      email = email_data['email'],
      appId = email_data['appId'],
      reason = email_data['reason'],
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
  
  