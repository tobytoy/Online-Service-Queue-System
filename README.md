# Online-Service-Queue-System
Open check service.

## env

```bash
python -m venv .venv
source .venv/bin/activate
```

# 線上取號系統

這是一個使用 Vue.js 前端和 Flask 後端的線上取號系統。

## 專案結構

- `frontend/`: 包含所有前端相關的檔案 (Vue.js, Vite, Tailwind CSS)。
- `clover/`: 包含後端伺服器 (Flask) 的 Python 程式碼。

## 安裝與啟動

### 環境設定

這個專案使用 Nix 來管理開發環境。`.idx/dev.nix` 檔案已經設定好所有必要的套件 (Python, Node.js, Flask)。當您第一次開啟這個工作區時，這些套件應該會自動安裝。

### 啟動步驟

1.  **啟動後端伺服器:**

    在終端機中，執行以下指令：

    ```bash
    python clover/app.py
    ```

    後端伺服器將會啟動在 `http://127.0.0.1:5001`。

2.  **啟動前端開發伺服器:**

    開啟一個**新的終端機分頁**，並切換到 `frontend` 目錄：

    ```bash
    cd frontend
    ```

    接著，安裝 npm 套件並啟動開發伺服器：

    ```bash
    npm install && npm run dev
    ```

    前端開發伺服器將會啟動，您可以在瀏覽器中開啟對應的網址 (通常是 `http://localhost:5173`) 來查看應用程式。
