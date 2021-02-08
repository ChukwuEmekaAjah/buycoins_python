import requests
from requests.auth import HTTPBasicAuth
from . import utilities


def list_my_orders(status:str="open", fields:list=[]):
    """Retrieve a list of orders made by you on the platform. 

    Returns all the orders made by you on the Buycoins platform

    Args:
        status (str):
            The status of the order. It is either "completed" or "open"
        fields (list):
            The fields you want returned by the graphql query. It defaults to all the query fields associated with the getOrders query if this argument is absent or empty. It is a list of dictionaries. 
            An example field dict is represented as:

            {"field": "estimatedFee"}

            Default fields are:
            [{"field": "estimatedFee"}, {"field": "total"}]
    
    Returns:
        A dict mapping containing a status key which can either be one of: "failure" or "success" and an errors/data key  depending on the status of the request. For example:

        {"status":"success",
         "data":{
            "getOrders":{
                "dynamicPriceExpiry":235245646
            }
         }
        }

    Raises:
        Exception: Only raised if the status is invalid or fields having an item dict without the field property.
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
    """Retrieve a list of orders made on the marketplace platform.
    
    Returns all the orders that are available on the Buycoins marketplace

    Args:
        fields (list):
            The fields you want returned by the graphql query. It defaults to all the query fields associated with the getMarketBook query if this argument is absent or empty. It is a list of dictionaries. 
            An example field dict is represented as:

            {"field": "estimatedFee"}

            Default fields are:
            [{"field": "estimatedFee"}, {"field": "total"}]
    
    Returns:
        A dict mapping containing a status key which can either be one of: "failure" or "success" and an errors/data key  depending on the status of the request. For example:

        {"status":"success",
         "data":{
            "getMarketBook":{
                "dynamicPriceExpiry":235245646
            }
         }
        }

    Raises:
        Exception: Only raised if fields having an item dict without the field property.
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

def post_limit_order(args:dict, fields:list=[]):
    """Post a limit order

    Returns the order data from making a postLimitOrder mutation call on the API. 

    Args:
        args (dict):
            Arguments required by the graphql query to calculate the fees

            args['orderSide'] (str):
                The orderSide for the order you want to post. It is either "buy" or "sell"
            args['priceType'] (str):
                The priceType you want your order to use. It can be either "dynamic" or "static"
            args['cryptocurrency'] (str):
                The cryptocurrency for which you want to post
            args['coinAmount'] (float):
                The amount cryptocurrency you intend to post
            args['staticPrice'] (str):
                The static price you want to use for the order. It is an `optional` field.
            args['dynamicExchangeRate'] (str):
                The exchange rate between naira and dollar for the cryptocurrency value you want to use for the order. It is an `optional` field. 
        
        fields (list):
            The fields you want returned by the graphql query. It defaults to all the mutation fields of the postListOrder mutation if this argument is absent or empty. It is a list of dictionaries. 
            An example field dict is represented as:

            {"field": "estimatedFee"}

            Default fields are:
            [{"field": "estimatedFee"}, {"field": "total"}]
    
    Returns:
        A dict mapping containing a status key which can either be one of: "failure" or "success" and an errors/data key  depending on the status of the request. For example:

        {"status":"success",
         "data":{
            "postLimitOrder":{
                "id":"afWGFdfa823ladfadfja",
                "status":"open"
            }
         }
        }

    Raises:
        Exception: Only raised if any of the args parameter fields are invalid e.g coinAmount not being a float or fields having an item dict without the field property.
    """
    order_side_types = ["buy", "sell"]
    price_types = ["static", "dynamic"]
    
    # add validation for fields
    if(not utilities.is_valid_fields(fields)):
        raise Exception("Fields contains a node dict without a 'field' property.")

    if not args.get("orderSide") or args.get("orderSide") not in order_side_types:
        raise Exception("orderSide argument must be a valid string that is either 'buy' or 'sell'")

    if not args.get("priceType") or args.get("priceType") not in price_types:
        raise Exception("priceType argument must be a valid string that is either 'dynamic' or 'static'")

    if not args.get("cryptocurrency") or type(args.get("cryptocurrency")) is not str or not args.get("cryptocurrency").strip():
        raise Exception("cryptocurrency argument must be a valid string identifier.")

    if not args.get("coinAmount") or type(args.get("coinAmount")) is not float or args.get("coinAmount") <= 0:
        raise Exception("coinAmount argument must be a valid float and greater than 0.")

    if args.get("staticPrice"):
        if type(args.get("staticPrice")) is not float or args.get("staticPrice") <= 0:
            raise Exception("staticPrice argument must be a valid float and greater than 0.")

    if args.get("dynamicExchangeRate"):
        if type(args.get("dynamicExchangeRate")) is not float or args.get("dynamicExchangeRate") <= 0:
            raise Exception("dynamicExchangeRate argument must be a valid float and greater than 0.")
    
    query_dict = {
        "operation": "mutation",
        "command": "postLimitOrder",
        "args": args,
        "fields": fields if len(fields) > 0 else [{"field":"id"}, {"field":"cryptocurrency"}, {"field":"status"}, {"field":"coinAmount"}, {"field":"side"}, {"field":"createdAt"}, {"field":"pricePerCoin"}, {"field":"priceType"}, {"field":"staticPrice"}, {"field":"dynamicExchangeRate"}]
    }

    data = utilities.create_request_body(query_dict)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=HTTPBasicAuth(utilities.AUTH['username'], utilities.AUTH['password']), data={"query":data}, params={})
    
    return utilities.parse_response(response)


