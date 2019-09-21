from flask import jsonify


class BusinessException(Exception):
    status_code = 200

    def __init__(self, message, code, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.code = code

    def to_dict(self):
        return response_error(self.code, self.message)


def response_success(data):
    return response_common(0, 'ok', data)


def response_error(code, msg):
    return response_common(code, msg, None)


def response_common(code, msg, data):
    res = {}
    res['code'] = code
    res['msg'] = msg
    res['data'] = data
    return res
