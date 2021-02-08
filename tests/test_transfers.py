from buycoins_client import Auth
from buycoins_client import Transfers
import unittest
from unittest.mock import patch

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

class TestBuySellMethods(unittest.TestCase):

    def test_invalid_fees_args_cryptocurrency(self):
        """
            Should throw an exception for invalid crytocurrency argument
        """
        try:
            Transfers.fees({"cryptocurrency":""})
        except Exception as e:
            self.assertEqual(str(e), "cryptocurrency argument must be a valid string identifier.")


    def test_invalid_fees_args_amount(self):
        """
            Should throw an exception for invalid crytocurrency argument
        """
        try:
            Transfers.fees({"cryptocurrency":"bitcoin", "amount":-0.2})
        except Exception as e:
            self.assertEqual(str(e), "amount argument must be a valid float and greater than 0.")


    @patch('buycoins_client.Transfers.requests.post')  # Mock 'requests' module 'post' method.
    def test_failed_fees_request(self, mock_post):
        """
            Should return a failure status when fees retrieval fails
        """

        mock_post.return_value = MockResponse({"errors":[{"message":"Argument 'cryptocurrency' on Field 'getEstimatedNetworkFee' has an invalid value (ethereu). Expected type 'Cryptocurrency'.","locations":[{"line":3,"column":3}],"path":["query","getEstimatedNetworkFee","cryptocurrency"],"extensions":{"code":"argumentLiteralsIncompatible","typeName":"Field","argumentName":"cryptocurrency"}}]}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Transfers.fees({"amount":0.02, "cryptocurrency":"bitcoin"}, [])
        
        self.assertEqual(response['status'], "failure")
        self.assertEqual(response["errors"][0]["reason"], "Argument 'cryptocurrency' on Field 'getEstimatedNetworkFee' has an invalid value (ethereu). Expected type 'Cryptocurrency'.")

    @patch('buycoins_client.Transfers.requests.post')  # Mock 'requests' module 'post' method.
    def test_successful_fees_request(self, mock_post):
        """
            Should return a success status when fees is successfully retrieved for a valid cryptocurrency
        """

        mock_post.return_value = MockResponse({"data":{"getEstimatedNetworkFee":{"estimatedFee":"0.0166","total":"0.0266"}}}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Transfers.fees({"amount":0.02, "cryptocurrency":"ethereum"}, [])
        
        self.assertEqual(response['status'], "success")
        self.assertEqual(response["data"]["getEstimatedNetworkFee"]["total"], "0.0266")
        self.assertEqual(response["data"]["getEstimatedNetworkFee"]["estimatedFee"], "0.0166")

    def test_invalid_sell_args_price(self):
        """
            Should throw an exception for invalid price id
        """
        try:
            Transfers.sell({"price":"", "coin_amount":0.02, "cryptocurrency":"bitcoin"})
        except Exception as e:
            self.assertEqual(str(e), "price argument must be a valid string identifier.")

    def test_invalid_sell_args(self):
        """
            Should throw an exception for invalid coin_amount
        """
        try:
            Transfers.sell({"price":"QnV5Y29pbnNQcmljZS0zOGIwYTg1Yi1jNjA1LTRhZjAtOWQ1My01ODk1MGVkMjUyYmQ=", "coin_amount":0.0, "cryptocurrency":"bitcoin"})
        except Exception as e:
            self.assertEqual(str(e), "coin_amount argument must be a valid float and greater than 0.")

    def test_invalid_sell_args(self):
        """
            Should throw an exception for invalid cryptocurrency
        """
        try:
            Transfers.sell({"price":"QnV5Y29pbnNQcmljZS0zOGIwYTg1Yi1jNjA1LTRhZjAtOWQ1My01ODk1MGVkMjUyYmQ=", "coin_amount":0.02, "cryptocurrency":""})
        except Exception as e:
            self.assertEqual(str(e), "cryptocurrency argument must be a valid string identifier.")

    @patch('buycoins_client.Transfers.requests.post')  # Mock 'requests' module 'post' method.
    def test_failed_sell_request(self, mock_post):
        """
            Should return a failure status when sale request fails
        """

        mock_post.return_value = MockResponse({"errors":[{"message":"Argument 'price' on Field 'sell' has an invalid value (meat). Expected type 'ID!'.","locations":[{"line":1,"column":12}],"path":["mutation","sell","price"],"extensions":{"code":"argumentLiteralsIncompatible","typeName":"Field","argumentName":"price"}}]}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Transfers.sell({"price":"meat", "coin_amount":0.02, "cryptocurrency":"bitcoin"}, [])
        
        self.assertEqual(response['status'], "failure")
        self.assertEqual(response["errors"][0]["reason"], "Argument 'price' on Field 'sell' has an invalid value (meat). Expected type 'ID!'.")

    @patch('buycoins_client.Transfers.requests.post')  # Mock 'requests' module 'post' method.
    def test_failed_buy_request(self, mock_post):
        """
            Should return a failure status when sale request fails
        """

        mock_post.return_value = MockResponse({"errors":[{"message":"Argument 'price' on Field 'buy' has an invalid value (meat). Expected type 'ID!'.","locations":[{"line":1,"column":12}],"path":["mutation","buy","price"],"extensions":{"code":"argumentLiteralsIncompatible","typeName":"Field","argumentName":"price"}}]}, 200)
        
        Auth.setup("chuks", "emeka")
        response = Transfers.buy({"price":"meat", "coin_amount":0.02, "cryptocurrency":"bitcoin"}, [])
        
        self.assertEqual(response['status'], "failure")
        self.assertEqual(response["errors"][0]["reason"], "Argument 'price' on Field 'buy' has an invalid value (meat). Expected type 'ID!'.")

    
if __name__ == '__main__':
    unittest.main()
