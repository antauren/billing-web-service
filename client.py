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


if __name__ == "__main__":
    main()
