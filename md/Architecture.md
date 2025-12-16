# 🏗️ 專案名稱：線上服務查詢與叫號系統（Online Service Queue System）

## 🎯 使用者故事（User Story）

開發一個 類手機 App 的 Web App（使用 Vite + PWA），提供查詢叫號進度與管理員叫號作業。

# 🧱 技術架構（Tech Stack）

## 前端（Frontend）

* Vite
* Vue 3
* vite-plugin-pwa（提供 PWA、manifest、自動更新）
* TailwindCSS（或 Ant Design Vue）
* 前端角色介面：
    * 一般使用者（public）
    * 管理員（fixed account/password，本地驗證即可）

## 後端（Backend）

* Google Apps Script
    * GET /read：公開讀取資料
    * POST /update：私有寫入（需 API KEY）

## 資料庫（Database）
* Google Sheet

# 📝 Google Sheet Schema（固定欄位格式）
## Row 1：系統全域資訊

欄位 | 說明
:---|:---
current_number  | 目前輪到的號碼
waiting_numbers | 自由等待號碼（逗號分隔）

## Row 2+：各服務窗口

window_name | current_serving | window_queue
:---|:---|:---
A窗口 | 15 | 16,17
B窗口 | 20 | 21,22

# 🧩 前端功能（含管理員三層下拉邏輯）
## 一般使用者 View

顯示資訊：

* 目前號碼（全域）
* 自由等待號碼（全域）
* 各窗口狀態（名稱、目前服務號、等待中）

資料取得方式：呼叫 GAS /read

# 🔐 管理員介面（重點：三個下拉 + 動態業務邏輯）

管理員登入後看到 3 個下拉與一個「執行按鈕」：

## 🥇 第一下拉：操作類型（action）

選項：

* 新增號碼
* 完成服務並叫下一號（窗口完成）

對應後端 action：

* 新增號碼 → add_waiting
* 完成窗口 → finish_window

## 🥈 第二下拉：窗口選擇

* 0：自由等待區（waiting list）
* 1：A 窗口
* 2：B 窗口
* …
（可依實際窗口數調整）

規則：

* 當第一下拉＝新增號碼 → 第二下拉一定要允許選 0（自由等待）
* 當第一下拉＝完成服務 → 第二下拉不允許選 0，只能選窗口 1、2、3...

## 🥉 第三下拉：選擇下一個服務號碼（動態）

依第二下拉更新內容：
### 若第二下拉選「0（自由等待區）」

顯示：

* 所有自由等待號碼（waiting_numbers）

### 若第二下拉選「A窗口」

顯示：

* A窗口等待名單 (window_queue)
* ＋ 自由等待號碼（視業務邏輯而定，可選擇加入）

### 若第一下拉＝完成服務 → 第三下拉自動選下一號

例如：

* A窗口 current = 12
* A窗口 queue = [13, 14, 15]
→ 完成操作後，next = 13（自動填入，不需手動選）

## ⚙️ 三層下拉的前端邏輯（Pseudo Code）

```js
watch(actionSelection, () => {
  if (actionSelection === "新增號碼") {
    windowOptions = ["0: 自由等待", ...allWindows]
  } else if (actionSelection === "完成服務") {
    windowOptions = allWindows  // 不含 0
  }
  selectedWindow = null
  nextNumberOptions = []
})

watch(selectedWindow, () => {
  if (selectedWindow === 0) {
    nextNumberOptions = waitingNumbers
  } else {
    const win = windowData[selectedWindow]
    if (actionSelection === "完成服務") {
      nextNumberOptions = [win.queue[0] || null] // 自動填入
    } else {
      nextNumberOptions = [...win.queue, ...waitingNumbers]
    }
  }
})
```

# 🔁 GitHub Issue → GitHub Action → Google Sheet（完整流程）

管理員按「執行」 → 前端 POST GitHub Issue API
Issue 格式：

```bash
/add 35
```

或：

```bash
/finish A
```

GitHub Action 解析後：

* /add 35 → 呼叫 GAS /update → { action: "add_waiting", number: 35 }
* /finish A → { action: "finish_window", window: "A" }

# 🔧 Google Apps Script API（更新版）

GET /read

回傳：

```json
{
  "current_number": "15",
  "waiting_numbers": ["16", "17"],
  "windows": [
    {
      "key": "1",
      "name": "A窗口",
      "current": "15",
      "queue": ["16", "17"]
    }
  ]
}
```

## POST /update

需帶 API KEY。

## 請支援下列動作：

### 1️⃣ add_waiting

加入自由等待區

Body:

```json
{ "action": "add_waiting", "number": "35" }
```

### 2️⃣ finish_window

將某窗口的 current_serving 移除，並將 queue 第一個號碼移到 current

Body:

```json
{ "action": "finish_window", "window": "A" }
```

GAS 要做：

* current_serving = queue.shift()
* queue = queue.slice(1)

# 📱 PWA 設定（vite-plugin-pwa）

請在專案中加入以下設定：

## vite.config.js 增補

```js
import { VitePWA } from 'vite-plugin-pwa'

export default {
  plugins: [
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.svg'],
      manifest: {
        name: '線上服務叫號系統',
        short_name: '叫號系統',
        start_url: '/',
        display: 'standalone',
        theme_color: '#ffffff',
        background_color: '#ffffff',
        icons: [
          {
            src: '/pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    })
  ]
}
```

# 📌 產生專案請求（Deliverables to Vibe Coding）

請依照上述完整規格：

1. 建立 Vite + Vue3 + PWA 專案
2. 完整前端 UI：
    * 使用者頁面
    * 管理者頁面（三層下拉含動態邏輯）
3. GAS 後端
4. GitHub Actions 自動 issue parser
5. Google Sheet 読寫邏輯
6. 完整程式架構（檔案路徑明確）
7. 所有功能能整合成可部署的專案
