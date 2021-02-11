import requests
from requests.auth import HTTPBasicAuth
from . import utilities

def fees(args:dict, fields:list=[]):
    """Retrieve fees for sending a cryptocurrency to an address
      
    Returns the fee amount in the specified cryptocurrency needed to make a transfer to another cryptocurrency address in the same currency

    Args:
        args (dict):
            Arguments required by the graphql query to calculate the fees

            args['cryptocurrency'] (str):
                The cryptocurrency for which we want to calculate fees for
            args['amount'] (float):
                The amount cryptocurrency you intend to send
        
        fields (list):
            The fields you want returned by the graphql query. It defaults to all the query fields of the getEstimatedNetworkFee query if this argument is absent or empty. It is a list of dictionaries. 
            An example field dict is represented as:

            {"field": "estimatedFee"}

            Default fields are:
            [{"field": "estimatedFee"}, {"field": "total"}]
    
    Returns:
        A dict mapping containing a status key which can either be one of: "failure" or "success" and an errors/data key  depending on the status of the request. For example:

        {"status":"success",
         "data":{
            "getEstimatedNetworkFee":{
                "estimatedFee":0.00002,
                "total":0.000003
            }
         }
        }

    Raises:
        Exception: Only raised if any of the args parameter fields are invalid e.g amount not being a float or fields having an item dict without the field property.
    """

    if not args.get("cryptocurrency") or type(args.get("cryptocurrency")) is not str or not args.get("cryptocurrency").strip():
        raise Exception("cryptocurrency argument must be a valid string identifier.")

    if not args.get("amount") or type(args.get("amount")) is not float or args.get("amount") <= 0:
        raise Exception("amount argument must be a valid float and greater than 0.")

    # add validation for fields

    if(not utilities.is_valid_fields(fields)):
        raise Exception("Fields contains a node dict without a 'field' property.")


    query_dict = {
        "operation": "query",
        "command": "getEstimatedNetworkFee",
        "args": args,
        "fields": fields if len(fields) > 0 else [{"field":"estimatedFee"}, {"field":"total"}]
    }

    data = utilities.create_request_body(query_dict)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=HTTPBasicAuth(utilities.AUTH['username'], utilities.AUTH['password']), data={"query":data}, params={})
    
    return utilities.parse_response(response)

def send(args:dict, fields:list=[]):
    """Send cryptocurrency to a cryptocurrency address

    Returns the transaction details after making a request to send cryptocurrency to an address

    Args:
        args (dict):
            Arguments required by the graphql query to send the currency

            args['cryptocurrency'] (str):
                The cryptocurrency you want to send.
            args['amount'] (float):
                The amount of cryptocurrency you intend to send
            args['address'] (str):
                The address of the proposed recipient of the cryptocurrency
        
        fields (list):
            The fields you want returned by the graphql query. It defaults to all the query fields if this argument is absent or empty. It is a list of dictionaries. 
            An example field dict is represented as:

            {"field": "estimatedFee"}

            Default fields are:
            [{"field": "estimatedFee"}, {"field": "total"}]

            See fields definition in Readme file for help on writing fields you want returned. 
    
    Returns:
        A dict mapping containing a status key which can either be one of: "failure" or "success" and an errors/data key  depending on the status of the request. For example:

        {"status":"success",
         "data":{
            "send":{
                "fee":0.00002,
                "id":"aqQzlkjdfQafld92893adfjdljfa"
            }
         }
        }

    Raises:
        Exception: Only raised if any of the args parameter fields are invalid e.g amount not being a float or fields having an item dict without the field property.
    """

    if not args.get("address") or type(args.get("address")) is not str or not args.get("address").strip():
        raise Exception("address argument must be a valid string identifier.")

    if not args.get("cryptocurrency") or type(args.get("cryptocurrency")) is not str or not args.get("cryptocurrency").strip():
        raise Exception("cryptocurrency argument must be a valid string identifier.")

    if not args.get("amount") or type(args.get("amount")) is not float or args.get("amount") <= 0:
        raise Exception("amount argument must be a valid float and greater than 0.")

    # add validation for fields

    if(not utilities.is_valid_fields(fields)):
        raise Exception("Fields contains a node dict without a 'field' property.")


    query_dict = {
        "operation": "mutation",
        "command": "send",
        "args": args,
        "fields": fields if len(fields) > 0 else [{"field":"id"}, {"field":"cryptocurrency"}, {"field":"status"}, {"field":"address"}, {"field":"amount"}, {"field":"fee"}, {"field":"transaction", "fields":[{"field":"hash"}, {"field":"id"}]}]
    }

    data = utilities.create_request_body(query_dict)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=HTTPBasicAuth(utilities.AUTH['username'], utilities.AUTH['password']), data={"query":data}, params={})
    
    return utilities.parse_response(response)



def buy(args:dict, fields:list=[]):
    """Buy a cryptocurrency
    
    Returns the transaction details after making a request to buy cryptocurrency from the Buycoins marketplace

    Args:
        args (dict):
            Arguments required by the graphql query to buy the currency

            args['cryptocurrency'] (str):
                The cryptocurrency you want to buy.
            args['coin_amount'] (float):
                The amount of cryptocurrency you intend to buy
            args['price'] (str):
                This is the price id retrieved from calling the Prices.list() function and retrieving the id for your buy currency
        
        fields (list):
            The fields you want returned by the graphql query. It defaults to all the query fields if this argument is absent or empty. It is a list of dictionaries. 
            An example field dict is represented as:

            {"field": "estimatedFee"}

            Default fields are:
            [{"field": "estimatedFee"}, {"field": "total"}]

            See fields definition in Readme file for help on writing fields you want returned. 
    
    Returns:
        A dict mapping containing a status key which can either be one of: "failure" or "success" and an errors/data key  depending on the status of the request. For example:

        {"status":"success",
         "data":{
            "send":{
                "status":"processing",
                "id":"aqQzlkjdfQafld92893adfjdljfa"
            }
         }
        }

    Raises:
        Exception: Only raised if any of the args parameter fields are invalid e.g coin_amount not being a float or fields having an item dict without the field property.
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
    """Sell a cryptocurrency
    Returns the transaction details after making a request to sell cryptocurrency on the Buycoins marketplace

    Args:
        args (dict):
            Arguments required by the graphql query to sell the currency

            args['cryptocurrency'] (str):
                The cryptocurrency you want to sell.
            args['coin_amount'] (float):
                The amount of cryptocurrency you intend to sell
            args['price'] (str):
                This is the price id retrieved from calling the Prices.list() function and retrieving the id for your sell currency
        
        fields (list):
            The fields you want returned by the graphql query. It defaults to all the query fields if this argument is absent or empty. It is a list of dictionaries. 
            An example field dict is represented as:

            {"field": "estimatedFee"}

            Default fields are:
            [{"field": "estimatedFee"}, {"field": "total"}]

            See fields definition in Readme file for help on writing fields you want returned. 
    
    Returns:
        A dict mapping containing a status key which can either be one of: "failure" or "success" and an errors/data key  depending on the status of the request. For example:

        {"status":"success",
         "data":{
            "sell":{
                "status":"processing",
                "id":"aqQzlkjdfQafld92893adfjdljfa"
            }
         }
        }

    Raises:
        Exception: Only raised if any of the args parameter fields are invalid e.g coin_amount not being a float or fields having an item dict without the field property.
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
