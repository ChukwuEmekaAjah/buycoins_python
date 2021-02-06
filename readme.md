# Buycoins Python Library


The Buycoins GraphQL API Python library provides convenient access to the Buycoins API from
applications written in the Python language. It includes a pre-defined set of
functions for API resources that initialize themselves dynamically from API
responses which makes it compatible with a wide range of versions of the Buycoins
API.

## Documentation

See the [Buycoins GraphQL API docs](https://developers.buycoins.africa/).

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```sh
pip install --upgrade buycoins_python
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
import buycoins_python as buycoins
buycoins.Auth.setup("public_key_...", "secret_key_...")

# list personal orders
my_orders = buycoins.Orders.list_my_orders(status="open", fields=[])

# list market book orders
my_orders = buycoins.Orders.list_market_orders()

```

### Modules
The package contains 6 core modules with related functions to adequately represent the queries and mutations on the main API. You don't need to know GraphQL to be able to use the package; this is because a dict to graphql parser has been created in the package. All you just have to do is specify arguments (where need be) or fields you want retrieved (else all the associated query fields are returned).

These modules are:
- Auth - For authentication setup and modification. Contains a single function for setting up public and secret keys.
- Accounts - For creating cryptocurrency addresses and virtual bank accounts
- Balances - For retrieving your balances in all the cryptocurrencies supported as well as for a single cryptocurrency of your choice
- Orders - For placing orders on the marketplace, viewing the market book as well as your personal orders on the platform
- Prices - For retrieving cryptocurrency prices on the platform
- Transfers - For checking transfer fees, sending, buying and selling cryptocurrencies via the API. 

### Testing

All tests for the modules are in the tests folder. In order to run the tests, run the command below in a shell within the project folder.

```bash
    python -m unittest discover tests  
```

### Handling exceptions

Invalid parameter types or absent parameters without a default raise an Exception. All excepts are of the generic Exception class. 

### Per-request Configuration

Configure individual requests with keyword arguments. 

```python
import buycoins_python as buycoins

# buy cryptocurrency
response = buycoins.Orders.buy(args={"price":"QnV5Y29pbnNQcmljZS0zOGIwYTg1Yi1jNjA1LTRhZjAtOWQ1My01ODk1MGVkMjUyYmQ=", "coin_amount":0.02, "cryptocurrency":"bitcoin"})

```

### Logging

The library can be configured to emit logging that will give you better insight
into what it's doing. The `info` logging level is usually most appropriate for
production use, but `debug` is also available for more verbosity.

There are a few options for enabling it:
Set `Logging`:
```python
    import buycoins_python as buycoins
    buycoins.log = 'debug'
    
```

### Todo

- Write tests for orders posting
- Submit package to Pypi registry
