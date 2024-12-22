# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('2Tkmg4v0avF4cpnyiUNUoTntOXJD5kr09PG410XeRgtnbTkaHSd5N8i7iv5szizkF6Ri7ZMWPm329pJBiAaYDwQPGYQPCci5+g2CvCoTr2ozqAWchp+D0Yt4l/Md9GuNflhRJW1+7DTssZ2v9ZZFxAdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('b1623fdc44b582869d7aaf719342464d')

line_bot_api.push_message('U08e0b3334851a188dac8149bd83e74a0', TextSendMessage(text='你想查哪堂課'))

# 爬蟲
def fetch_course_info(selectno: int):
    """
    根據選課代碼爬取課程資訊
    """
    try:
        url = 'https://alcat.pu.edu.tw/choice/q_person.php'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.post(url, data={'selectno': selectno}, headers=headers, timeout=10)

        if response.status_code != 200:
            return f"伺服器回應錯誤，狀態碼: {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")

        # 找到科目名稱
        course_name_tag = soup.find('h2', string=lambda text: text and '科目名稱：' in text)
        if not course_name_tag:
            return "找不到科目名稱，請確認選課代碼是否正確。"

        # 初始化課程資訊
        course = {
            "科目名稱": course_name_tag.text.replace('科目名稱：', '').strip(),
            "人數上限": None,
            "修課人數": None,
            "人數餘額": None
        }

        # 提取表格數據
        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                key = cells[0].text.strip()
                value = cells[1].text.strip()
                if key in course:
                    course[key] = value

        # 計算餘額
        if course["人數上限"] is not None and course["修課人數"] is not None:
            course["人數餘額"] = course["人數上限"] - course["修課人數"]

        return (
            f"科目名稱: {course['科目名稱']}\n"
            f"人數上限: {course.get('人數上限', '未知')}\n"
            f"修課人數: {course.get('修課人數', '未知')}\n"
            f"人數餘額: {course['人數餘額']}"
        )

    except Exception as e:
        return f"選課代碼 {selectno} 發生錯誤：{e}"

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()  # 使用者輸入的文字

    # 分析多個選課代碼
    course_codes = [code.strip() for code in user_message.split() if code.isdigit()]

    if not course_codes:
        # 如果沒有有效代碼
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入有效的選課代碼（例如: 2876 2886）。")
        )
        return

    # 查詢所有選課代碼
    results = []
    for code in course_codes:
        response = fetch_course_info(int(code))
        results.append(f"選課代碼: {code}\n{response}\n{'-'*30}")

    # 回應查詢結果
    reply_message = "\n".join(results)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
