# 每次 Code 更動強制審查程序 (Mandatory Code / Security / UI & UX Review SOP)

針對本專案（`g:\我的雲端硬碟\AI\Logistics`）之任何程式碼、資料庫、排程演算法或前端網頁更動，Agent 必須於每次修改後強制執行以下三維度審查與自動化驗證程序：

## 1. Code Review（程式碼品質、命名規範與資料同步審查 — `CHK-R01`）
- **廠區標準命名規範**：所有晶圓八廠所屬廠區描述一律採用 **`晶圓 8AB 廠`**、**`晶圓 8CD 廠`**、**`晶圓 8E 廠`**、**`晶圓 8F 廠`**、**`晶圓 8S 廠`**，嚴禁出現舊版 `晶圓八廠 AB/CD/E/F/S 區` 字樣。
- **排程與法規一致性**：修改 `optimizer_plan2.py`、`optimizer_plan3.py` 或 `validator.py` 後，必須同步重新執行：
  1. `python optimizer_plan2.py`
  2. `python optimizer_plan3.py`
  3. `python validator.py`
  4. `python scratch/sync_export_json.py`
- **跨檔零誤差同步**：確保 `logistics.db`、`db_export.json`、`db_data.js`、`plans.html`（`CAR_COMPARE_DATA`）與 `audit_report*.html` 數據 100% 同步。

## 2. 安全性審查（Security Review — `CHK-R02`）
- **SQL Injection 防護**：`server.py` 與所有資料庫腳本必須 100% 使用 `?` 參數化查詢（Parameterized Queries），且動態資料表名稱必須通過 `ALLOWED_TABLES` 白名單驗證。
- **路徑遍歷與寫入防護**：API 端點與靜態檔案服務嚴格限制於專案根目錄與授權資料表內，防止 Path Traversal 與未授權寫入。
- **敏感資訊與 XSS 防護**：嚴禁於前端或後端硬編碼外部私鑰/API Key，且確保動態渲染欄位無惡意腳本注入風險。

## 3. UI & UX 審查（介面視覺、響應式與防呆體驗審查 — `CHK-R03`）
- **語意化清晰標示**：站點副標題清楚呈現 `晶圓 8AB/8CD/8E/8F/8S 廠碼頭/主樞紐`，休息與交接站點明確標示 `專屬停車區／司機休息室旁（不佔據碼頭裝卸作業泊位）`，且外包廠區（嘉晶創新、嘉晶篤行）維持 0 休息。
- **雙模無縫載入與即時切換**：確保 `index.html`、`plans.html`、`spec.html`、`audit_report*.html` 在離線快取 (`db_data.js`) 與本地伺服器 (`http://localhost:5000`) 下皆能零延遲切換「原方案 / 方案二 / 方案三」與「日班 / 夜班 / 24H」。
