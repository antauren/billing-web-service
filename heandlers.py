def heandle_request(request) -> dict:
    if not is_jsonrpc_version_true(request):
        return {'jsonrpc': '2.0',
                'error': {'code': -32000, 'message': 'The server supports only "jsonrpc 2.0" version request.'},
                'id': request.get('id', None)
                }

    return {}


def is_jsonrpc_version_true(request):
    return request.get('jsonrpc', None) == '2.0'
