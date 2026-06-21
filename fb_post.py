import mimetypes
from pathlib import Path

import requests
from config import FB_PAGE_ID, FB_PAGE_TOKEN


def get_page_access_token() -> str:
    me_response = requests.get(
        "https://graph.facebook.com/v25.0/me",
        params={"fields": "id", "access_token": FB_PAGE_TOKEN},
        timeout=30,
    )
    me_result = me_response.json()

    if me_result.get("id") == FB_PAGE_ID:
        return FB_PAGE_TOKEN

    pages_response = requests.get(
        "https://graph.facebook.com/v25.0/me/accounts",
        params={
            "fields": "id,access_token",
            "limit": 100,
            "access_token": FB_PAGE_TOKEN,
        },
        timeout=30,
    )
    pages_result = pages_response.json()

    if "error" in pages_result:
        raise RuntimeError(f"無法取得粉專 Token：{pages_result['error']}")

    for page in pages_result.get("data", []):
        if page.get("id") == FB_PAGE_ID and page.get("access_token"):
            return page["access_token"]

    raise RuntimeError("目前 Token 無法管理指定的 Facebook 粉專")


def post_to_facebook(message: str, photo_path: Path) -> dict:
    url = f"https://graph.facebook.com/v25.0/{FB_PAGE_ID}/photos"

    data = {
        "caption": message,
        "access_token": get_page_access_token()
    }

    content_type = mimetypes.guess_type(photo_path.name)[0] or "image/jpeg"

    with photo_path.open("rb") as photo:
        files = {
            "source": (photo_path.name, photo, content_type)
        }
        response = requests.post(url, data=data, files=files, timeout=60)

    try:
        return response.json()
    except Exception:
        return {
            "status_code": response.status_code,
            "text": response.text
        }
