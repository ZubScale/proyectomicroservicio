# gateway/main.py  —  Puerto 8000
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import uuid
import time

app = FastAPI(title="API Gateway", version="1.0.0")

SERVICES = {
    "usuarios":  "http://localhost:8001",
    "productos": "http://localhost:8002",
    "pedidos":   "http://localhost:8003",
}


@app.api_route(
    "/{service}/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def gateway(service: str, path: str, request: Request):
    if service not in SERVICES:
        raise HTTPException(404, f"Servicio '{service}' no existe")

    correlation_id = str(uuid.uuid4())
    start = time.time()

    target_url = f"{SERVICES[service]}/{path}"
    if request.query_params:
        target_url += f"?{request.query_params}"

    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        resp = await client.request(
            method=request.method,
            url=target_url,
            headers={"X-Correlation-ID": correlation_id},
            content=await request.body(),
        )

    elapsed = round((time.time() - start) * 1000, 2)
    response = JSONResponse(content=resp.json(), status_code=resp.status_code)
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-Response-Time-Ms"] = str(elapsed)
    return response
