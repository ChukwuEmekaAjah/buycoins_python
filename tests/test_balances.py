from buycoins_python import Balances
from buycoins_python import Auth
import unittest
from unittest.mock import patch

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

class TestBalancesMethods(unittest.TestCase):

    def test_invalid_field(self):
        """
            Should throw an exception for a node dict without a field property
        """
        try:
            Balances.list([{"field":"cryptocrrency"}, {"name":"chuks"}])
        except Exception as e:
            self.assertEqual(str(e), "Fields contains a node dict without a 'field' property.")

    def test_invalid_get_parameter(self):
        """
            Should throw an exception for invalid single cryptocurrency retrieval parameter
        """
        try:
            Balances.get("    ")
        except Exception as e:
            self.assertEqual(str(e), "cryptocurrency argument must be a valid string identifier.")
    
    @patch('buycoins_python.Balances.requests.post')  # Mock 'requests' module 'post' method.
    def test_failed_Balances_retrieval(self, mock_post):
        """
            Should return a failure status when invalid node is requested.
        """

        mock_post.return_value = MockResponse({"errors":[{"message":"Field 'cryptocurrenc' doesn't exist on type 'Account'","locations":[{"line":7,"column":5}],"path":["query","getBalances","cryptocurrenc"],"extensions":{"code":"undefinedField","typeName":"Account","fieldName":"cryptocurrenc"}}]}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Balances.list([{"field":"cryptocrrency"}])
        
        self.assertEqual(response['status'], "failure")
        self.assertEqual(response["errors"][0]["reason"], "Field 'cryptocurrenc' doesn't exist on type 'Account'")

    @patch('buycoins_python.Balances.requests.post')  # Mock 'requests' module 'post' method.
    def test_successful_Balances_get(self, mock_post):
        """
            Should return a success status for successful single balance retrieval
        """
        mock_post.return_value = MockResponse({"data":{"getBalances":[{"id":"QWNjb3VudC0=","cryptocurrency":"usd_tether","confirmedBalance":"0.0"}]}}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Balances.get("usd_tether")
        
        self.assertEqual(response['status'], "success")
        self.assertEqual(response["data"]["getBalances"][0]["id"], "QWNjb3VudC0=")
        self.assertEqual(response["data"]["getBalances"][0]["cryptocurrency"], "usd_tether")

    @patch('buycoins_python.Balances.requests.post')  # Mock 'requests' module 'post' method.
    def test_successful_Balances_list(self, mock_post):
        """
            Should return a success status for successful Balances retrieval
        """
        mock_post.return_value = MockResponse({"data":{"getBalances":[{"id":"QWNjb3VudC0=","cryptocurrency":"usd_tether","confirmedBalance":"0.0"}]}}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Balances.list([])
        
        self.assertEqual(response['status'], "success")
        self.assertEqual(response["data"]["getBalances"][0]["id"], "QWNjb3VudC0=")
        self.assertEqual(response["data"]["getBalances"][0]["cryptocurrency"], "usd_tether")

if __name__ == '__main__':
    unittest.main()
