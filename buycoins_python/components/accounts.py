import requests
from requests.auth import HTTPBasicAuth
from . import utilities

def create(account_name:str, fields:list=[]):
    """Create a new bank account. Requires the account name.

    Returns the created bank account details made from the createDepositAccount mutation call on the API.

    Args:
        account_name (str):
            The account name to be used in creating the new bank account. It is required. 
        
        fields (list):
            The fields you want returned by the graphql query. It defaults to all the mutation fields of the createDepositAccount mutation if this argument is absent or empty. It is a list of dictionaries. 
            An example field dict is represented as:

            {"field": "estimatedFee"}

            Default fields are:
            [{"field":"accountNumber"}, {"field":"accountName"}, {"field":"accountType"}, {"field":"bankName"}, {"field":"accountReference"}]
    
    Returns:
        A dict mapping containing a status key which can either be one of: "failure" or "success" and an errors/data key  depending on the status of the request. For example:

        {"status":"success",
         "data":{
            "createDepositAccount":{
                "accountReference":"afWGFdfa823ladfadfja",
                "accountName":"Chukwuemeka Ajah"
            }
         }
        }

    Raises:
        Exception: Only raised if fields having an item dict without the field property or account_name is an invalid string.
    """
    if(not account_name or type(account_name) is not str or not account_name.strip()):
        raise Exception("Please provide account name to create bank account for")

    query_dict = {
        "operation": "mutation",
        "command": "createDepositAccount",
        "args": {"accountName": account_name},
        "fields": fields if len(fields) > 0 else [{"field":"accountNumber"}, {"field":"accountName"}, {"field":"accountType"}, {"field":"bankName"}, {"field":"accountReference"}]
    }

    data = utilities.create_request_body(query_dict)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=utilities.AUTH, data={"query":data}, params={})
    
    return utilities.parse_response(response)

def createAddress(crypto_currency:str, fields:list=[]):
    """Create a cryptocurrency address to receive money in. You should send this address to your prospective sender

    Returns the newly created cryptocurrency address from making a call on the `createAddress` mutation call on the API.

    Args:
        crypto_currency (str):
            The name of the cryptocurrency you want to create a new address in.  
        
        fields (list):
            The fields you want returned by the graphql query. It defaults to all the mutation fields of the createAddress mutation if this argument is absent or empty. It is a list of dictionaries. 
            An example field dict is represented as:

            {"field": "estimatedFee"}

            Default fields are:
            [{"field":"cryptocurrency"}, {"field":"address"}]
    
    Returns:
        A dict mapping containing a status key which can either be one of: "failure" or "success" and an errors/data key  depending on the status of the request. For example:

        {"status":"success",
         "data":{
            "createAddress":{
                "address":"afWGFdfa823ladfadfja",
                "cryptocurrency":"bitcoin"
            }
         }
        }

    Raises:
        Exception: Only raised if fields having an item dict without the field property or crypto_currency is an invalid string.
    """

    if(not crypto_currency or type(crypto_currency) is not str or not crypto_currency.strip()):
        raise Exception("crypto_currency parameter is compulsory and it is a string.")

    query_dict = {
        "operation": "mutation",
        "command": "createAddress",
        "args": {"cryptocurrency": crypto_currency},
        "fields": fields if len(fields) > 0 else [{"field":"cryptocurrency"}, {"field":"address"}]
    }

    data = utilities.create_request_body(query_dict)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=HTTPBasicAuth(utilities.AUTH['username'], utilities.AUTH['password']), data={"query":data}, params={})
    
    return utilities.parse_response(response)

