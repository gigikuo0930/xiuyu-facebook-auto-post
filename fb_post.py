import mimetypes
from pathlib import Path

import requests
from config import FB_PAGE_ID, FB_PAGE_TOKEN

def post_to_facebook(message: str, photo_path: Path) -> dict:
    url = f"https://graph.facebook.com/v25.0/{FB_PAGE_ID}/photos"

    data = {
        "caption": message,
        "access_token": FB_PAGE_TOKEN
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
