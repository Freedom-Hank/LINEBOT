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

    if re.match('電影推薦', message):
        image_carousel_template_message = TemplateSendMessage(
            alt_text='電影推薦清單',
            template=ImageCarouselTemplate(
                columns=[
                    # 電影 1
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/sW4C2DQ.jpeg',
                        action=MessageAction(
                            label='電影 1：星際效應',
                            text='《星際效應》：2014年上映，克里斯多福·諾蘭執導的經典科幻電影。'
                        )
                    ),
                    # 電影 2
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/WWXT5y8.jpeg',
                        action=MessageAction(
                            label='電影 2：復仇者聯盟',
                            text='《復仇者聯盟》：2012年上映，漫威英雄集結，史詩級動作電影。'
                        )
                    ),
                    # 電影 3
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/U43AmNa.jpeg',
                        action=MessageAction(
                            label='電影 3：哈利波特',
                            text='《哈利波特》：2001年上映，奇幻魔法世界，哈利的冒險故事開始了！'
                        )
                    ),
                    # 電影 4
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/Vz5Dd2n.jpeg',
                        action=MessageAction(
                            label='電影 4：寄生上流',
                            text='《寄生上流》：2019年上映，韓國經典黑色喜劇，榮獲奧斯卡最佳影片！'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
    else:
        # 預設回覆
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入『電影推薦』查看最新電影資訊！"))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
