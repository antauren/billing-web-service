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
    payload = {'method': None, 'jsonrpc': '2.0'}
    response = requests.post(url, json=payload).json()
    assert response['error']['code'] == -32600

    # Invalid Request
    payload = {'method': 'foo', 'params': -1, 'jsonrpc': '2.0'}
    response = requests.post(url, json=payload).json()
    assert response['error']['code'] == -32600

    # Method not found
    payload = {'method': 'abcdefghijklmnopqrstuvwxyz', 'jsonrpc': '2.0'}
    response = requests.post(url, json=payload).json()
    assert response['error']['code'] == -32601

    # Invalid params (params count)
    payload = {'method': 'create_account', 'params': ['name_1', False, 0] * 100, 'jsonrpc': '2.0'}
    response = requests.post(url, json=payload).json()
    assert response['error']['code'] == -32602

    # transfer_money
    donor_id = requests.post(url,
                             json={'method': 'create_account', 'params': ['name_1', True], 'jsonrpc': '2.0', }
                             ).json()['result']
    recipient_id = requests.post(url,
                                 json={'method': 'create_account', 'params': ['name_2', True], 'jsonrpc': '2.0'}
                                 ).json()['result']
    requests.post(url,
                  json={'method': 'transfer_money', 'params': [donor_id, recipient_id, 300], 'jsonrpc': '2.0'}
                  )
    donor_amount = requests.post(url,
                                 json={'method': 'get_balance', 'params': [donor_id], 'jsonrpc': '2.0'}
                                 ).json()['result']
    recipient_amount = requests.post(url,
                                     json={'method': 'get_balance', 'params': [recipient_id], 'jsonrpc': '2.0'}
                                     ).json()['result']
    assert donor_amount == -300.0
    assert recipient_amount == 300.0


if __name__ == '__main__':
    main()
