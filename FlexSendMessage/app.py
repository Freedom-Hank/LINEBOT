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
    message = event.message.text.strip()
    if re.match('查看菜單',message):
        # Flex Message Simulator網頁：https://developers.line.biz/console/fx/
        flex_message = FlexSendMessage(
            alt_text='餐廳菜單',
            contents={
                "type": "carousel",
                "contents": [
                    # 第一道菜
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://i.imgur.com/EZtkARu.png",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "contents": [
                                {"type": "text", "text": "日式拉麵", "size": "xl", "weight": "bold"},
                                {"type": "text", "text": "濃厚豚骨湯頭，搭配彈牙麵條", "wrap": True, "color": "#aaaaaa", "size": "sm"},
                                {"type": "text", "text": "NT 160", "size": "lg", "weight": "bold", "color": "#ff5551"}
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "action": {
                                        "type": "message",
                                        "label": "訂購",
                                        "text": "已將【日式拉麵】加入購物車"
                                    }
                                }
                            ]
                        }
                    },
                    # 第二道菜
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://i.imgur.com/kWVCmKD.jpeg",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "contents": [
                                {"type": "text", "text": "香煎牛排", "size": "xl", "weight": "bold"},
                                {"type": "text", "text": "犇頂牛排，外酥內嫩", "wrap": True, "color": "#aaaaaa", "size": "sm"},
                                {"type": "text", "text": "NT 190", "size": "lg", "weight": "bold", "color": "#ff5551"}
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "action": {
                                        "type": "message",
                                        "label": "訂購",
                                        "text": "已將【香煎牛排】加入購物車"
                                    }
                                }
                            ]
                        }
                    },
                    # 第三道菜
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://i.imgur.com/K9iRIe3.jpeg",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "contents": [
                                {"type": "text", "text": "石鍋炒飯", "size": "xl", "weight": "bold"},
                                {"type": "text", "text": "石鍋加熱，用料實在，風味絕佳", "wrap": True, "color": "#aaaaaa", "size": "sm"},
                                {"type": "text", "text": "NT 240", "size": "lg", "weight": "bold", "color": "#ff5551"}
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "action": {
                                        "type": "message",
                                        "label": "訂購",
                                        "text": "已將【石鍋拌飯】加入購物車"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)

    else:
        # 預設回覆
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入『查看菜單』查看我們的餐點！"))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
