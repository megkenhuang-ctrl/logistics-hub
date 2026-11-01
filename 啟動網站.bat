@echo off
chcp 65001 >nul
echo ========================================================
echo   廠區物流時刻表資料庫戰情網 (Fab Logistics Hub)
echo ========================================================
echo.
echo [1/2] 正在檢查與初始化資料庫 (logistics.db)...
python init_db.py
echo.
echo [2/2] 啟動本機伺服器 http://localhost:5000 ...
start http://localhost:5000
python server.py
pause
