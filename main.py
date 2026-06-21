from pathlib import Path

from gemini_post import generate_article
from fb_post import post_to_facebook

PHOTO_DIR = Path(__file__).resolve().parent / "岫玉照片"
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
SHOPEE_URL = "https://shopee.tw/gigikuo930"


def select_photo() -> Path | None:
    photos = sorted(
        path for path in PHOTO_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in PHOTO_EXTENSIONS
    ) if PHOTO_DIR.exists() else []

    if not photos:
        print(f"找不到照片，請把圖片放入：{PHOTO_DIR}")
        return None

    print("=== 請選擇本次發文照片 ===")
    for index, photo in enumerate(photos, start=1):
        print(f"{index:>2}. {photo.name}")

    while True:
        choice = input("輸入照片編號（直接按 Enter 取消）：").strip()
        if not choice:
            return None

        try:
            selected_index = int(choice)
            if 1 <= selected_index <= len(photos):
                return photos[selected_index - 1]
        except ValueError:
            pass

        if choice:
            print(f"請輸入 1 到 {len(photos)} 之間的編號。")


def main():
    photo_path = select_photo()
    if photo_path is None:
        print("已取消發布。")
        return

    article = generate_article().rstrip()
    article = f"{article}\n\n🛒 蝦皮賣場：{SHOPEE_URL}"

    print("=== 本次產生貼文 ===")
    print(f"照片：{photo_path.name}")
    print(article)
    print("===================")

    confirm = input("是否發布到 Facebook？輸入 Y 才發布：").strip().upper()

    if confirm != "Y":
        print("已取消發布。")
        return

    result = post_to_facebook(article, photo_path)

    print("=== Facebook 回傳結果 ===")
    print(result)

if __name__ == "__main__":
    main()