def post_market_order(args:dict, fields:list=[]):
    """Post a market order

    Returns the order data from making a postMarketOrder mutation call on the API. 

    Args:
        args (dict):
            Arguments required by the graphql query to calculate the fees

            args['orderSide'] (str):
                The orderSide for the order you want to post. It is either "buy" or "sell"
            args['cryptocurrency'] (str):
                The cryptocurrency for which you want to post
            args['coinAmount'] (float):
                The amount cryptocurrency you intend to post
            
        fields (list):
            The fields you want returned by the graphql query. It defaults to all the mutation fields of the postMarketOrder mutation if this argument is absent or empty. It is a list of dictionaries. 
            An example field dict is represented as:

            {"field": "estimatedFee"}

            Default fields are:
            [{"field": "estimatedFee"}, {"field": "total"}]
    
    Returns:
        A dict mapping containing a status key which can either be one of: "failure" or "success" and an errors/data key  depending on the status of the request. For example:

        {"status":"success",
         "data":{
            "postMarketOrder":{
                "id":"afWGFdfa823ladfadfja",
                "status":"open"
            }
         }
        }

    Raises:
        Exception: Only raised if any of the args parameter fields are invalid e.g coinAmount not being a float or fields having an item dict without the field property.
    """
    order_side_types = ["buy", "sell"]
    
    # add validation for fields
    if(not utilities.is_valid_fields(fields)):
        raise Exception("Fields contains a node dict without a 'field' property.")

    if not args.get("orderSide") or args.get("orderSide") not in order_side_types:
        raise Exception("orderSide argument must be a valid string that is either 'buy' or 'sell'")

    if not args.get("cryptocurrency") or type(args.get("cryptocurrency")) is not str or not args.get("cryptocurrency").strip():
        raise Exception("cryptocurrency argument must be a valid string identifier.")

    if not args.get("coinAmount") or type(args.get("coinAmount")) is not float or args.get("coinAmount") <= 0:
        raise Exception("coinAmount argument must be a valid float and greater than 0.")

    query_dict = {
        "operation": "mutation",
        "command": "postMarketOrder",
        "args": args,
        "fields": fields if len(fields) > 0 else [{"field":"id"}, {"field":"cryptocurrency"}, {"field":"status"}, {"field":"coinAmount"}, {"field":"side"}, {"field":"createdAt"}, {"field":"pricePerCoin"}, {"field":"priceType"}, {"field":"staticPrice"}, {"field":"dynamicExchangeRate"}]
    }

    data = utilities.create_request_body(query_dict)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=HTTPBasicAuth(utilities.AUTH['username'], utilities.AUTH['password']), data={"query":data}, params={})
    
    return utilities.parse_response(response)

