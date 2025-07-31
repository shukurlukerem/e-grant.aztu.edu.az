# # middleware/log_middleware.py
# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request
# from starlette.responses import Response
# from utils.logger_config import logger
# import json
# from io import BytesIO

# class LoggingMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         ip = request.client.host
#         body = await request.body()
#         user_info = ""

#         # Extract user info from request.state (if set after auth)
#         if hasattr(request.state, "user"):
#             user = request.state.user
#             fin = user.get("fin")
#             gmail = user.get("gmail")
#             user_info = f"FIN: {fin} | Gmail: {gmail}"

#         response: Response = await call_next(request)

#         response_body = b""
#         async for chunk in response.body_iterator:
#             response_body += chunk
#         response.body_iterator = iterate_in_chunks(response_body)

#         logger.info(f"IP: {ip} | {user_info} | Response: {response_body.decode('utf-8')[:1000]}")

#         return response

# def iterate_in_chunks(body: bytes, chunk_size=4096):
#     yield from (body[i:i + chunk_size] for i in range(0, len(body), chunk_size))
