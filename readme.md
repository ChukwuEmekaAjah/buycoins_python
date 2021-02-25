# Buycoins Python Library


The Buycoins GraphQL API Python library provides convenient access to the Buycoins API from
applications written in the Python language. It includes a pre-defined set of
functions for API resources that initialize themselves dynamically from API
responses which makes it compatible with a wide range of versions of the Buycoins
API.

<b>You don't need to know GraphQL to be able to use the package. </b> Your basic understanding of calling functions and assigning variables in Python is more than enough. 

## Documentation

See the [Buycoins GraphQL API docs](https://developers.buycoins.africa/).

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```sh
pip install --upgrade buycoins_client
```

Install from source with:

```sh
python setup.py install
```

### Requirements

-   Python 3+ (PyPy supported)

## Usage

The library needs to be configured with your account's public and secret keys which is
available in your [Buycoins App settings][api-keys] after you make a request to [Buycoins support](mailto:support@buycoins.africa).
value:

```python
import buycoins_client as buycoins
buycoins.Auth.setup("public_key_...", "secret_key_...")

# list personal orders
my_orders = buycoins.Orders.list_my_orders(status="open", fields=[])

# list market book orders
my_orders = buycoins.Orders.list_market_orders()

```

## Modules
The package contains 6 core modules with related functions to adequately represent the queries and mutations on the main API. You don't need to know GraphQL to be able to use the package; this is because a dict to graphql parser has been created in the package. All you just have to do is specify arguments (where need be) or fields you want retrieved (else all the associated query fields are returned).

These modules are:
- Auth - For authentication setup and modification. Contains a single function for setting up public and secret keys.
- Accounts - For creating cryptocurrency addresses and virtual bank accounts
- Balances - For retrieving your balances in all the cryptocurrencies supported as well as for a single cryptocurrency of your choice
- Orders - For placing orders on the marketplace, viewing the market book as well as your personal orders on the platform
- Prices - For retrieving cryptocurrency prices on the platform
- Transfers - For checking transfer fees, sending, buying and selling cryptocurrencies via the API. 

### Client Responses
The Client offers two kinds of responses. They are: `failure` and `success` responses. A failure response occurs when the API returns back a response with errors. A success response occurs when the API returns the result expected by the call. Every type of response has a <b>status</b> key that can only be any of `success` or `failure`. Both responses are `dicts` and are represented as follows:


A success response always has a `data` key indicating the data returned from the API. 

##### Success Response
```python

    >>> import buycoins_client as buycoins

    >>> buycoins.Auth.setup("public_key_...", "secret_key_...")

    >>> currency_prices = buycoins.Prices.list()

    >>> print(currency_prices)

    >>> {
        "status":"success",
        "data":
            {"getPrices":[{
                "id":"QnV5Y29pbnNQcmljZS1mM2ZhOWI2Yy00MmM4LTQxMzAtOThmZC0zZGMwYjRjMmRlNjQ=",
                "cryptocurrency":"bitcoin",
                "sellPricePerCoin":"17827839.315",
                "minSell":"0.001",
                "maxSell":"0.35190587",
                "expiresAt":1612391202
            }]
            }
        }

```

The `raw` field of a `failure` response is the raw error message from the API. However, an error response always has an `errors` key that's a list of errors. This list of errors contains a `dict` with keys `reason` (why the error happened) and `field` (where the error happened). 

##### Failure Response
```python

    >>> import buycoins_client as buycoins

    >>> buycoins.Auth.setup("public_key_...", "secret_key_...")

    >>> currency_prices = buycoins.Prices.list()

    >>> print(currency_prices)

    >>> #if the request were to fail by any means, the output of print would be:

    >>> {
        "status":"failure",
        "errors":[{
            "reason":"Field 'cryptocrrency' doesn't exist on type 'BuycoinsPrice'",
            "field":"query.getPrices.cryptocrrency"}],
        "raw":[{"message":"Field 'cryptocrrency' doesn't exist on type 'BuycoinsPrice'","locations":[{"line":1,"column":23}],"path":["query","getPrices","cryptocrrency"],"extensions":{"code":"undefinedField","typeName":"BuycoinsPrice","fieldName":"cryptocrrency"}}]
```

## Modules API

### Fields

An explanation on how to choose the data fields returned by each mutation or query
Every  `query` or `mutation` call on the package takes a `fields` parameter that is optional. If the `fields` parameter is not provided, the API call defaults to returning all the data the `query` or `mutation` can provide since the API is a GraphQL API and developers are allowed to indicate the fields they want returned. 

Since the package is a wrapper on the main client and not all developers understand or want to learn how to use GraphQL, the package contains a parser that transforms an array of fields to an equivalent GraphQL schema. The `fields` parameter which is a list only accepts `dicts` with only one required `dict` key: `field`. The two other keys are `args` and `fields`. `args` is equivalent to arguments being passed to a GraphQL node. It is a `dict` containing the argument name with its corresponding value. The `fields` key is a recursive pattern of the `fields` data structure. It is also a `list` just like the parent `fields` parameter. The nesting can be done to any depth of choice as in GraphQL.

The fields parameter is shown below:

```python

    >>> fields = [
        {'field':"cryptocurrency"}, 
        {"field":"id"}}, 
        {"field":"minSell"}
    ]

    # An example request
    >>> currency_prices = buycoins.Prices.list(fields=fields) # This would normally return all the data available in the getPrices Query

    >>> print(currency_prices)

    >>> {
        "data":{
            "getPrices":[{
                "id": "aEDA324fafdjlfda",
                "cryptocurrency":"bitcoin",
                "minSell":0.002
            }, {
                "id": "qAF82fa2fal3ai",
                "cryptocurrency":"litecoin",
                "minSell":0.002
            }
            ]
        }
    }

    >>> fields_with_args = [
        {'field':"cryptocurrency"}, 
        {"field":"price", "args":{"time":13435929, "type":"min"}}
        ]

    >>> fields_with_other_fields = [
        {'field':"cryptocurrency"}, 
        {"field":"price", "args":{"time":13435929, "type":"min"}}, 
        {"field":"fees", "args":{"time":13435929, "type":"min"}, 
        "fields":[
            {"field":"day"}, 
            {"field":"name"}]
        }]

    >>> # an example of field with sub-fields with getMarketBook query

    >>> fields = [
        {"field":"dynamicPriceExpiry"}, 
        {"field":"orders", "fields":[
            {"field":"edges", "fields": [
                {"field":"node", "fields":[
                    {"field":"id"}, 
                    {"field":"cryptocurrency"}, 
                    {"field":"coinAmount"}, 
                    {"field":"side"}, 
                    {"field":"status"}, 
                    {"field":"createdAt"}, 
                    {"field":"pricePerCoin"}, 
                    {"field":"priceType"}, 
                    {"field":"staticPrice"}, 
                    {"field":"dynamicExchangeRate"}
                    ]
                }]
            }]
        }]

    >>> market_orders = buycoins.Orders.list_market_orders(fields=fields)

    >>> print(market_orders)

```

The parser for the fields-graphql schema parser can be found in the `/buycoins_client/components/utilities.py` file and can be copied to create similar functionality in any package of choice. 

### Auth

It requires that you utilize the public and secret keys as specified in the [Authentication documentation](https://developers.buycoins.africa/introduction/authentication)

To set up authentication credentials just call the `setup` function of the `Auth` module with the public and secret keys respectively. It raises an exception if any of both parameters is not provided or aren't of type `str`. You can set it up as follows:
```python
>>> import buycoins_client as buycoins

>>> buycoins.Auth.setup("public_key_...", "secret_key_...")

```

### Accounts
The `Accounts` module is used for creating virtual bank accounts and for creating cryptocurrency addresses. It contains two functions, these functions are: `create` for creating a virtual account and `create_address` for creating a cryptocurrency address. For creating a virtual account, see the documentation from the  API here [Create a virtual account](https://developers.buycoins.africa/naira-token-account/create-virtual-deposit-account).
For creating a cryptocurrency address, see the main documentation here: [Create cryptocurrency address](https://developers.buycoins.africa/receiving/create-address)

#### create (<b> This feature is currently disabled </b>)
This function takes a single compulsory parameter which is the account name to use for the new virtual bank account. Just like in GraphQL where you specify the fields you want returned, it accepts an optional fields parameter that's a list. If a fields list is not provided, it defaults to returning all the data the `mutation` can return. The function raises an exception if a valid `account_name` parameter is not provided or the `fields` parameter provided contains an invalid field dict.

It returns the newly created virtual bank account `dict` or an error response `dict` if the request to the Buycoins API fails.

```python
>>> import buycoins_client as buycoins

>>> buycoins.Auth.setup("public_key_...", "secret_key_...")

>>> new_account = buycoins.Accounts.create("Chukwuemeka Ajah")

>>> print(new_account)

```

#### create_address
Creates a cryptocurrency address to receive money in. You should send this address to your prospective sender.

This function takes a single compulsory parameter which is the cryptocurrency name you want to create an address for. Just like in GraphQL where you specify the fields you want returned, it accepts an optional fields parameter that's a list. If a fields list is not provided, it defaults to returning all the data the `createAddress mutation` can return. The function raises an exception if a valid `crypto_currency` parameter is not provided or the `fields` parameter provided contains an invalid field dict.

It returns the newly created cryptocurrency address `dict` or an error response `dict` if the request to the Buycoins API fails.

```python
>>> import buycoins_client as buycoins

>>> buycoins.Auth.setup("public_key_...", "secret_key_...")

>>> new_address = buycoins.Accounts.create_address("litecoin")

>>> print(new_address)

>>> {
        'status': 'success', 
        'data': {
            'createAddress': {
                'cryptocurrency': 'litecoin', 
                'address': 'MTyrRGZKfo1jNJvfH3RWnQ5qjivLT2UyYn'
            }
        }
    }

```

### Balances
The `Balances` module is used for retrieving your account balances in different cryptocurrencies on the Buycoins platform. It contains two functions. They are `get` for retrieving a single cryptocurrency balance and `list` for retrieving balances of all the cryptocurrencies you own. 
The Buycoins documentation on retrieving balances can be found [here](https://developers.buycoins.africa/sending/account-balances)

#### get
Retrieve a single cryptocurrency balance on your wallets

This function takes a single compulsory parameter which is the cryptocurrency name you want to get its balance. Just like in GraphQL where you specify the fields you want returned, it accepts an optional fields parameter that's a list. If a fields list is not provided, it defaults to returning all the data the `getBalances query` can return. The function raises an exception if a valid `cryptocurrency` string parameter is not provided or the `fields` parameter provided contains an invalid field dict.

It returns the wallet balance in the specified currency.

```python
>>> import buycoins_client as buycoins

>>> buycoins.Auth.setup("public_key_...", "secret_key_...")

>>> wallet_balance = buycoins.Balances.get("litecoin", fields=[{"field":"confirmedBalance"}])

>>> print(wallet_balance)

>>> {
        'status': 'success', 
        'data': {
            'getBalances': [
               {
                    'confirmedBalance': '0.0'
                }
            ]
        }
    }

```

#### list
Retrieve a list of balances in all supported cryptocurrencies you own on your wallet.

This function takes no compulsory parameter. Just like in GraphQL where you specify the fields you want returned, it accepts an optional fields parameter that's a list. If a fields list is not provided, it defaults to returning all the data the `getBalances query` can return. The function raises an exception if the `fields` parameter provided contains an invalid field dict.

It returns your wallet balances in all the cryptocurrencies that are supported on the Buycoins platform.

```python
>>> import buycoins_client as buycoins

>>> buycoins.Auth.setup("public_key_...", "secret_key_...")

>>> wallet_balances = buycoins.Balances.list()

>>> print(wallet_balances)

>>> {
        'status': 'success', 
        'data': {
            'getBalances': [
                {
                    'id': 'QWNjb3VudC0=', 'cryptocurrency': 'usd_tether', 'confirmedBalance': '0.0'
                }, 
                {
                    'id': 'QWNjb3VudC0=', 'cryptocurrency': 'naira_token', 'confirmedBalance': '0.0'
                }, 
                {
                    'id': 'QWNjb3VudC0=', 'cryptocurrency': 'bitcoin', 'confirmedBalance': '0.0'
                }, 
                {
                    'id': 'QWNjb3VudC0=', 'cryptocurrency': 'ethereum', 'confirmedBalance': '0.0'
                }, 
                {
                    'id': 'QWNjb3VudC0=', 'cryptocurrency': 'litecoin', 'confirmedBalance': '0.0'
                }, 
                {
                    'id': 'QWNjb3VudC0=', 'cryptocurrency': 'usd_coin', 'confirmedBalance': '0.0'
                }
            ]
        }
    }

```

### Prices
The `Prices` module is used for retrieving the current prices of cryptocurrencies supported on the Buycoins platform. It contains only one function. The function name is `list`. 

The Buycoins documentation on retrieving the prices of cryptocurrencies can be found [here](https://developers.buycoins.africa/placing-orders/buy)

#### list
Retrieve a list of cryptocurrency prices

This function takes no compulsory parameter. Just like in GraphQL where you specify the fields you want returned, it accepts an optional fields parameter that's a list. If a fields list is not provided, it defaults to returning all the data the `getPrices query` can return. The function raises an exception if the `fields` parameter provided contains an invalid field dict.

It returns the current prices of cryptocurrencies supported on the Buycoins platform.

```python
>>> import buycoins_client as buycoins

>>> buycoins.Auth.setup("public_key_...", "secret_key_...")

>>> currency_prices = buycoins.Prices.list()

>>> print(currency_prices)

>>> {
    'status': 'success', 
    'data': {
        'getPrices': [{
            'id': 'QnV5Y29pbnNQcmljZS0zZjVmZmUwMS1hM2M1LTRlNTgtODY0Yi1jYmM0NWNkZmY3ZWM=', 
            'cryptocurrency': 'bitcoin', 
            'sellPricePerCoin': '23865583.5', 
            'minSell': '0.0002', 
            'maxSell': '4.54256862', 
            'expiresAt': 1614295216
            }, 
            {
            'id': 'QnV5Y29pbnNQcmljZS0wN2RkMDNmYi01YWM1LTRkMTgtOWExMy1kZTZjYWFkMDFmMmQ=', 
            'cryptocurrency': 'ethereum', 
            'sellPricePerCoin': '753528.6', 
            'minSell': '0.005', 
            'maxSell': '20.32703634', 
            'expiresAt': 1614295217
            }, 
            {
                'id': 'QnV5Y29pbnNQcmljZS1lZDdmNzgxNi1kMTUyLTQ2ZjUtYTc1ZS04OTc5NjEzY2VhN2M=', 
                'cryptocurrency': 'litecoin', 'sellPricePerCoin': '91995.75', 'minSell': '0.05', 
                'maxSell': '503.39025025', 'expiresAt': 1614295220
            }, 
            {'id': 'QnV5Y29pbnNQcmljZS1iZGY0OGU4NC1mYTliLTQyNTAtYjc4Ny1kYzRmZjFiNzkyMDY=', 
            'cryptocurrency': 'usd_coin', 'sellPricePerCoin': '495.099', 'minSell': '5', 
            'maxSell': '45090.08437014', 'expiresAt': 1614295218
            }]
        }
    }

```


### Transfers
The `Transfers` module contains functions for retrieving cryptocurrency transfer fees, sending cryptocurrencies, placing orders for buying as well as selling cryptocurrencies. It implements GraphQL API calls to the Buycoins API as stated in the following links of the API documentation.
- fees [getEstimatedNetworkFee documentation](https://developers.buycoins.africa/sending/network-fees)
- send [Send cryptocurrency documentation](https://developers.buycoins.africa/sending/send)
- buy [Buy documentation](https://developers.buycoins.africa/placing-orders/buy)
- sell [Sell documentation](https://developers.buycoins.africa/placing-orders/sell)

#### fees
Retrieve fees for sending a cryptocurrency to an address

This function takes a single compulsory parameter which is a dict containing the required arguments needed for retrieving the transfer fee when a `getEstimatedNetworkFee query` is called on the Buycoins API. These arguments are: `cryptocurrency` and `amount` as stated in the main API documentation.

Just like in GraphQL where you specify the fields you want returned, it accepts an optional fields parameter that's a list. If a fields list is not provided, it defaults to returning all the data the `getEstimatedNetworkFee query` can return. The function raises an exception if an invalid `args` field value is provided or required field in the dict is absent or the `fields` parameter provided contains an invalid field dict.

It returns the fees in the specified cryptocurrency required to make a transfer possible on the Buycoins platform. 

```python
>>> import buycoins_client as buycoins

>>> buycoins.Auth.setup("public_key_...", "secret_key_...")

>>> fees = buycoins.Transfers.fees({"cryptocurrency":"bitcoin", "amount":0.02}, fields=[{"field":"estimatedFee"}])

>>> print(fees)

>>> {
        'status': 'success', 
        'data': {
            'getEstimatedNetworkFee': {
                'estimatedFee': '0.00062'
            }
        }
    }

```

#### send
Send cryptocurrency to a cryptocurrency address

This function takes a single compulsory parameter which is a dict containing the required arguments needed for sending cryptocurrency to a specified address via the `send mutation` on the Buycoins API documentation. These arguments are: `cryptocurrency`, `address` and `amount` as stated in the main API documentation.

Just like in GraphQL where you specify the fields you want returned, it accepts an optional fields parameter that's a list. If a fields list is not provided, it defaults to returning all the data the `send mutation` can return. The function raises an exception if an invalid `args` field value is provided or required field in the `args` dict is absent or the `fields` parameter provided contains an invalid field dict.

It returns the transaction details. 

```python
import buycoins_client as buycoins

buycoins.Auth.setup("public_key_...", "secret_key_...")

transaction_info = buycoins.Transfers.send({"cryptocurrency":"bitcoin", "amount":0.02, "address":"vdADFaj7f89dfkadf="})

print(transaction_info)

```

#### buy
Buy cryptocurrency on the Buycoins platform.

This function takes a single compulsory parameter which is a dict containing the required arguments needed for buying cryptocurrency via the `buy mutation` on the Buycoins API documentation. These arguments are: `cryptocurrency`, `price` and `coin_amount` as stated in the main API documentation. The `price` field is the `id` of the cryptocurrency price returned from calling `Prices.get` function for the cryptocurrency.

Just like in GraphQL where you specify the fields you want returned, it accepts an optional fields parameter that's a list. If a fields list is not provided, it defaults to returning all the data the `buy mutation` can return. The function raises an exception if an invalid `args` field value is provided or required field in the `args` dict is absent or the `fields` parameter provided contains an invalid field dict.

It returns the transaction details. 

```python
import buycoins_client as buycoins

buycoins.Auth.setup("public_key_...", "secret_key_...")

transaction_info = buycoins.Transfers.buy({"cryptocurrency":"bitcoin", "coin_amount":0.02, "price":"vdADFaj7f89dfkadf="})

print(transaction_info)

```

#### sell
Sell a cryptocurrency on the Buycoins platform.

This function takes a single compulsory parameter which is a dict containing the required arguments needed for selling cryptocurrency via the `sell mutation` on the Buycoins API documentation. These arguments are: `cryptocurrency`, `price` and `coin_amount` as stated in the main API documentation. The `price` field is the `id` of the cryptocurrency price returned from calling `Prices.get` function for the cryptocurrency.

Just like in GraphQL where you specify the fields you want returned, it accepts an optional fields parameter that's a list. If a fields list is not provided, it defaults to returning all the data the `sell mutation` can return. The function raises an exception if an invalid `args` field value is provided or required field in the `args` dict is absent or the `fields` parameter provided contains an invalid field dict.

It returns the transaction details. 

```python
import buycoins_client as buycoins

buycoins.Auth.setup("public_key_...", "secret_key_...")

transaction_info = buycoins.Transfers.sell({"cryptocurrency":"bitcoin", "coin_amount":0.02, "price":"vdADFaj7f89dfkadf="})

print(transaction_info)

```

### Orders
The `Orders` module contains functions for retrieving personal orders made on the platform, marketplace orders as well as posting personal and marketplace orders. It implements GraphQL API calls to the Buycoins API as stated in the following links of the API documentation.

- list_my_orders [Get list orders documentation](https://developers.buycoins.africa/p2p/get-orders)
- list_market_orders [Get market book documentation](https://developers.buycoins.africa/p2p/get-market-book)
- post_limit_order [Post limit order documentation](https://developers.buycoins.africa/p2p/post-limit-order)
- post_market_order [Post market order documentation](https://developers.buycoins.africa/p2p/post-market-order)


#### list_my_orders
Retrieve a list of orders made by you on the platform. 

This function takes a single compulsory parameter which is a string indicating the status of the order required for retrieving limit orders using the `getOrders query` on the Buycoins API documentation. These argument is `status` and it defaults to `open`. It can be any of `open` or `completed`.

Just like in GraphQL where you specify the fields you want returned, it accepts an optional fields parameter that's a list. If a fields list is not provided, it defaults to returning all the data the `getOrders query` can return. The function raises an exception if an invalid `status` value is provided or the `fields` parameter provided contains an invalid field dict.

It returns all the limit orders made by you on the Buycoins platform.

```python
>>> import buycoins_client as buycoins

>>> buycoins.Auth.setup("public_key_...", "secret_key_...")

>>> orders = buycoins.Orders.list_my_orders(status="completed")

>>> print(orders)

>>> {
        'status': 'success', 
        'data': {
            'getOrders': {
                'dynamicPriceExpiry': 1614296116, 
                'orders': {
                    'edges': []
                }
            }
        }
    }
```

#### list_market_orders
Retrieve a list of orders made on the marketplace platform.

This function <b>no</b> compulsory parameters. It's a call on the `getMarketBook query` on the Buycoins API documentation. 

Just like in GraphQL where you specify the fields you want returned, it accepts an optional fields parameter that's a list. If a fields list is not provided, it defaults to returning all the data the `getMarketBook query` can return. The function raises an exception if `fields` parameter provided contains an invalid field dict.

It returns all the limit orders made by you on the Buycoins platform.

```python
>>> import buycoins_client as buycoins

>>> buycoins.Auth.setup("public_key_...", "secret_key_...")

>>> orders = buycoins.Orders.list_market_orders()

>>> print(orders)

>>> {
        'status': 'success', 
        'data': {
            'getMarketBook': {
                'dynamicPriceExpiry': 1614296236, 
                'orders': {
                    'edges': [
                        {
                            'node': {
                                'id': 'UG9zdE9yZGVyLTg5NDUxNTM2LWU1MzAtNDY2OS1hNDZjLWFhYWE5MjdlY2JlYw==', 
                                'cryptocurrency': 'bitcoin', 
                                'coinAmount': '0.0005', 
                                'side': 'sell', 
                                'status': 'active', 
                                'createdAt': 1614291760, 
                                'pricePerCoin': '26599999.0', 
                                'priceType': 'static', 
                                'staticPrice': '2659999900', 
                                'dynamicExchangeRate': None
                            }
                        },
                        {
                            'node': {
                                'id': 'UG9zdE9yZGVyLWJhNTMxYTUyLWU3ZGUtNDU4Yi05MmNhLWYxMTMxYzFlOGQ3NA==', 
                                'cryptocurrency': 'bitcoin', 
                                'coinAmount': '0.006', 
                                'side': 'sell', 
                                'status': 'active', 
                                'createdAt': 1614273600, 
                                'pricePerCoin': '25500000.0', 
                                'priceType': 'static', 
                                'staticPrice': '2550000000', 
                                'dynamicExchangeRate': None
                            }
                        }
                    ]
                }
            }
        }
    }

```

#### post_limit_order
Post a limit order and have the transaction details returned

This function takes a single compulsory parameter which is a dict containing the required arguments needed for posting an order via the `postLimitOrder mutation` on the Buycoins API documentation. These arguments are: `cryptocurrency`, `orderSide`, `priceType`, `staticPrice`, `dynamicExchangeRate`  and `coinAmount` as stated in the main API documentation. The `orderSide` can only be either of `buy` or `sell`. The `priceType` can only be either of `static` or `dynamic`. The `staticPrice` and `dynamicExchangeRate` arguments are <b>optional</b> as stated in the API. 

The function raises an exception if a valid `args` parameter argument is not provided or the `fields` parameter provided contains an invalid field dict.

```python
import buycoins_client as buycoins

buycoins.Auth.setup("public_key_...", "secret_key_...")

posted_order = buycoins.Orders.post_limit_order({"orderSide":"buy", "cryptocurrency":"bitcoin","coinAmount":0.002, "priceType":"dynamic"})

print(posted_order)

```

#### post_market_order
Post a market order and have the transaction details returned

This function takes a single compulsory parameter which is a dict containing the required arguments needed for posting an order via the `postMarketOrder mutation` on the Buycoins API documentation. These arguments are: `cryptocurrency`, `orderSide`, and `coinAmount` as stated in the main API documentation. The `orderSide` can only be either of `buy` or `sell`. 

The function raises an exception if a valid `args` parameter argument is not provided or the `fields` parameter provided contains an invalid field dict.

```python
import buycoins_client as buycoins

buycoins.Auth.setup("public_key_...", "secret_key_...")

posted_order = buycoins.Orders.post_market_order({"orderSide":"buy", "cryptocurrency":"bitcoin", "coinAmount":0.002})

print(posted_order)

```


### Testing

All tests for the modules are in the tests folder. In order to run the tests, run the command below in a shell within the project folder.

```bash
    python -m unittest discover tests  
```

or

```bash
    pytest
```
### Handling exceptions

Invalid parameter types or absent parameters without a default raise an Exception. All excepts are of the generic Exception class. 

### Per-request Configuration

Configure individual requests with keyword arguments. 
Also, make sure to have called the `Auth.setup` function at the beginning of your code file with your public and secret keys before making any calls to the API else the package would raise an exception.

```python
import buycoins_client as buycoins

# buy cryptocurrency
response = buycoins.Orders.buy(args={"price":"QnV5Y29pbnNQcmljZS0zOGIwYTg1Yi1jNjA1LTRhZjAtOWQ1My01ODk1MGVkMjUyYmQ=", "coin_amount":0.02, "cryptocurrency":"bitcoin"})

```
