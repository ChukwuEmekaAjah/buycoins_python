import requests
auth = None

def make_request(url, method='post', headers={'Content-type':'application/json', 'Accepts':'application/json'}, params={}, data={}):
    response = requests.request(method, url, headers=headers, auth=auth, data=data, params=params)
    return response


def _get_messages(errors):
    return list(map(lambda error: error.message, errors))

def _get_fields(errors):
    return list(map(lambda error: (error.path and error.path.join) or "", errors))

def _create_error_response(errors):
    messages = _get_messages(errors)
    fields = _get_fields(errors)
    response = []
    for i in range(len(messages)):
        response.append({"reason":messages[i], "field": fields[i] })
    return response

def parse_response(response):
    jsonResponse = response.json()
    if(jsonResponse.errors):
        return {
            "status": "failure",
            "errors": _create_error_response(jsonResponse.errors),
            "raw": jsonResponse.errors
        }
    else:
        return {
            "status": "success",
            "data": response.data
        }