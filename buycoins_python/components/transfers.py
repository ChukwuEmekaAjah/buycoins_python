import requests
from requests.auth import HTTPBasicAuth
from . import utilities

def fees(args:dict, fields:list=[]):
    """
        Retrieve fees for sending a cryptocurrency to an address
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
    """
        Send cryptocurrency to a cryptocurrency address
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