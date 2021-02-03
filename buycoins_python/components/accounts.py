import requests
from . import utilities

def create(account_name:str):
    """
        Create a new bank account. Requires the account name.
    """
    if(not account_name or not account_name.strip()):
        raise Exception("Please provide account name to create bank account for")

    data = """
        mutation {{
            createDepositAccount(accountName: {account_name}) {{
                accountNumber
                accountName
                accountType
                bankName
                accountReference
            }}
        }}
    """.format(account_name=account_name)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=utilities.AUTH, data=data, params={})
    
    return utilities.parse_response(response)