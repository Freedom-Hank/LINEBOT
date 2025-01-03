# 選課小幫手
## 專案介紹
本專案是一個基於 Flask 框架開發的 LINE Bot，結合爬蟲技術，讓使用者可以輸入選課代碼，快速查詢課程資訊（如課程名稱、人數上限、修課人數及人數餘額）。該專案已部署於 Render 平台，並可穩定運行。

## 功能介紹
* 課程查詢：
  * 用戶輸入選課代碼（如 2876），即時獲取課程資訊。
* 多選課代碼查詢：
  * 支援一次性查詢多個課程，並返回詳細資訊。
* 即時回應：
  * 支援即時查詢，返回結果不延遲。
* 錯誤處理：
  * 輸入格式錯誤或伺服器問題時，提供友善提示。

## 應用技術
* 後端框架： Flask
* 爬蟲技術： BeautifulSoup
* LINE 平台： LINE Messaging API
* 部署平台： Render

## 安裝與使用
1. 安裝環境
   * Python 3.7 或以上版本
   * 套件管理工具 pip
2. 複製專案
   ```
   git clone https://github.com/your-repository/linebot-course-info.git
   cd linebot-course-info
   ```
3. 安裝所需套件
   pip install -r requirements.txt

## Render 部署
1. 登入 Render
   * 登入帳號
   * 點擊 New > Web Service
2. 上傳專案
   * 將專案上傳至 GitHub 並連結到 Render
   * 配置專案的部署設置
     * Environment: Python 3.x
     * Build Command: pip install -r requirements.txt
     * Start Command: python app.py
3. 部署與測試
   部署完成後，Render 會生成一個公開的 URL，將該 URL 設定為 LINE Messaging API 的 Webhook URL，並在後方加上/callback

## 使用方式
1. 添加 LINE BOT 為好友
2. 查詢課程資訊
   * 單一課程查詢： 輸入選課代碼（如 2876），BOT 會回應該課程的詳細資訊，例如:
     ```
     科目名稱: 日文科教學實習
     人數上限: 40
     修課人數: 14
     人數餘額: 26
     ------------------------------
     ```
   * 多選課代碼查詢： 輸入多個選課代碼（以空格分隔，例如 2876 2987），BOT 會返回每個課程的詳細資訊，例如:
     ```
     科目名稱: 日文科教學實習
     人數上限: 40
     修課人數: 14
     人數餘額: 26
     ------------------------------
     選課代碼: 2876
     科目名稱: 日文科教學實習
     人數上限: 40
     修課人數: 17
     人數餘額: 23
     ------------------------------
     ```

## 未來改進
* 提供課程名稱或教師名稱查詢功能。
* 支援課程訂閱，當課程資訊更新時通知用戶。
* 增加操作日誌以記錄用戶行為。
