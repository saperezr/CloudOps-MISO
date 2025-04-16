import os
import sys
import unittest
from unittest.mock import MagicMock, patch
from flask import Flask

# Asegurarse de que el directorio src esté en el path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mock para la base de datos
class MockDB:
    def __init__(self):
        self.session = MagicMock()
        self.session.add = MagicMock()
        self.session.commit = MagicMock()
        self.session.rollback = MagicMock()
        self.session.query = MagicMock()

# Mock para el modelo BlackListedEmail
class MockBlackListedEmail:
    def __init__(self, email, appId, reason=None, ipAddress=None):
        self.email = email
        self.appId = appId
        self.reason = reason
        self.ipAddress = ipAddress
        self.createdOn = None

# Aplicar los mocks globalmente
def apply_mocks():

    mock_db = MockDB()
    patch('models.db', mock_db).start()
    
    patch('models.BlackListedEmail', MockBlackListedEmail).start()
    
    patch('flask_jwt_extended.create_access_token', lambda identity, expires_delta: "mock.jwt.token").start()
    patch('flask_jwt_extended.jwt_required', lambda f: f).start()

apply_mocks()

app_context = app.app_context()
app_context.push() 