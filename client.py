import requests
import json


def main():
    url = 'http://localhost:8080/jsonrpc'

    # jsonrpc version error
    payload = {'jsonrpc': '1.0'}
    response = requests.post(url, json=payload).json()
    assert response['error']['code'] == -32000

    # json parse error
    payload = json.dumps({'jsonrpc': '2.0'}) + '}'
    response = requests.post(url, data=payload).json()
    assert response['error']['code'] == -32700

    # Invalid Request
    payload = json.dumps({'jsonrpc': '2.0', 'method': None})
    response = requests.post(url, data=payload).json()
    assert response['error']['code'] == -32600

    # Invalid Request
    payload = json.dumps({'jsonrpc': '2.0', 'method': 'foo', 'params': -1})
    response = requests.post(url, data=payload).json()
    assert response['error']['code'] == -32600

    # Method not found
    payload = json.dumps({'jsonrpc': '2.0', 'method': 'abcdefghijklmnopqrstuvwxyz'})
    response = requests.post(url, data=payload).json()
    assert response['error']['code'] == -32601

    # Invalid params (params count)
    payload = json.dumps({'jsonrpc': '2.0', 'method': 'create_account', 'params': ['name_1', False, 0] * 100})
    response = requests.post(url, data=payload).json()
    assert response['error']['code'] == -32602

    # transfer_money
    donor_id = requests.post(url, json={'jsonrpc': '2.0', 'method': 'create_account', 'params': ['name_1', True]}
                             ).json()['result']
    recipient_id = requests.post(url, json={'jsonrpc': '2.0', 'method': 'create_account', 'params': ['name_2', True]}
                                 ).json()['result']
    requests.post(url, json={'jsonrpc': '2.0', 'method': 'transfer_money', 'params': [donor_id, recipient_id, 300]}
                  )
    donor_amount = requests.post(url, json={'jsonrpc': '2.0', 'method': 'get_balance', 'params': [donor_id]}
                                 ).json()['result']
    recipient_amount = requests.post(url, json={'jsonrpc': '2.0', 'method': 'get_balance', 'params': [recipient_id]}
                                     ).json()['result']
    assert donor_amount == -300.0
    assert recipient_amount == 300.0


if __name__ == "__main__":
    main()
