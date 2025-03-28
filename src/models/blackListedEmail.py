from datetime import datetime, timezone
from marshmallow import Schema, fields
from sqlalchemy.dialects.postgresql import UUID
from models import db

class BlackListedEmail(db.Model):
  __tablename__ = 'BlackListedEmails'
  
  email = db.Column(db.String(120), primary_key=True)
  appId = db.Column(UUID(as_uuid=True), nullable=False)
  reason = db.Column(db.String(255))
  ipAddress = db.Column(db.String(39))
  createdOn = db.Column(db.DateTime, default=datetime.now(timezone.utc))
  
  
class BlackListedEmailSchema(Schema):
  email = fields.Str()
  appId = fields.UUID()
  reason = fields.Str()
  ipAddress = fields.Str()
  createdOn = fields.DateTime()
    
    
blacklisted_email_schema = BlackListedEmailSchema()