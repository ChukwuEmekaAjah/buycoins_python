from buycoins_python import Prices
from buycoins_python import Auth
import unittest
from unittest.mock import patch

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

class TestPricesMethods(unittest.TestCase):

    def test_invalid_field(self):
        """
            Should throw an exception for a node dict without a field property
        """
        try:
            Prices.list([{"field":"cryptocrrency"}, {"name":"chuks"}])
        except Exception as e:
            self.assertEqual(str(e), "Fields contains a node dict without a 'field' property.")
    
    @patch('buycoins_python.Prices.requests.post')  # Mock 'requests' module 'post' method.
    def test_failed_prices_retrieval(self, mock_post):
        """
            Should return a failure status when invalid node is requested.
        """

        mock_post.return_value = MockResponse({"errors":[{"message":"Field 'cryptocrrency' doesn't exist on type 'BuycoinsPrice'","locations":[{"line":1,"column":23}],"path":["query","getPrices","cryptocrrency"],"extensions":{"code":"undefinedField","typeName":"BuycoinsPrice","fieldName":"cryptocrrency"}}]}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Prices.list([{"field":"cryptocrrency"}])
        
        self.assertEqual(response['status'], "failure")
        self.assertEqual(response["errors"][0]["reason"], "Field 'cryptocrrency' doesn't exist on type 'BuycoinsPrice'")

    @patch('buycoins_python.Prices.requests.post')  # Mock 'requests' module 'post' method.
    def test_successful_prices_retrieval(self, mock_post):
        """
            Should return a success status for successful prices retrieval
        """
        mock_post.return_value = MockResponse({"data":{"getPrices":[{"id":"QnV5Y29pbnNQcmljZS1mM2ZhOWI2Yy00MmM4LTQxMzAtOThmZC0zZGMwYjRjMmRlNjQ=","cryptocurrency":"bitcoin","sellPricePerCoin":"17827839.315","minSell":"0.001","maxSell":"0.35190587","expiresAt":1612391202}]}}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Prices.list([])
        
        self.assertEqual(response['status'], "success")
        self.assertEqual(response["data"]["getPrices"][0]["id"], "QnV5Y29pbnNQcmljZS1mM2ZhOWI2Yy00MmM4LTQxMzAtOThmZC0zZGMwYjRjMmRlNjQ=")
        self.assertEqual(response["data"]["getPrices"][0]["cryptocurrency"], "bitcoin")

if __name__ == '__main__':
    unittest.main()
