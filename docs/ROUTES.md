# 路由設計文件 (ROUTES)

根據 PRD 與系統架構文件，本專案將 Flask 路由分為兩個主要模組：`home` 與 `record`。本文件詳列各個 URL 路徑、HTTP 請求方式及負責邏輯。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (顯示記帳列表狀態與餘額) | GET | `/` | `index.html` | 取得資料庫中所有紀錄與餘額，渲染主頁面。 |
| 新增收支頁面 (視 UI 設計) | GET | `/record/create` | `create.html` | 提供能讓使用者填寫金額、類別、日期與備註的 HTML 表單。 |
| 建立收支記錄 | POST | `/record/create` | — (重導向至 `/`) | 接收表單送出的資料 (`type`, `amount`, `date`, `note`)，驗證完後呼叫 Model 寫入資料庫並返回首頁。 |
| 刪除收支記錄 | POST | `/record/<id>/delete` | — (重導向至 `/`) | 依據路徑參數 `record_id`，呼叫 Model 將該筆紀錄刪除。 |

## 2. 每個路由的詳細說明

### `home` 模組
- **GET `/` (首頁)**
  - **輸入**：無
  - **處理邏輯**：呼叫 `RecordModel.get_all_records()` 取得明細清單，並呼叫 `RecordModel.get_balance_summary()` 取得統計資訊。
  - **輸出**：將 `records` 與 `summary` 變數作為 context 傳入 `index.html` 進行渲染。
  - **錯誤處理**：若資料庫連線或讀取異常，可返回 HTTP 500 與簡單的錯誤提示。

### `record` 模組
- **GET `/record/create`**
  - **輸入**：無
  - **處理邏輯**：單純提供輸入介面。
  - **輸出**：渲染 `create.html` 頁面顯示新增表單。
- **POST `/record/create`**
  - **輸入**：透過 `request.form` 取得前端送出的欄位。
  - **處理邏輯**：
    1. 驗證必填項。
    2. 金額必須大於 0 的數值，型別必須是 `income` 或 `expense`。
    3. 成功後對 `RecordModel.create_record(...)` 發出叫用。
  - **輸出**：若成功，HTTP 302 重新導向至首頁 (`url_for('home.index')`)。
  - **錯誤處理**：如果資料格式有誤或缺漏，可使用 Flask 的 `flash()` 將錯誤訊息帶回表單畫面 (`create.html`)。
- **POST `/record/<int:record_id>/delete`**
  - **輸入**：URL 所帶的整數變數 `record_id`。
  - **處理邏輯**：呼叫 `RecordModel.delete_record(record_id)` 從資料庫移除指定記錄。
  - **輸出**：完成後重新導向至首頁。
  - **錯誤處理**：如果紀錄不在資料庫中，則由資料庫本身忽略或藉由 Model 返回空，安全性避免跳錯，也可回傳 404。

## 3. Jinja2 模板清單

所有的視圖頁面將建置於 `app/templates/` 中，規劃如下：
- **`base.html`**：最上層的通用佈局，包含網頁標頭（`<head>`）、共用的 CSS 與 JS，以及所有頁面皆會顯示的頂部導覽列（Navbar）。
- **`index.html`**：繼承 `base.html`。首部區塊用來顯示餘額狀態與收入支出金額，下半區塊會 `for` 迴圈迭代出所有收支清單。
- **`create.html`**：繼承 `base.html`。獨立的新增記錄表單頁面。

## 4. 路由骨架程式碼
參考專案中的 `app/routes/home.py` 與 `app/routes/record.py`，已備妥了符合 Flask Blueprint 規範的函數定義與註解骨架。
