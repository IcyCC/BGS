from functools import wraps
from flask import make_response
def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        return rst
    return wrapper_fun