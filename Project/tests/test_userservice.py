from models.users import User
from unittest.mock import patch,MagicMock
from services.UserService import UserService
import pytest

def test_home(client):
    response = client.get("/register")
    assert b"<title>signup</title>" in response.data
    
def test_register_mocks():
    with patch('services.UserService.UserRepository.find_by_email', return_value = None) as mock_find, \
         patch('services.UserService.UserRepository.create_user', return_value = None) as mock_create_user:
             
        user = UserService.register_user('john', 'cena', 'john@gmail.com', 'password123')
        mock_find.assert_called_once_with('john@gmail.com')    
        mock_create_user.assert_called_once()
    
        assert user.email == 'john@gmail.com'
        assert user.firstname == 'john'
        assert user.lastname == 'cena'
        
def test_register_existing_email():


    with patch('services.UserService.UserRepository.find_by_email') as mock_find, \
         patch('services.UserService.UserRepository.create_user') as mock_create:
        
        # First registration: Email does not exist
        mock_find.return_value = None
        mock_create.return_value = None
        
        # Register the first user
        user1 = UserService.register_user('john', 'cena', 'john@gmail.com', 'password123')
        
        # Ensure `find_by_email` and `create_user` were called correctly
        mock_find.assert_called_once_with('john@gmail.com')
        mock_create.assert_called_once()
        assert user1.email == 'john@gmail.com'
        assert user1.firstname == 'john'
        assert user1.lastname == 'cena'
        
        # Reset mocks to track calls for the second registration
        mock_find.reset_mock()
        mock_create.reset_mock()
        
        # Simulate that a user now exists with the provided email
        existing_user = MagicMock(spec=User)
        existing_user.email = 'john@gmail.com'
        existing_user.firstname = 'john'
        existing_user.lastname = 'cena'
        existing_user.password = 'hashed_password123'
        mock_find.return_value = existing_user
        
        # Attempt to register another user with the same email, expecting a ValueError
        with pytest.raises(ValueError) as excinfo:
            UserService.register_user('john2', 'cena2', 'john@gmail.com', 'password123')
        
        # Assert that the correct exception message is raised
        assert "Email already exists" in str(excinfo.value)
        
        # Ensure that `find_by_email` was called again with the same email
        mock_find.assert_called_once_with('john@gmail.com')
        
        # Ensure that `create_user` was NOT called again since the email exists
        mock_create.assert_not_called()

def test_login_mocks():

    with patch('services.UserService.UserRepository.find_by_email') as mock_find, \
         patch('services.UserService.ph.verify') as mock_verify:
        
        # Create a mock User object
        mock_user = MagicMock(spec=User)
        mock_user.firstname = 'John'
        mock_user.lastname = 'Cena'
        mock_user.email = 'john@gmail.com'
        mock_user.password = 'hashed_password123'  # Assume passwords are hashed
        
        # Configure the mocks
        mock_find.return_value = mock_user
        mock_verify.return_value = True  # Simulate correct password verification
        
        # Call the login_user service method
        user = UserService.login_user('john@gmail.com', 'password123')
        
        # Assertions to ensure methods were called correctly
        mock_find.assert_called_once_with('john@gmail.com')
        mock_verify.assert_called_once_with('hashed_password123', 'password123')
        
        # Assertions on the returned User object
        assert user.email == 'john@gmail.com'
