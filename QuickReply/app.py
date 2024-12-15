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

line_bot_api.push_message('U08e0b3334851a188dac8149bd83e74a0',TextSendMessage(text='你可以開始了'))

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
    message = event.message.text.strip()
    if re.match('我想吃飯', message):
        quick_reply_message = TextSendMessage(
            text="請選擇您要加入購物車的品項：",
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="主菜", text="主菜")),
                QuickReplyButton(action=MessageAction(label="湯品", text="湯品")),
                QuickReplyButton(action=MessageAction(label="飲料", text="飲料"))
            ])
        )
        line_bot_api.reply_message(event.reply_token, quick_reply_message)
    
    # 使用者選擇 QuickReply 選項
    elif message in ["主菜", "湯品", "飲料"]:
        reply_message = f"您已成功將【{message}】加入購物車"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
    
    # 預設回覆
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入『我想吃飯』來開始點餐吧！"))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
