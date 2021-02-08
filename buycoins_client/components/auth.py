from . import utilities


def setup(public_key, secret_key):
    """Set up authentication data for making calls to the API endpoint.

    Returns True if the authentication credentials were set. However, the correctness of the public and secret keys can only be confirmed at the point of making calls to the API.

    Args:
        public_key (str):
            The public key retrieved from the Buycoins app settings page after access is provided by the Buycoins support team
        
        secret_key (str):
            The secret key retrieved from the Buycoins app settings page after access is provided by the Buycoins support team
    
    Returns:
        A boolean (True) indicating that the credentials were successfully setup.

    Raises:
        Exception: Only raised if public_key or secret_key parameters are not valid strings.
    """
    if not public_key or type(public_key) is not str:
        raise Exception("Invalid public key. Public key should be a string")
    if not secret_key or type(secret_key) is not str:
        raise Exception("Invalid secret key. Secret key should be a string")
    
    utilities.AUTH = {'username': public_key, 'password': secret_key}
    return True # use requests auth for basic authentication