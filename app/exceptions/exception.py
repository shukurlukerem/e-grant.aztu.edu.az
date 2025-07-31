from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

# Global 500 error
async def handle_global_exception(request: Request, e: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(e),
        },
    )

# 404 - Not Found
async def handle_not_found(request: Request, e: HTTPException):
    return JSONResponse(
        status_code=404,
        content={
            "status": 404,
            "message": "User not found",
            "error_code": "NOT_FOUND",
        },
    )

# Custom 404 - Not Found with message (not an exception handler)
def handle_specific_not_found(message: str):
    return JSONResponse(
        status_code=404,
        content={
            "status": 404,
            "message": message,
            "error_code": "NOT_FOUND",
        },
    )

# Custom 404 - Missing Field (not an exception handler)
def handle_missing_field():
    return JSONResponse(
        status_code=404,
        content={
            "status": 404,
            "message": "Missing field",
            "error_code": "MISSING_FIELD",
        },
    )

# 409 - Conflict
async def handle_conflict(request: Request, e: HTTPException):
    return JSONResponse(
        status_code=409,
        content={
            "status": 409,
            "message": "User exists",
            "error_code": "CONFLICT",
        },
    )

# 403 - Forbidden (Token missing)
async def handle_forbidden(request: Request, e: HTTPException):
    return JSONResponse(
        status_code=403,
        content={
            "status": 403,
            "message": "Token is missing.",
            "error_code": "FORBIDDEN",
        },
    )

# 403 - Forbidden (Role-based, not an exception handler)
def handle_role_forbidden(message: str):
    return JSONResponse(
        status_code=403,
        content={
            "status": 403,
            "message": message,
            "error_code": "FORBIDDEN",
        },
    )

# 401 - Unauthorized
def handle_unauthorized(status_code=401, message="Unauthorized"):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": "Unauthorized",
            "message": message,
        },
    )

# 200 - Sign-in Success
def handle_signin_success(data, message, token):
    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "message": message,
            "data": data,
            "token": token,
            "success_code": "SUCCESS",
        },
    )

# 200 - General Success
def handle_success(data, message):
    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "message": message,
            "data": data,
            "success_code": "SUCCESS",
        },
    )

# 201 - Creation
def handle_creation(message):
    return JSONResponse(
        status_code=201,
        content={
            "status": 201,
            "message": message,
            "success_code": "CREATED",
        },
    )
