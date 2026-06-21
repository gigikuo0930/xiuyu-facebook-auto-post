@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo 找不到專案的 Python 環境 .venv
    echo 請先在 VS Code 終端機完成環境安裝。
    echo.
    pause
    exit /b 1
)

echo 正在啟動岫玉雅集館發文程式...
echo.
".venv\Scripts\python.exe" main.py

echo.
echo 程式已結束。
pause
