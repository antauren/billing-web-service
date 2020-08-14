PARSE_ERROR = {'jsonrpc': '2.0',
               'error': {'code': -32700, 'message': 'Parse error'},
               'id': None
               }


def handle_request(request: dict) -> dict:
    if not is_jsonrpc_version_true(request):
        return {'jsonrpc': '2.0',
                'error': {'code': -32000, 'message': 'The server supports only "jsonrpc 2.0" version request.'},
                'id': request.get('id', None)
                }

    if not (is_rpc_method_specified(request) and is_params_true(request)):
        return {'jsonrpc': '2.0',
                'error': {'code': -32600, 'message': 'Invalid Request.'},
                'id': request.get('id', None)
                }

    return {}


def is_jsonrpc_version_true(request: dict) -> bool:
    version = request.get('jsonrpc', '')

    return isinstance(version, str) and version.startswith('2.')


def is_rpc_method_specified(request: dict) -> bool:
    method = request.get('method', None)

    return isinstance(method, str)


def is_params_true(request: dict) -> bool:
    params = request.get('params', [])

    return isinstance(params, list) or isinstance(params, dict)
