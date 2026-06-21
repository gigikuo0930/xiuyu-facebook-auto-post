# 岫玉雅集館粉專自動發文

## 1. 安裝套件

```bat
cd /d D:\岫玉雅集館粉專
pip install -r requirements.txt
```

## 2. 建立 .env

把 `.env.example` 複製成 `.env`，填入：

```env
FB_PAGE_ID=495676636973018
FB_PAGE_TOKEN=你的PageToken
GEMINI_API_KEY=你的Gemini_API_Key
```

## 3. 執行

```bat
python main.py
```

程式會先產生貼文，確認輸入 `Y` 才會發布到 Facebook。

## 4. 注意

- Page Token 不會因為電腦重開機失效。
- 但 Token 可能會因為到期、改密碼、移除 App 權限而失效。
- 第一次建議先手動確認內容，不要直接全自動發布。
