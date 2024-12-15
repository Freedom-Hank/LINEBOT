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
    if re.match('我要訂餐',message):
        # 第一步：顯示訂餐資訊
        order_message = TextSendMessage(text="【無敵好吃牛肉麵 * 1 ，總價 NT200】")

        # 第二步：顯示 ConfirmTemplate 確認訂單
        confirm_template_message = TemplateSendMessage(
            alt_text='訂單確認',
            template=ConfirmTemplate(
                text='請確認您的訂單：無敵好吃牛肉麵 * 1 ，總價 NT200',
                actions=[
                    PostbackAction(
                        label='確定',
                        display_text='確定',
                        data='action=confirm_order'
                    ),
                    PostbackAction(
                        label='取消',
                        display_text='取消',
                        data='action=cancel_order'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,  [order_message, confirm_template_message] )
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

# Postback 處理邏輯
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data

    if data == 'action=confirm_order':
        # 使用者點擊「確定」
        reply_text = "訂單已確認，謝謝您的購買！"
    elif data == 'action=cancel_order':
        # 使用者點擊「取消」
        reply_text = "已取消訂單，謝謝您的光臨！"
    else:
        reply_text = "發生錯誤，請重新操作！"

    # 回覆訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
