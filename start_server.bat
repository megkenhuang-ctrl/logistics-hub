@echo off
chcp 65001 >nul
title 晶圓廠物流時刻與運能結算系統 (Port 5000)

echo ========================================================
echo   晶圓廠跨廠區物流時刻表與運能結算系統
echo ========================================================
echo.

cd /d "%~dp0"

if not exist logistics.db (
    echo [資訊] 首次執行，正在建立 SQLite 資料庫 (logistics.db)...
    python init_db.py
)

echo [啟動] 正在啟動 Web 服務 (http://localhost:5000)...
echo [提示] 廠區內部同仁請訪問: http://[本機IP]:5000
echo.
python server.py

pause
