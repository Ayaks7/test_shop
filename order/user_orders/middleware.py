import json
from django.http import HttpResponseForbidden
from typing import Optional
import jwt
from jwt import PyJWTError

from user_orders.utils import SECRET_KEY, ALGORITHM


class UserAuthMiddleware(object):
    """Аутенфикация по временному токену."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token is not None:
            token = token.replace('Bearer ', '')
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id: Optional[str] = payload.get("sub")
                if user_id is None:
                    return HttpResponseForbidden()
            except PyJWTError:
                return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()
        return self.get_response(request)
