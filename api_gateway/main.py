# api_gateway/main.py
import httpx
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import StreamingResponse
from api_gateway.config import settings
from api_gateway.middlewares.auth import JWTAuthMiddleware

app = FastAPI(title="API Gateway")

# Add authentication middleware
app.add_middleware(JWTAuthMiddleware)

# Initialize a global async client to reuse connections
http_client = httpx.AsyncClient()

@app.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()

SERVICE_MAP = {
    "auth": settings.auth_service_url,
    "rooms": settings.rooms_service_url,
    "guests": settings.guests_service_url,
    "reservations": settings.reservations_service_url,
    "payments": settings.payments_service_url,
    "availability": settings.availability_service_url,
    "billing": settings.billing_service_url,
}

@app.get("/")
def read_root():
    return {"message": "Welcome to API Gateway"}

@app.api_route("/api/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def gateway(request: Request, service: str, path: str):
    """
    Reverse proxy to downstream services.
    Route pattern: /api/<service_name>/<path>
    """
    if service not in SERVICE_MAP:
        raise HTTPException(status_code=404, detail="Service not found")

    service_url = SERVICE_MAP[service]

    # Construct target URL. If path is empty, we must keep the trailing slash
    # to match the downstream FastAPI prefix router (e.g. /rooms/)
    if not path:
         target_url = f"{service_url}/{service}/"
    else:
         target_url = f"{service_url}/{service}/{path}"

    # Prepare headers, excluding Host as httpx handles it
    headers = dict(request.headers)
    headers.pop("host", None)

    try:
        # Forward the request to the target service using the global client
        req = http_client.build_request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=await request.body(),
            params=request.query_params
        )
        response = await http_client.send(req)

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
