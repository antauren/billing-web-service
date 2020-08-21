# Asynchronous Web Service

This billing web-service works by [*json-rpc 2.0*](https://www.jsonrpc.org/specification) protocol.

Web service use [*aiohttp*](docs.aiohttp.org) for asynchronous request processing 
and [*aiopg*](aiopg.readthedocs.io) engine for work with PostgreSQL database.


You can use three methods:
  * create_account
  * transfer_money
  * get_balance
  
(Batch requests are not supported yet.)


## Examples

### create_account

* create_account *user_1*
    * request: `{'method': 'create_account', 'params': ['user_1', True], 'jsonrpc': '2.0', 'id': 1}`
    * response:  `{'result': 1, 'id': 1, 'jsonrpc': '2.0'}`

* create_account *user_2*
    * request: `{'method': 'create_account', 'params': {'name': 'user_2', 'overdraft': True}, 'jsonrpc': '2.0'}`
    * response: `{'result': 2, 'id': None, 'jsonrpc': '2.0'}`

###  transfer_money  


* transfer_money money from *user_1* to *user_2*
    * request: `{'method': 'transfer_money', 'params': {'donor_id': 1, 'recipient_id': 2, 'amount': 5 }, 'jsonrpc': '2.0'}` 
    * response: `{'result': True, 'id': None, 'jsonrpc': '2.0'}`
    

* transfer_money money from *user_2* to *user_1*
    * request: `{'method': 'transfer_money', 'params': [2, 1, 300], 'jsonrpc': '2.0', 'id': 2}`
    * response: `{'result': True, 'id': 2, 'jsonrpc': '2.0'}`


###  get_balance 

* get_balance *user_1*
    * request: `{'method': 'get_balance', 'params': [1], 'jsonrpc': '2.0', 'id': 3}`
    * response: `{'result': 295.0, 'id': 3, 'jsonrpc': '2.0'}`

* get_balance *user_2*
    * request: `{'method': 'get_balance', 'params': {'account_id': 2}, 'jsonrpc': '2.0'}`
    * response: `{'result': -295.0, 'id': None, 'jsonrpc': '2.0'}`
    

## Requirements
 * Python >= 3.7
 * PostgreSQL



## Installation and launch
1. Clone the repository:

    ```bash
    git clone https://github.com/antauren/billing-web-service.git
    cd billing-web-service
    ```
    
2. Install requirements:
    ```
    pip install -r requirements.txt
    ```
    
3. Create environment file from example:
    ```bash
    cp .env.example .env
    ```
    
4. Personalize settings by modifying ```.env``` with your preferable text editor.
     
5. Run server:
    ```
    python server.py
    ```
    
6. Launch client:
    ```
    python client.py
    ```
