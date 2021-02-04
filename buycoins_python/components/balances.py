import requests
from requests.auth import HTTPBasicAuth
from . import utilities

def get(cryptocurrency:str, fields:list=[]):
    """Retrieve a single cryptocurrency balance on your wallets

    Returns balance in the specified currency. This is a call on the `getBalances` query with the `cryptocurrency` argument.

    Args:
        cryptocurrency (str):
            The cryptocurrency you own on the platform. E.g bitcoin or ethereum.
        
        fields (list):
            The fields you want returned by the graphql query. It defaults to all the query fields of the getBalances query if this argument is absent or empty. It is a list of dictionaries. 
            An example field dict is represented as:

            {"field": "estimatedFee"}

            Default fields are:
            [{"field":"id"}, {"field":"cryptocurrency"}, {"field":"confirmedBalance"}]
    
    Returns:
        A dict mapping containing a status key which can either be one of: "failure" or "success" and an errors/data key  depending on the status of the request. For example:

        {"status":"success",
         "data":{
            "getBalances":{
                "id":"afWGFdfa823ladfadfja",
                "cryptocurrency":"bitcoin"
            }
         }
        }

    Raises:
        Exception: Only raised if fields having an item dict without the field property.
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
    """Retrieve a list of balances in all supported cryptocurrencies

    Returns your balances in all the cryptocurrencies you own. This is a call on the `getBalances` query.

    Args:
        fields (list):
            The fields you want returned by the graphql query. It defaults to all the query fields of the getBalances query if this argument is absent or empty. It is a list of dictionaries. 
            An example field dict is represented as:

            {"field": "estimatedFee"}

            Default fields are:
            [{"field":"id"}, {"field":"cryptocurrency"}, {"field":"confirmedBalance"}]
    
    Returns:
        A dict mapping containing a status key which can either be one of: "failure" or "success" and an errors/data key  depending on the status of the request. For example:

        {"status":"success",
         "data":{
            "getBalances":{
                "id":"afWGFdfa823ladfadfja",
                "cryptocurrency":"bitcoin"
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
        "command": "getBalances",
        "fields": fields if len(fields) > 0 else [{"field":"id"}, {"field":"cryptocurrency"}, {"field":"confirmedBalance"}]
    }

    data = utilities.create_request_body(query_dict)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=HTTPBasicAuth(utilities.AUTH['username'], utilities.AUTH['password']), data={"query":data}, params={})
    
    return utilities.parse_response(response)
