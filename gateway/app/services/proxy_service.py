import logging

import httpx
from fastapi import HTTPException, Request, Response

logger = logging.getLogger(__name__)

TIMEOUT = httpx.Timeout(60.0)


async def forward_request(
    request: Request,
    target_base_url: str,
    path: str,
) -> Response:
    target_url = f"{target_base_url.rstrip('/')}/{path.lstrip('/')}"

    body = await request.body()

    headers = {}

    if content_type := request.headers.get("content-type"):
        headers["content-type"] = content_type

    if authorization := request.headers.get("authorization"):
        headers["authorization"] = authorization

    if accept := request.headers.get("accept"):
        headers["accept"] = accept

    logger.info("=" * 50)
    logger.info("Incoming path: %s", request.url.path)
    logger.info("Captured path: %s", path)
    logger.info("Target URL: %s", target_url)
    logger.info("Method: %s", request.method)
    logger.info("=" * 50)

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                params=request.query_params,
                content=body,
            )

        logger.info("Downstream status: %s", response.status_code)
        logger.info("Downstream body: %s", response.text)

        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type"),
        )

    except httpx.HTTPError as exc:
        logger.exception("HTTPX exception while proxying")

        raise HTTPException(
            status_code=502,
            detail=f"Gateway could not reach downstream service: {type(exc).__name__}",
        )

    except Exception:
        logger.exception("Unexpected gateway error")

        raise HTTPException(
            status_code=500,
            detail="Internal gateway error",
        )