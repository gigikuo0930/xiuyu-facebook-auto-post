from datetime import datetime, timedelta, timezone
from pathlib import Path

from fb_post import post_to_facebook
from gemini_post import generate_article

PHOTO_DIR = Path(__file__).resolve().parent / "岫玉照片"
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
SHOPEE_URL = "https://shopee.tw/gigikuo930"
TAIPEI_TIMEZONE = timezone(timedelta(hours=8))


def select_daily_photo() -> Path:
    photos = sorted(
        path
        for path in PHOTO_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in PHOTO_EXTENSIONS
    ) if PHOTO_DIR.exists() else []

    if not photos:
        raise FileNotFoundError(f"找不到照片，請把圖片放入：{PHOTO_DIR}")

    today = datetime.now(TAIPEI_TIMEZONE).date()
    return photos[today.toordinal() % len(photos)]


def main() -> None:
    photo_path = select_daily_photo()
    article = generate_article().rstrip()
    message = f"{article}\n\n🛒 蝦皮賣場：{SHOPEE_URL}"

    print(f"本次照片：{photo_path.name}")
    result = post_to_facebook(message, photo_path)

    if "error" in result:
        raise RuntimeError(f"Facebook 發布失敗：{result['error']}")

    if not result.get("id") and not result.get("post_id"):
        raise RuntimeError(f"Facebook 回傳非預期結果：{result}")

    print(f"Facebook 發布成功：{result.get('post_id') or result.get('id')}")


if __name__ == "__main__":
    main()
