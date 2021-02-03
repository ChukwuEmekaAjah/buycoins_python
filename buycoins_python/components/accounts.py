import requests
from requests.auth import HTTPBasicAuth
from . import utilities

def create(account_name:str):
    """
        Create a new bank account. Requires the account name.
    """
    if(not account_name or type(account_name) is not str or not account_name.strip()):
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
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=utilities.AUTH, data={"query":data}, params={})
    
    return utilities.parse_response(response)

def createAddress(crypto_currency:str):
    """
        Create a cryptocurrency address to receive money in. You should send this address to your prospective sender
    """

    if(not crypto_currency or type(crypto_currency) is not str or not crypto_currency.strip()):
        raise Exception("crypto_currency parameter is compulsory and it is a string.")

    data = """
        mutation {{
            createAddress(cryptocurrency: {crypto_currency}) {{
                cryptocurrency
                address
            }}
        }}
    """.format(crypto_currency=crypto_currency)

    if(not utilities.AUTH):
        raise Exception("Please set up your public and secret keys using buycoins_python.Auth.setup function.")

    response = requests.post(utilities.API_URL, headers=utilities.HEADERS, auth=HTTPBasicAuth(utilities.AUTH['username'], utilities.AUTH['password']), data={"query":data}, params={})
    
    return utilities.parse_response(response)
