
AUTH = None
API_URL = "https://backend.buycoins.tech/api/graphql"
HEADERS = { 'Accept':'application/json'}


def is_valid_fields(fields):
    """Check validity of dict keys passed into the fields list for expected fields in API calls.

    Returns True if the fields are valid else False

    Args:
        fields (list):
            The fields you want returned by the graphql query. It is a list of dictionaries. 
            
            Example is:
            [{"field": "id"}, {"field": "minSell"}]
    
    Returns:
        A boolean value
        True or False

    """
    for field in fields:
        if not field.get("field"):
            return False
        
        if field.get('args'):
            if type(field.get('args')) is not dict:
                return False
        
        if field.get('fields'):
            return is_valid_fields(field.get('fields'))
    return True

def create_request_body(fields):
    operations = ["query", "mutation"]

    if( not fields.get("operation") in operations):
        raise Exception("Invalid operation {operation}".format(operation=fields["operation"]))

    if (not fields.get("command") or type(fields.get("command")) is not str or not fields.get("command").strip()):
        raise Exception("Invalid command {command}".format(command=fields["command"]))

    query = "{operation} {{ {command}".format(operation=fields["operation"], command=fields["command"])

    if fields.get("args", None) is not None:
        query += "("
        query += parse_args(fields["args"])
        query += ")"

    query += "{{ {fields} }}".format(fields=parse_fields(fields["fields"], []))

    query += "}"
    
    return query

def parse_args(args:dict):
    """Parse arguments passed to a graphql query name or nodes and returns a string of arguments

    Args:
        dict (list):
            The arguments you want passed to your node or query name. An example for retrieving balances is:

            {"cryptocurrency":"bitcoin"}
    
    Returns:
        A string of comma-separated arguments key-value pairs as in the graphql standard like (cryptocurrency: bitcoin, status:open)

    """
    parsed_args = args.items()

    arg_pairs = []

    for pair in parsed_args:
        arg_pairs.append("{}:{}".format(pair[0],pair[1]))

    return ",".join(arg_pairs)

def parse_fields(fields:list=[], fields_array=[]):
    """Parse fields that are expected to be returned in a graphql query and returns a string of fields and their arguments (if any)

    Args:
        fields (list):
            The fields you want returned by an API call. A field dict can contain arguments (for nodes that require arguments). A field can also contain other fields which are the same type as normal fields (for nodes which have child properties).

            [{'field':"cryptocurrency"}, {"field":"price", "args":{"time":13435929, "type":"min"}}, {"field":"fees", "args":{"time":13435929, "type":"min"}, "fields":[{"field":"day"}, {"field":"name"}]}]
    
    Returns:
        A string of comma-separated nodes e.g "cryptocurrency, price(time:1345353, type:min), fees(time:13535, type:min){day, name}"

    """

    for field in fields:
        parsed_fields = "{}".format(field.get("field"))

        if field.get("args") is not None: # check for arguments in field
            parsed_fields += "("
            parsed_fields += parse_args(field.get("args"))
            parsed_fields += ")"

        if field.get("fields") is not None: # check for child nodes
            parsed_fields += "{"
            parsed_fields += parse_fields(field.get("fields"), [])
            parsed_fields += "}"

        fields_array.append(parsed_fields)

    return ",".join(fields_array)


def _get_messages(errors):
    """Parses an API call error response and retrieves messages in the API call response and return it as a list of string messages. 

    Args:
        errors (list):
            The list of errors returned from the unsuccessful API call
    
    Returns:
        A list of messages e.g ["Invalid argument 'cryptocurren' passed to query 'getPrices'"]

    """
    return list(map(lambda error: error.get("message", ""), errors))

def _get_fields(errors):
    """Parses an API call error response and retrieves paths in the API call response and return it as a list of string messages. 

    Args:
        errors (list):
            The list of errors returned from the unsuccessful API call
    
    Returns:
        A list of string paths e.g ["person.age"]

    """
    return list(map(lambda error: (error.get("path", []) and ".".join(error.get("path",[]))) or "", errors))

def _create_error_response(errors):
    """Combines error messages and fields to create an array of reasons for errors and the corresponding fields causing the errors.

    Args:
        errors (list):
            The list of errors returned from the unsuccessful API call
    
    Returns:
        A list of dict reasons e.g [{"reason":"Invalid argument 'cryptocurren' passed to query 'getPrices'", "field":"cryptocurren"}]

    """
    messages = _get_messages(errors)
    fields = _get_fields(errors)
    response = []
    for i in range(len(messages)):
        response.append({"reason":messages[i], "field": fields[i] })
    return response

def parse_response(response):
    """Parses a requests.Response object and returns the corresponding response based the response status code

    Args:
        response (requests.Response):
            The response from the API call
    
    Returns:
        A dict containing a status field and other fields based on the request status code

        Successful responses are in the format shown below:
            {
                "status": "success",
                "data":{
                    "getPrices":{ # the query or mutation name
                        "cryptocurrency":"bitcoin", 
                        "id":"aAQfdl134"
                    }
                }
            }

        Failure responses are in the format given below:
            {
                "status": "failure",
                "errors":[ # parsed error response from API call
                    {
                        "reason":"Invalid argument 'cryptocurren' passed to query 'getPrices'", 
                        "field":"cryptocurren"
                    }
                ]
                "raw":[{"reason":"Invalid argument 'cryptocurren' passed to query 'getPrices'", "field":"cryptocurren"}] # the raw error response from the API call
            }
    """
    jsonResponse = response.json()
    if(response.status_code == 401):
        return {
            "status": "failure",
            "errors": [{"reason": "Invalid credentials", "field":None}],
            "raw": []
        }

    if(response.status_code > 299): # any other type of failed request status code away from standard 200 range.
        return {
            "status": "failure",
            "errors": [{"reason": "Unknown failure", "field":None}],
            "raw": []
        }
    
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