import mimetypes
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from config import FB_PAGE_ID, FB_PAGE_TOKEN

TAIPEI_TIMEZONE = timezone(timedelta(hours=8))


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


def has_posted_today(marker: str) -> bool:
    today_start = datetime.now(TAIPEI_TIMEZONE).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    response = requests.get(
        f"https://graph.facebook.com/v25.0/{FB_PAGE_ID}/published_posts",
        params={
            "fields": "id,message,created_time",
            "since": today_start.isoformat(),
            "limit": 100,
            "access_token": get_page_access_token(),
        },
        timeout=30,
    )
    result = response.json()

    if "error" in result:
        raise RuntimeError(f"無法檢查粉專今日貼文：{result['error']}")

    return any(
        marker in post.get("message", "")
        for post in result.get("data", [])
    )


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
        response = requests.post(url, data=data, files=files, timeout=300)

    try:
        return response.json()
    except Exception:
        return {
            "status_code": response.status_code,
            "text": response.text
        }
