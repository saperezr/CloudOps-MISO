import unittest
from unittest.mock import patch, MagicMock
import uuid
from services.services import addBlacklistEmail, getEmailFromBlacklist
from errors.errors import MissingFieldsError, InvalidUUIDError, InvalidSearchFieldsError, InvalidReasonFieldsError, ApiError
from models.blackListedEmail import BlackListedEmail
from sqlalchemy.exc import SQLAlchemyError

class TestServices(unittest.TestCase):

    def setUp(self):
        self.valid_email_data = {
            'email': 'test@example.com',
            'app_uuid': str(uuid.uuid4()),
            'blocked_reason': 'Test reason'
        }
        self.valid_ip = '127.0.0.1'
        
        # Mock para la sesión de la base de datos
        self.mock_session = MagicMock()
        self.mock_session.add = MagicMock()
        self.mock_session.commit = MagicMock()
        self.mock_session.rollback = MagicMock()
        
        # Mock para el modelo BlackListedEmail
        self.mock_blacklisted_email = MagicMock()
        self.mock_blacklisted_email.email = self.valid_email_data['email']
        self.mock_blacklisted_email.appId = self.valid_email_data['app_uuid']
        self.mock_blacklisted_email.reason = self.valid_email_data['blocked_reason']
        self.mock_blacklisted_email.ipAddress = self.valid_ip

    @patch('services.services.db')
    def test_add_blacklist_email_success(self, mock_db):
        # Configurar el mock
        mock_db.session = self.mock_session
        BlackListedEmail = MagicMock()
        BlackListedEmail.return_value = self.mock_blacklisted_email
        
        with patch('services.services.BlackListedEmail', BlackListedEmail):
            result = addBlacklistEmail(self.valid_email_data, self.valid_ip)

        BlackListedEmail.assert_called_once()
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
        
        self.assertEqual(result, self.mock_blacklisted_email)

    def test_add_blacklist_email_missing_fields(self):
        # Probar con datos faltantes
        invalid_data = {'email': 'test@example.com'}  # Falta app_uuid
        
        with self.assertRaises(MissingFieldsError):
            addBlacklistEmail(invalid_data, self.valid_ip)

    def test_add_blacklist_email_invalid_email(self):
        # Probar con email inválido
        invalid_data = self.valid_email_data.copy()
        invalid_data['email'] = 'invalid-email'
        
        with self.assertRaises(InvalidSearchFieldsError):
            addBlacklistEmail(invalid_data, self.valid_ip)

    def test_add_blacklist_email_invalid_uuid(self):
        # Probar con UUID inválido
        invalid_data = self.valid_email_data.copy()
        invalid_data['app_uuid'] = 'not-a-uuid'
        
        with self.assertRaises(InvalidUUIDError):
            addBlacklistEmail(invalid_data, self.valid_ip)

    def test_add_blacklist_email_invalid_reason_length(self):
        # Probar con razón demasiado larga
        invalid_data = self.valid_email_data.copy()
        invalid_data['blocked_reason'] = 'a' * 256
        
        with self.assertRaises(InvalidReasonFieldsError):
            addBlacklistEmail(invalid_data, self.valid_ip)

    @patch('services.services.db')
    def test_add_blacklist_email_db_error(self, mock_db):
        # Configurar el mock para simular un error de base de datos
        mock_db.session = self.mock_session
        self.mock_session.commit.side_effect = SQLAlchemyError("Database error")
        
        result = addBlacklistEmail(self.valid_email_data, self.valid_ip)
        
        self.mock_session.rollback.assert_called_once()
        
        self.assertIsNone(result)

    @patch('services.services.BlackListedEmail')
    def test_get_email_from_blacklist_found(self, mock_blacklisted_email_class):
       
        mock_blacklisted_email_class.query.filter_by.return_value.first.return_value = self.mock_blacklisted_email
        
        result = getEmailFromBlacklist(self.valid_email_data['email'])
        
        mock_blacklisted_email_class.query.filter_by.assert_called_once_with(email=self.valid_email_data['email'])
        
        self.assertEqual(result, self.mock_blacklisted_email)

    @patch('services.services.BlackListedEmail')
    def test_get_email_from_blacklist_not_found(self, mock_blacklisted_email_class):

        mock_blacklisted_email_class.query.filter_by.return_value.first.return_value = None
        
        result = getEmailFromBlacklist(self.valid_email_data['email'])
        
      
        mock_blacklisted_email_class.query.filter_by.assert_called_once_with(email=self.valid_email_data['email'])
        
        self.assertIsNone(result)

    def test_get_email_from_blacklist_empty_email(self):
        # Probar con email vacío
        result = getEmailFromBlacklist(None)

        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main() 