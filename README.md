# 股票申購小幫手

## LINE bot

* 功能: 點按圖文選單即可收到值得申購的股票資訊 (報酬率>10%)
* 主程式: func.py

### 使用工具

* Python
* Django
* LINE Bot API
* ngrok (測試)
* Heroku (部署)

### 實際使用截圖

![stock_public_linebot](demo_imgs/demo20200409.jpg)

---

## Beta version (LINE bot 前身)

stock_public.py

* 列出目前可申購 & 報酬率>10% 的股票代號與名稱
* Input: 使用者輸入欲抽的股票
* Output: 申購 XXXX股票: 請設定【日期】轉帳【金額】元
* 同時將 output 存入以當日日期為名稱的 txt 檔，做為紀錄

![stock_public](demo_imgs/stock_public_demo.png)
