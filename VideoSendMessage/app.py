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

line_bot_api.push_message('U08e0b3334851a188dac8149bd83e74a0', TextSendMessage(text='你想找什麼樣的影片'))

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
    if re.match('Live',message):
        video_message = VideoSendMessage(
            original_content_url='https://campus-studio.com/download/cr.mp4',
            preview_image_url='https://campus-studio.com/download/cr.jpg'
        )
        line_bot_api.reply_message(event.reply_token, video_message)
    else:
        message = TextSendMessage("抱歉，沒有這類型的影片")
        line_bot_api.reply_message(event.reply_token,message)
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
