import json

import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from fastapi import Request

from app.config import settings


async def authenticate(request: Request):
    """
    Decorator for authenticate user(set current user to request)
    """

    token_components = request.headers.get("Authorization", '').split(' ')
    token_type = token_components[0]
    access_token = token_components[-1]
    # access_token = request.headers.get("Authorization")

    # TODO ask
    if token_type != settings.TOKEN_TYPE:
        return False, {'token': 'Invalid token type'}

    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])  # type: ignore
        if payload['sub'] != settings.ACCESS_TOKEN_JWT_SUBJECT:
            return False, {'error': 'Access token is expected'}

        request.state.user_id = payload['id']
        return True, ''
    except Exception:
        request.state.user_id = None
        return False, {'error': 'Invalid token or token is expired'}


class ApiKeyMiddleware(BaseHTTPMiddleware):
    not_authorize_paths = [
        "/docs",
        "/openapi.json",
    ]

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.not_authorize_paths or request.method == 'OPTIONS':
            request.state.user_id = None
        else:
            is_valid, error_message = await authenticate(request=request)
            if not is_valid:
                return Response(content=json.dumps(error_message), status_code=401)
        return await call_next(request)
