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


if __name__ == "__main__":
    main()
