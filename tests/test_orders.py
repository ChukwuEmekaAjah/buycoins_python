from buycoins_python import Auth
from buycoins_python import Orders
import unittest
from unittest.mock import patch

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

class TestOrdersMethods(unittest.TestCase):

    def test_invalid_status_type(self):
        """
            Should throw an exception for status parameter type that is not a string
        """
        try:
            Orders.list_my_orders(3)
        except Exception as e:
            self.assertEqual(str(e), "status parameter is compulsory and it is a string. Default is 'open'")

    def test_invalid_status(self):
        """
            Should throw an exception for invalid status parameter
        """
        try:
            Orders.list_my_orders("closed")
        except Exception as e:
            self.assertEqual(str(e), "Personal orders status can only be 'open' or 'completed'.")

    def test_invalid_field(self):
        """
            Should throw an exception for a node dict without a field property
        """
        try:
            Orders.list_my_orders("completed", [{"field":"cryptocrrency"}, {"name":"chuks"}])
        except Exception as e:
            self.assertEqual(str(e), "Fields contains a node dict without a 'field' property.")
    
    @patch('buycoins_python.Orders.requests.post')  # Mock 'requests' module 'post' method.
    def test_failed_list_my_orders(self, mock_post):
        """
            Should return a failure status when invalid node is requested.
        """

        mock_post.return_value = MockResponse({"errors":[{"message":"Field 'edgesa' doesn't exist on type 'PostOrderConnection'","locations":[{"line":1,"column":59}],"path":["query","getOrders","orders","edgesa"],"extensions":{"code":"undefinedField","typeName":"PostOrderConnection","fieldName":"edgesa"}}]}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Orders.list_my_orders("completed", [])
        
        self.assertEqual(response['status'], "failure")
        self.assertEqual(response["errors"][0]["reason"], "Field 'edgesa' doesn't exist on type 'PostOrderConnection'")

    @patch('buycoins_python.Orders.requests.post')  # Mock 'requests' module 'post' method.
    def test_successful_list_my_orders(self, mock_post):
        """
            Should return a success status for successful personal orders retrieval
        """
        mock_post.return_value = MockResponse({"data":{"getOrders":{"dynamicPriceExpiry":1612396362,"orders":{"edges":[]}}}}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Orders.list_my_orders(status="open", fields=[])
        
        self.assertEqual(response['status'], "success")
        self.assertEqual(response["data"]["getOrders"]["dynamicPriceExpiry"], 1612396362)

    @patch('buycoins_python.Orders.requests.post')  # Mock 'requests' module 'post' method.
    def test_failed_list_market_orders(self, mock_post):
        """
            Should return a failure status when invalid node is requested.
        """

        mock_post.return_value = MockResponse({"errors":[{"message":"Field 'edgesa' doesn't exist on type 'PostOrderConnection'","locations":[{"line":1,"column":59}],"path":["query","getMarketBook","orders","edgesa"],"extensions":{"code":"undefinedField","typeName":"PostOrderConnection","fieldName":"edgesa"}}]}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Orders.list_market_orders([])
        
        self.assertEqual(response['status'], "failure")
        self.assertEqual(response["errors"][0]["reason"], "Field 'edgesa' doesn't exist on type 'PostOrderConnection'")

    @patch('buycoins_python.Orders.requests.post')  # Mock 'requests' module 'post' method.
    def test_successful_list_market_orders(self, mock_post):
        """
            Should return a success status for successful personal orders retrieval
        """
        mock_post.return_value = MockResponse({"data":{"getMarketBook":{"dynamicPriceExpiry":1612396362,"orders":{"edges":[]}}}}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Orders.list_market_orders(fields=[])
        
        self.assertEqual(response['status'], "success")
        self.assertEqual(response["data"]["getMarketBook"]["dynamicPriceExpiry"], 1612396362)

if __name__ == '__main__':
    unittest.main()
