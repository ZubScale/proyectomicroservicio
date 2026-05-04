# api_gateway/middlewares/auth.py
import jwt
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from api_gateway.config import settings

# Paths that don't require authentication
EXEMPT_PATHS = ["/api/auth/login", "/api/auth/register", "/docs", "/openapi.json"]

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Check if path is exempt from auth
        if any(path.startswith(exempt) for exempt in EXEMPT_PATHS) or path == "/":
            return await call_next(request)

        # Look for Bearer token in headers
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid Authorization header"}
            )

        token = auth_header.split(" ")[1]

        try:
            # Decode JWT
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
            # Add user info to request state so downstream logic can access it if needed
            request.state.user = payload
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token has expired"}
            )
        except jwt.PyJWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )

        # Proceed with request
        response = await call_next(request)
        return response
