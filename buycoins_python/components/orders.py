import requests
from requests.auth import HTTPBasicAuth
from . import utilities


def list_my_orders(status:str = "open", fields:list = []):
    """
        Retrieve a list of orders made by you on the platform. 

        If fields parameter is empty, it defaults to retrieving all the fields
    """
    # add validation for fields

    if(not utilities.is_valid_fields(fields)):
        raise Exception("Fields contains a node dict without a 'field' property.")

    query_dict = {
        "operation": "query",
        "command": "getOrders",
        "args": {"status":status},
        "fields": fields if len(fields) > 0 else [{"field":"dynamicPriceExpiry"}, {"field":"orders", "fields":[{"field":"edges", "fields": [{"field":"node", "fields":[{"field":"id"}, {"field":"cryptocurrency"}, {"field":"coinAmount"}, {"field":"side"}, {"field":"status"}, {"field":"createdAt"}, {"field":"pricePerCoin"}, {"field":"priceType"}, {"field":"staticPrice"}, {"field":"dynamicExchangeRate"}]}]}]}]
    }


    data = utilities.create_request_body(query_dict)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=HTTPBasicAuth(utilities.AUTH['username'], utilities.AUTH['password']), data={"query":data}, params={})
    
    return utilities.parse_response(response)

def list_market_orders(fields:list = []):
    """
        Retrieve a list of orders made on the marketplace platform.

        If fields parameter is empty, it defaults to retrieving all the fields
    """
    # add validation for fields

    if(not utilities.is_valid_fields(fields)):
        raise Exception("Fields contains a node dict without a 'field' property.")

    query_dict = {
        "operation": "query",
        "command": "getMarketBook",
        "fields": fields if len(fields) > 0 else [{"field":"dynamicPriceExpiry"}, {"field":"orders", "fields":[{"field":"edges", "fields": [{"field":"node", "fields":[{"field":"id"}, {"field":"cryptocurrency"}, {"field":"coinAmount"}, {"field":"side"}, {"field":"status"}, {"field":"createdAt"}, {"field":"pricePerCoin"}, {"field":"priceType"}, {"field":"staticPrice"}, {"field":"dynamicExchangeRate"}]}]}]}]
    }


    data = utilities.create_request_body(query_dict)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=HTTPBasicAuth(utilities.AUTH['username'], utilities.AUTH['password']), data={"query":data}, params={})
    
    return utilities.parse_response(response)

