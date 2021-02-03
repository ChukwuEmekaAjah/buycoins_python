import requests

AUTH = None
API_URL = "https://backend.buycoins.tech/api/graphql"
HEADERS = {'Content-type':'application/json', 'Accepts':'application/json'}

def make_request(url, method='post', headers={'Content-type':'application/json', 'Accepts':'application/json'}, params={}, data={}):
    response = requests.request(method, url, headers=headers, auth=auth, data=data, params=params)
    return response


def _get_messages(errors):
    return list(map(lambda error: error.get("message", ""), errors))

def _get_fields(errors):
    return list(map(lambda error: (error.get("path", []) and ".".join(error.get("path",[]))) or "", errors))

def _create_error_response(errors):
    messages = _get_messages(errors)
    fields = _get_fields(errors)
    response = []
    for i in range(len(messages)):
        response.append({"reason":messages[i], "field": fields[i] })
    return response

def parse_response(response):
    jsonResponse = response.json()
    
    if(jsonResponse.get("errors")):
        return {
            "status": "failure",
            "errors": _create_error_response(jsonResponse.get("errors", [])),
            "raw": jsonResponse.get('errors', [])
        }
    else:
        return {
            "status": "success",
            "data":jsonResponse.get("data",{})
        }