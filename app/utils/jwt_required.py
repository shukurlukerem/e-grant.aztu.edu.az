from functools import wraps
from fastapi import Request
from app.exceptions.exception import handle_unauthorized
from app.utils.jwt_util import decode_auth_token

def token_required(allowed_roles=None):
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            # Extract Request instance from kwargs or args
            request: Request = kwargs.get('request')
            if request is None:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if request is None:
                return handle_unauthorized(401, 'Request object is missing.')

            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return handle_unauthorized(401, 'Authorization token is missing.')

            try:
                token = auth_header.split(" ")[1]
                payload = decode_auth_token(token)

                if payload is None:
                    return handle_unauthorized(403, 'Token is invalid or expired.')

                if allowed_roles and payload.get('role') not in allowed_roles:
                    return handle_unauthorized(403, 'Access denied: role not allowed.')

                # Save user info on request.state (FastAPI way)
                request.state.user = payload

            except Exception as e:
                return handle_unauthorized(403, f'Invalid token format: {str(e)}')

            return await f(*args, **kwargs)
        return decorated_function
    return decorator
