import unittest
from unittest.mock import patch, MagicMock
import json
import uuid
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from blueprints.routes import main, blacklists
from errors.errors import ApiError
from models import db
from config import Config

class TestRoutes(unittest.TestCase):
    def setUp(self):
        # Crear una aplicación Flask para pruebas
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Configuración de JWT
        self.app.config['JWT_SECRET_KEY'] = 'test-key'
        self.app.config['JWT_TOKEN_LOCATION'] = ['headers']
        JWTManager(self.app)
        
        # base de datos
        db.init_app(self.app)
        
        self.app.register_blueprint(main)
        self.app.register_blueprint(blacklists)
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        with self.app.app_context():
            db.create_all()
        
        # Datos de prueba
        self.test_data = {
            'email': 'test@example.com',
            'app_uuid': str(uuid.uuid4()),
            'blocked_reason': 'Test reason'
        }
        
        # Crear un token JWT real para las pruebas
        with self.app.app_context():
            self.mock_token = create_access_token(identity="testuser")
        
        # Mock para el servicio de blacklist
        self.mock_blacklisted_email = {
            'email': 'test@example.com',
            'appId': str(uuid.uuid4()),
            'reason': 'Test reason',
            'ipAddress': '127.0.0.1',
            'createdOn': '2024-03-19T00:00:00Z'
        }

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    def test_get_token(self):
        response = self.app.test_client().post('/token')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.get_json())

    def test_add_email_to_blacklist_success(self):
        # Mock para addBlacklistEmail
        with patch('blueprints.routes.addBlacklistEmail', return_value=self.mock_blacklisted_email) as mock_add:

            headers = {'Authorization': f'Bearer {self.mock_token}'}
            response = self.app.test_client().post('/blacklists/', json=self.test_data, headers=headers)

            mock_add.assert_called_once()
            args = mock_add.call_args[0]
            self.assertEqual(args[0], self.test_data)
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['msg'], "El email fue agregado existosamente.")

    def test_add_email_to_blacklist_error(self):
        # Mock para addBlacklistEmail que retorna None
        with patch('blueprints.routes.addBlacklistEmail', return_value=None) as mock_add:

            headers = {'Authorization': f'Bearer {self.mock_token}'}
            response = self.app.test_client().post('/blacklists/', json=self.test_data, headers=headers)

            mock_add.assert_called_once()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['msg'], "El email fue agregado existosamente.")

    def test_get_email_info_found(self):
        # Mock para getEmailFromBlacklist
        with patch('blueprints.routes.getEmailFromBlacklist', return_value=self.mock_blacklisted_email) as mock_get:

            headers = {'Authorization': f'Bearer {self.mock_token}'}
            response = self.app.test_client().get('/blacklists/test@example.com', headers=headers)
            
            mock_get.assert_called_once_with('test@example.com')
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data['blacklisted'])

    def test_get_email_info_not_found(self):
        # Mock para getEmailFromBlacklist
        with patch('blueprints.routes.getEmailFromBlacklist', return_value=None) as mock_get:
           
            headers = {'Authorization': f'Bearer {self.mock_token}'}
            response = self.app.test_client().get('/blacklists/test@example.com', headers=headers)
            
            mock_get.assert_called_once_with('test@example.com')
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertFalse(data['blacklisted'])

    def test_ping(self):
        
        response = self.app.test_client().get('/ping')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['msg'], "Solo para confirmar que el servicio está arriba.")

if __name__ == '__main__':
    unittest.main() 