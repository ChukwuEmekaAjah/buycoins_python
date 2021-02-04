import requests
from requests.auth import HTTPBasicAuth
from . import utilities

def get(cryptocurrency:str, fields:list=[]):
    """
        Retrieve a single cryptocurrency balance on your wallets
    """

    if not cryptocurrency or type(cryptocurrency) is not str or not cryptocurrency.strip():
        raise Exception("cryptocurrency argument must be a valid string identifier.")

    # add validation for fields
    if(not utilities.is_valid_fields(fields)):
        raise Exception("Fields contains a node dict without a 'field' property.")

    query_dict = {
        "operation": "query",
        "command": "getBalances",
        "args": {"cryptocurrency": cryptocurrency},
        "fields": fields if len(fields) > 0 else [{"field":"id"}, {"field":"cryptocurrency"}, {"field":"confirmedBalance"}]
    }

    data = utilities.create_request_body(query_dict)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=HTTPBasicAuth(utilities.AUTH['username'], utilities.AUTH['password']), data={"query":data}, params={})
    
    return utilities.parse_response(response)


def list(fields:list = []):
    """
        Retrieve a list of balances in all supported cryptocurrencies

        If fields parameter is empty, it defaults to retrieving all the fields
    """
    # add validation for fields

    if(not utilities.is_valid_fields(fields)):
        raise Exception("Fields contains a node dict without a 'field' property.")

    query_dict = {
        "operation": "query",
        "command": "getBalances",
        "fields": fields if len(fields) > 0 else [{"field":"id"}, {"field":"cryptocurrency"}, {"field":"confirmedBalance"}]
    }

    data = utilities.create_request_body(query_dict)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=HTTPBasicAuth(utilities.AUTH['username'], utilities.AUTH['password']), data={"query":data}, params={})
    
    return utilities.parse_response(response)
