from fastapi import HTTPException, Request, Response
import httpx


async def forward_request(
    request: Request,
    target_base_url: str,
    path: str,
) -> Response:
    target_url = f"{target_base_url.rstrip('/')}/{path.lstrip('/')}"

    headers = {
        "content-type": request.headers.get("content-type", "application/json"),
    }

    authorization = request.headers.get("authorization")
    if authorization:
        headers["authorization"] = authorization

    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                params=request.query_params,
                content=await request.body(),
            )

        # print("Downstream status:", response.status_code)
        # print("Downstream body:", response.text)
        
        print("=" * 50)
        print("Incoming path:", request.url.path)
        print("Captured path:", path)
        print("Target URL:", target_url)
        print("Method:", request.method)
        print("=" * 50)

        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type"),
        )

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )