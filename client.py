import requests


def jsonrpc_post(params: dict, id_=None):
    url = 'http://localhost:8080/jsonrpc'

    payload = {
        'jsonrpc': '2.0'
    }

    if id_ is not None:
        payload['id'] = id_

    payload.update(params)

    response = requests.post(url, json=payload, )
    response.raise_for_status()

    return response


def create_account(name: str, overdraft: bool, amount=0, id_=None):
    params = {
        'method': 'create_account',
        'params': [name, overdraft, amount]
    }

    return jsonrpc_post(params, id_)


def transfer_money(donor_id: int, recipient_id: int, amount: int, id_=None):
    params = {
        'method': 'transfer_money',
        'params': [donor_id, recipient_id, amount]
    }

    return jsonrpc_post(params, id_)


def get_balance(account_id: int, id_=None):
    params = {
        'method': 'get_balance',
        'params': [account_id]
    }

    return jsonrpc_post(params, id_)
