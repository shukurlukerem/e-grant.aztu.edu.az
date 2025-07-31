from functools import wraps
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.utils.jwt_util import decode_auth_token
from app.exceptions.exception import (handle_forbidden, 
                                      handle_unauthorized,
                                      handle_role_forbidden)

def role_required(required_roles):
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            # We expect 'Request' to be passed as a keyword argument
            request: Request = kwargs.get('request')
            if request is None:
                # Try to find Request in positional args (usually first)
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if request is None:
                # Could not find Request instance
                return handle_unauthorized(403, "Request object is missing.")

            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return handle_unauthorized(403, 'Authorization token is missing.')

            try:
                token = auth_header.split(" ")[1]
                payload = decode_auth_token(token)

                if payload is None:
                    return handle_unauthorized(403, 'Token is invalid or expired.')

                print(f"Decoded payload: {payload}")

                try:
                    user_role_code = int(payload.get('role_code', -1))
                except ValueError:
                    return handle_unauthorized(403, 'Role code is not a valid integer.')

                print(f"User role code: {user_role_code}")
                print(f"Required roles: {required_roles}")

                if user_role_code not in required_roles:
                    print("Role check failed")
                    return handle_role_forbidden(403, "User does not have the required role to access this endpoint.")

                # Save user info in request.state for downstream use
                request.state.user = payload

            except Exception as e:
                return handle_unauthorized(401, f'Invalid token format: {str(e)}')

            return await f(*args, **kwargs)
        return decorated_function
    return decorator
