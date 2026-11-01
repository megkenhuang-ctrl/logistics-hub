# 晶圓廠物流時刻與運能結算系統 — 系統佈署指南 (Deployment Guide)

本系統採用 **極簡零依賴架構（Zero External Dependency）**：
- **後端**：標準 Python 3.8+ 內建模組 (`http.server`, `sqlite3`, `socket`, `json`)，無需安裝任何龐大 pip 套件。
- **資料庫**：SQLite (`logistics.db`) 單一檔案，免裝 MySQL/PostgreSQL 伺服器。
- **前端**：響應式 SPA 單頁應用 (`index.html`)，靜態載入 Tailwind CSS、FontAwesome、KaTeX。

---

## 方案一：廠區 / 辦公室內部 Windows 伺服器（最推薦、最簡單）

適合部署在廠區專屬電腦或辦公室實體主機，供內部同仁瀏覽。

### 步驟 1：開放 Windows 防火牆 Port 5000
以系統管理員身分開啟 PowerShell，執行：
```powershell
New-NetFirewallRule -DisplayName "Logistics Web System (5000)" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

### 步驟 2：設定開機自動啟動（常駐服務）
**方法 A：Windows 工作排程器（Task Scheduler，內建免安裝）**
1. 按 `Win + R` 輸入 `taskschd.msc` 開啟工作排程器。
2. 點擊「建立基本工作」➔ 名稱輸入 `LogisticsWebServer`。
3. 觸發程序選擇「當電腦啟動時」。
4. 動作選擇「啟動程式」：
   - 程式或指令碼：`python.exe`
   - 新增引數：`server.py`
   - 開始於：`G:\我的雲端硬碟\AI\Logistics`（請替換為實際存放路徑）
5. 完成後勾選「以最高權限執行」，即可達成開機背景常駐。

**方法 B：使用 NSSM 封裝為 Windows 服務（推薦，具當機重啟能力）**
```cmd
nssm install LogisticsService python "C:\path\to\server.py"
nssm set LogisticsService AppDirectory "C:\path\to\Logistics"
nssm start LogisticsService
```

### 步驟 3：提供同仁訪問網址
查詢主機 IP（例如 `10.120.45.67`），告知廠內同仁即可使用：
```text
http://10.120.45.67:5000/
```

---

## 方案二：Docker 容器化佈署（跨平台標準化）

若伺服器支援 Docker，此方案最標準且完全隔離環境。

### 1. 快速一鍵啟動
專案目錄已內建 `Dockerfile` 與 `docker-compose.yml`，只需在專案目錄下執行：
```bash
docker compose up -d --build
```

### 2. 檢視運行狀態
```bash
docker ps
docker logs -f fab-logistics-web
```

### 3. 停止與重啟
```bash
docker compose down
docker compose restart
```

---

## 方案三：Linux 伺服器 / 雲端 VM（Ubuntu / Debian / CentOS）

若佈署在廠內 Linux VM 或 GCP / AWS 虛擬主機：

### 步驟 1：建立 systemd 服務
建立服務設定檔 `/etc/systemd/system/logistics.service`：
```ini
[Unit]
Description=Logistics Schedule Web Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/logistics
ExecStart=/usr/bin/python3 /opt/logistics/server.py
Restart=always
RestartSec=5
Environment=PORT=5000

[Install]
WantedBy=multi-user.target
```

### 步驟 2：啟用並啟動服務
```bash
sudo systemctl daemon-reload
sudo systemctl enable logistics
sudo systemctl start logistics
sudo systemctl status logistics
```

### 步驟 3：設定 Nginx 反向代理（可選，提供標準 80 或 HTTPS 443）
在 `/etc/nginx/sites-available/default` 加入：
```nginx
server {
    listen 80;
    server_name logistics.yourdomain.internal;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
重啟 Nginx：`sudo systemctl restart nginx`。

---

## 方案四：雲端 Serverless / 容器平台（GCP Cloud Run / Render / Fly.io）

- **GCP Cloud Run**：
  直接連動 Git 儲存庫或以 gcloud CLI 推送映像檔：
  ```bash
  gcloud run deploy logistics-system --source . --port 5000 --allow-unauthenticated
  ```
- **Render / Fly.io**：
  選擇 Web Service ➔ 指定 Dockerfile 即可自動建置與對外發布。

---

## 備份與維護說明

1. **資料備份**：
   - 僅需備份 `logistics.db` 單一檔案即可完整保存所有班表、OD 矩陣與司機出勤歷史。
2. **時刻表批次重設 / 匯入**：
   - 修改 `init_db.py` 中的班表邏輯後，在網頁第四頁點擊「重新載入」或執行 `python init_db.py` 即可在 1 秒內更新全庫。
