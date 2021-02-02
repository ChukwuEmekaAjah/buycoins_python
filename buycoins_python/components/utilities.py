import requests
auth = None

def make_request(url, method='post', headers=auth, params={}, data={}):
    print("making a request now")
    print("auth is", auth)
    return "hello world"