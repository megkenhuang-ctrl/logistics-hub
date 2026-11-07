@echo off
chcp 65001 >nul
title 晶圓廠物流時刻與運能結算系統 (Port 5000)

echo ========================================================
echo   晶圓廠跨廠區物流時刻表與運能結算系統
echo ========================================================
echo.

cd /d "%~dp0"

:: 優先檢測本機安裝的 Python 執行檔路徑，避免 WindowsApps 虛擬捷徑干擾
set "PY_CMD="
if exist "%LOCALAPPDATA%\Python\bin\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Python\bin\python.exe"
) else (
    where py >nul 2>&1 && (
        set "PY_CMD=py"
    ) || (
        set "PY_CMD=python"
    )
)

if not exist logistics.db (
    echo [資訊] 首次執行，正在建立 SQLite 資料庫 (logistics.db)...
    "%PY_CMD%" init_db.py
)

echo [啟動] 正在啟動 Web 服務 (http://localhost:5000)...
echo [提示] 廠區內部同仁請訪問: http://[本機IP]:5000
echo.
start http://localhost:5000
"%PY_CMD%" server.py

pause
