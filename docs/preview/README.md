# 廣告合作指南：功能分支預覽

此分支供確認，尚未合併 main，未更動 GitHub Pages 發布設定。

- 區域：服務項目之後、聯絡表單之前。
- 功能：預設收合、原地展開全文、頁內目錄、同頁聯絡、文末收合並回到卡片。
- 全文直接存在 HTML；不依賴點擊後請求。停用 JavaScript 仍可使用原生 summary 展開／收合。
- 原文檔與使用者來源 SHA256 相同：68A59B8E60890A2C172E830899157D9FB201DE97ACCA5873D2BC270DBD4B56FA。
- 本次保留原稿，營收與損益、Meta 學習期及預算門檻等校稿建議待使用者另行確認。
- 僅保留同頁目錄功能；不提供獨立文章網址或外部直達段落功能，沿用首頁既有進站定位行為。

## 驗證

已驗證 1440、390、320 px 寬度；鍵盤展開、目錄、文末收合與焦點、無橫向溢出、停用 JavaScript 閱讀。原文所有段落及表格均出現在靜態 HTML；原有首頁區塊內容未改動。

測試：`node tests/article-browser.cjs`、`python tests/article-content.py`。瀏覽器測試使用此電腦 bundled Playwright 與已安裝 Chrome，換環境需調整路徑。HTML 產生器用於首次嵌入，後續更新需移除舊文章區後再執行，勿直接重跑。

## 實際畫面

![桌機收合](desktop-collapsed.png)

![手機展開](mobile-expanded.png)
