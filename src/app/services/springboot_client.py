from typing import Any

import httpx

APP_ID = "agent"
APP_SECRET = "agent"


async def fetch_data(host: str, userid: str, sql: str, dataset: str) -> dict[str, Any]:
    """
    Fetch data from Spring Boot with a two-step token flow.
    """
    base_url = host.rstrip("/")
    token_url = (
        f"{base_url}/rest/oauth2/token"
        f"?grant_type=client_credentials&client_id={APP_ID}&client_secret={APP_SECRET}"
    )

    async with httpx.AsyncClient(timeout=30) as client:
        token_resp = await client.get(token_url)
        token_resp.raise_for_status()
        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise ValueError("Missing access_token in token response")

        query_url = f"{base_url}/api/oauthaccess/datav/agent/queryData"
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {"userid": userid, "sql": sql, "dataset": dataset}
        query_resp = await client.post(query_url, headers=headers, json=payload)
        query_resp.raise_for_status()
        return query_resp.json()
