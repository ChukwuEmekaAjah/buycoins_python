import requests
from requests.auth import HTTPBasicAuth
from . import utilities


def list(fields:list = []):
    """Retrieve a list of cryptocurrency prices

    Returns the list of cryptocurrency prices being traded on the Buycoins platform. It utilizes the `getPrices` query on the API.

    Args:
        fields (list):
            The fields you want returned by the graphql query. It defaults to all the query fields of the getPrices query if this argument is absent or empty. It is a list of dictionaries. 
            An example field dict is represented as:

            {"field": "estimatedFee"}

            Default fields are:
            [{"field": "id"}, {"field": "minSell"}]
    
    Returns:
        A dict mapping containing a status key which can either be one of: "failure" or "success" and an errors/data key  depending on the status of the request. For example:

        {"status":"success",
         "data":{
            "postListOrder":{
                "id":"afWGFdfa823ladfadfja",
                "status":"open"
            }
         }
        }

    Raises:
        Exception: Only raised if fields parameter has an item dict without the field property.
    """
    # add validation for fields

    if(not utilities.is_valid_fields(fields)):
        raise Exception("Fields contains a node dict without a 'field' property.")

    query_dict = {
        "operation": "query",
        "command": "getPrices",
        "fields": fields if len(fields) > 0 else [{"field":"id"}, {"field":"cryptocurrency"}, {"field":"sellPricePerCoin"}, {"field":"minSell"}, {"field":"maxSell"}, {"field":"expiresAt"}]
    }


    data = utilities.create_request_body(query_dict)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=HTTPBasicAuth(utilities.AUTH['username'], utilities.AUTH['password']), data={"query":data}, params={})
    
    return utilities.parse_response(response)
