import random
from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

TOPICS = [
    "岫玉天青凍介紹",
    "岫玉紅冰介紹",
    "岫玉白冰介紹",
    "岫玉日常保養方式",
    "天然玉石配戴寓意",
    "岫玉吊墜如何挑選",
    "岫玉戒指日常搭配",
    "天然玉石每件紋理不同的特色",
]

def generate_article() -> str:
    topic = random.choice(TOPICS)

    prompt = f"""
你是「岫玉雅集館」粉專小編，請撰寫一篇 Facebook 貼文。

主題：{topic}

要求：
1. 80~150字
2. 繁體中文
3. 口吻溫暖、自然、不要太誇大
4. 不要宣稱療效、開運、保證功效
5. 結尾加入柔性的購買引導
6. 附上3~5個Hashtag
7. 直接輸出貼文內容，不要加標題說明
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text.strip()
