
AUTH = None
API_URL = "https://backend.buycoins.tech/api/graphql"
HEADERS = { 'Accept':'application/json'}


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

    query += "{{ {fields} }}".format(fields=parse_fields(fields["fields"]))

    query += "}"

    return query

def parse_args(args:dict):

    parsed_args = args.items()

    arg_pairs = []

    for pair in parsed_args:
        arg_pairs.append("{}:{}".format(pair[0],pair[1]))

    return ",".join(arg_pairs)

def parse_fields(fields, fields_array=[]):
    
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