parse_error = {'jsonrpc': '2.0',
               'error': {'code': -32700, 'message': 'Parse error'},
               'id': None
               }


def handle_request(request) -> dict:
    if not is_jsonrpc_version_true(request):
        return {'jsonrpc': '2.0',
                'error': {'code': -32000, 'message': 'The server supports only "jsonrpc 2.0" version request.'},
                'id': request.get('id', None)
                }

    if not (is_method_true(request) and is_params_true(request)):
        return {'jsonrpc': '2.0',
                'error': {'code': -32600, 'message': 'Invalid Request.'},
                'id': request.get('id', None)
                }

    return {}


def is_jsonrpc_version_true(request):
    return request.get('jsonrpc', None) == '2.0'


def is_method_true(request: dict) -> bool:
    method = request.get('method', None)

    if method is None:
        return False

    if not isinstance(method, str):
        return False

    return True


def is_params_true(request: dict) -> bool:
    params = request.get('params', [])

    if not (isinstance(params, list) or isinstance(params, dict)):
        return False

    return True
