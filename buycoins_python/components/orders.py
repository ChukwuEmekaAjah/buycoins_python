import requests
from requests.auth import HTTPBasicAuth
from . import utilities


def list_my_orders(status:str="open", fields:list=[]):
    """
        Retrieve a list of orders made by you on the platform. 

        If fields parameter is empty, it defaults to retrieving all the fields
    """

    if(not status or type(status) is not str or not status.strip()):
        raise Exception("status parameter is compulsory and it is a string. Default is 'open'")

    status_types = ["open", "completed"]
    if status not in status_types:
        raise Exception("Personal orders status can only be 'open' or 'completed'.")

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

def list_market_orders(fields:list=[]):
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

def buy(args:dict, fields:list=[]):
    """
        Buy a cryptocurrency
        args key-value pairs are important.
        If fields parameter is empty, it defaults to retrieving all the fields
    """
    # add validation for fields
    if(not utilities.is_valid_fields(fields)):
        raise Exception("Fields contains a node dict without a 'field' property.")

    if not args.get("price") or type(args.get("price")) is not str or not args.get("price").strip():
        raise Exception("price argument must be a valid string identifier.")

    if not args.get("cryptocurrency") or type(args.get("cryptocurrency")) is not str or not args.get("cryptocurrency").strip():
        raise Exception("cryptocurrency argument must be a valid string identifier.")

    if not args.get("coin_amount") or type(args.get("coin_amount")) is not float or args.get("coin_amount") <= 0:
        raise Exception("coin_amount argument must be a valid float and greater than 0.")
    
    query_dict = {
        "operation": "mutation",
        "command": "buy",
        "args": args,
        "fields": fields if len(fields) > 0 else [{"field":"id"}, {"field":"cryptocurrency"}, {"field":"status"}, {"field":"totalCoinAmount"}, {"field":"side"}]
    }

    data = utilities.create_request_body(query_dict)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=HTTPBasicAuth(utilities.AUTH['username'], utilities.AUTH['password']), data={"query":data}, params={})
    
    return utilities.parse_response(response)

def sell(args:dict, fields:list=[]):
    """
        Buy a cryptocurrency
        args key-value pairs are important.
        If fields parameter is empty, it defaults to retrieving all the fields
    """
    # add validation for fields
    if(not utilities.is_valid_fields(fields)):
        raise Exception("Fields contains a node dict without a 'field' property.")

    if not args.get("price") or type(args.get("price")) is not str or not args.get("price").strip():
        raise Exception("price argument must be a valid string identifier.")

    if not args.get("cryptocurrency") or type(args.get("cryptocurrency")) is not str or not args.get("cryptocurrency").strip():
        raise Exception("cryptocurrency argument must be a valid string identifier.")

    if not args.get("coin_amount") or type(args.get("coin_amount")) is not float or args.get("coin_amount") <= 0:
        raise Exception("coin_amount argument must be a valid float and greater than 0.")
    
    query_dict = {
        "operation": "mutation",
        "command": "sell",
        "args": args,
        "fields": fields if len(fields) > 0 else [{"field":"id"}, {"field":"cryptocurrency"}, {"field":"status"}, {"field":"totalCoinAmount"}, {"field":"side"}]
    }

    data = utilities.create_request_body(query_dict)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=HTTPBasicAuth(utilities.AUTH['username'], utilities.AUTH['password']), data={"query":data}, params={})
    
    return utilities.parse_response(response)

