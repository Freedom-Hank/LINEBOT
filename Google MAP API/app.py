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
import os
import googlemaps  # 用於 Google Maps API


app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('eeQGzjzKcpLE0NGAbNPph/OKtkvUK4qwusKE2s30VKqkk2YjIs8z6vcQTLlQ2txu6bRBj7WXBYbdVZ0Es9l1+sj4cHkd0CVyC8PmIjFmGvRohqtnpJ7uJKAE+4rERncihjErfjsUnQJp/jsE1fqmrAdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('c3155b740fe5557ebb82049435be6ae8')

# Google Maps API Key
google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=google_maps_api_key)


line_bot_api.push_message('U08e0b3334851a188dac8149bd83e74a0', TextSendMessage(text='請輸入關鍵字（例如「公園」、「咖啡廳」），我會幫您附近位置！'))

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
    # 使用 Google Places API 查詢地點
    places_result = gmaps.places(query=user_message, location=(24.2299, 120.5726), radius=5000)  # 設定查詢範圍為 5 公里
    if places_result['status'] == 'OK' and places_result['results']:
        # 取得第一個結果
        place = places_result['results'][0]
        place_name = place['name']
        place_address = place['formatted_address']
        place_lat = place['geometry']['location']['lat']
        place_lng = place['geometry']['location']['lng']

         # 回傳位置訊息
        location_message = LocationSendMessage(
            title=place_name,
            address=place_address,
            latitude=place_lat,
            longitude=place_lng
        )
        line_bot_api.reply_message(event.reply_token, location_message)
    else:
        # 沒有找到結果
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="很抱歉，我找不到相關位置，請換個關鍵字試試！")
        )

#主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
