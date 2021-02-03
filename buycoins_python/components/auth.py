from . import utilities
def setup(public_key, secret_key):
    if not public_key or type(public_key) is not str:
        raise Exception("Invalid public key. Public key should be a string")
    if not secret_key or type(secret_key) is not str:
        raise Exception("Invalid secret key. Secret key should be a string")
    
    utilities.AUTH = {'username': public_key, 'password': secret_key}
    return {'username': public_key, 'password': secret_key} # use requests auth for basic authentication