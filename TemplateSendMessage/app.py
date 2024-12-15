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
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('eeQGzjzKcpLE0NGAbNPph/OKtkvUK4qwusKE2s30VKqkk2YjIs8z6vcQTLlQ2txu6bRBj7WXBYbdVZ0Es9l1+sj4cHkd0CVyC8PmIjFmGvRohqtnpJ7uJKAE+4rERncihjErfjsUnQJp/jsE1fqmrAdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('c3155b740fe5557ebb82049435be6ae8')

line_bot_api.push_message('U08e0b3334851a188dac8149bd83e74a0', TextSendMessage(text='你可以開始了'))

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
    message = event.message.text
    if re.match('推薦景點',message):
        buttons_template_message = TemplateSendMessage(
        alt_text='推薦旅遊景點',
        template=CarouselTemplate(
            columns=[
                # 景點 1
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/xPSPblU.jpeg',
                    title='台北 101',
                    text='台北地標，必訪景點！',
                    actions=[
                        URIAction(
                            label='查看詳細資訊',
                            uri='https://www.taipei-101.com.tw/'
                        ),
                        MessageAction(
                            label='導航至景點',
                            text='導航至 台北101'
                        )
                    ]
                ),
                # 景點 2
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/JSfNO0H.jpeg',
                    title='日月潭',
                    text='台灣南投縣著名風景區!',
                    actions=[
                        URIAction(
                            label='查看詳細資訊',
                            uri='https://www.sunmoonlake.gov.tw/'
                        ),
                        MessageAction(
                            label='導航至景點',
                            text='導航至 日月潭'
                        )
                    ]
                ),
                # 景點 3
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/yJK9Ar5.jpeg',
                    title='九份老街',
                    text='充滿懷舊氣息的山城老街!',
                    actions=[
                        URIAction(
                            label='查看詳細資訊',
                            uri='https://www.travel.taipei/zh-tw/attraction/details/1672'
                        ),
                        MessageAction(
                            label='導航至景點',
                            text='導航至 九份老街'
                        )
                    ]
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
