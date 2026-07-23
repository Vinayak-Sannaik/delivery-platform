import logging
from fastapi import HTTPException, Request, Response
import httpx

# 1. Instantiate the logger ONCE at the module level
logger = logging.getLogger(__name__)

# Timeout configuration
TIMEOUT = httpx.Timeout(60.0)


async def forward_request(
    request: Request,
    target_base_url: str,
    path: str,
    client: httpx.AsyncClient | None = None,
) -> Response:
    target_url = f"{target_base_url.rstrip('/')}/{path.lstrip('/')}"

    # Build safe proxy headers (exclude host header to let HTTPX calculate it)
    headers = {
        k: v for k, v in request.headers.items() 
        if k.lower() not in ("host", "content-length")
    }

    # Use structured logging instead of print()
    logger.info(
        "Proxying request | path=%s | target_url=%s | method=%s",
        request.url.path,
        target_url,
        request.method,
    )

    try:
        # Use provided client or a temporary client block
        async_client = client or httpx.AsyncClient(timeout=TIMEOUT)
        
        # If client was passed in, don't use 'async with' (avoid closing shared client)
        if client:
            response = await async_client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                params=request.query_params,
                content=await request.body(),
            )
        else:
            async with async_client:
                response = await async_client.request(
                    method=request.method,
                    url=target_url,
                    headers=headers,
                    params=request.query_params,
                    content=await request.body(),
                )
                
        print("=" * 50)
        print("Incoming path:", request.url.path)
        print("Captured path:", path)
        print("Target URL:", target_url)
        print("Method:", request.method)
        print("=" * 50)
        
        print("DOWNSTREAM STATUS:", response.status_code)
        print("DOWNSTREAM BODY:", response.text)

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers={
                k: v for k, v in response.headers.items() 
                if k.lower() not in ("content-length", "transfer-encoding")
            },
            media_type=response.headers.get("content-type"),
        )

    except httpx.RequestError as exc:
        print("HTTPX ERROR:", repr(exc))
        logger.exception("Gateway proxy network error target_url=%s", target_url)
        raise HTTPException(
            status_code=502,
            detail=f"Bad Gateway: Unable to reach downstream service ({type(exc).__name__})",
        )
    except Exception:
        logger.exception("Unexpected error in gateway proxy")
        raise HTTPException(
            status_code=500,
            detail="Internal Gateway Error",
        )