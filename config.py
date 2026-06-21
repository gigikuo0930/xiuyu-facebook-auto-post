import os
from dotenv import load_dotenv

load_dotenv()

FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not FB_PAGE_ID:
    raise ValueError("缺少 FB_PAGE_ID，請在 .env 設定")
if not FB_PAGE_TOKEN:
    raise ValueError("缺少 FB_PAGE_TOKEN，請在 .env 設定")
if not GEMINI_API_KEY:
    raise ValueError("缺少 GEMINI_API_KEY，請在 .env 設定")
