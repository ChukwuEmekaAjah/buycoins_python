from buycoins_python import Accounts
from buycoins_python import Auth
import unittest
from unittest.mock import patch

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

class TestAccountMethods(unittest.TestCase):

    def test_invalid_account_name(self):
        """
            Should throw an exception for invalid account name
        """
        
        Auth.setup("chuks", "emeka")
        try:
            Accounts.create("")
        except Exception as e:
            self.assertEqual(str(e), "Please provide account name to create bank account for")

    
    @patch('buycoins_python.Accounts.requests.post')  # Mock 'requests' module 'post' method.
    def test_failed_account_creation(self, mock_post):
        """
            Should return a failure status for failed account creation
        """

        mock_post.return_value = MockResponse({"errors":[{"message":"hello world", "path":["ajah","chuks"]}]}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Accounts.create("Emeka")
        
        self.assertEqual(response['status'], "failure")

    @patch('buycoins_python.Accounts.requests.post')  # Mock 'requests' module 'post' method.
    def test_successful_account_creation(self, mock_post):
        """
            Should return a success status for successful account creation
        """
        mock_post.return_value = MockResponse({"data":{"createDepositAccount":{"accountName":"Emeka"}}}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Accounts.create("Emeka")
        
        self.assertEqual(response['status'], "success")
        


if __name__ == '__main__':
    unittest.main()
