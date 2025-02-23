from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import os
from linebot import LineBotApi    #line-bot-sdk：用於發送 Line Bot 訊息與圖片通知。
from linebot.models import TextSendMessage, ImageSendMessage

app = Flask(__name__)

LINE_BOT_TOKEN = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
LINE_USER_ID =WebhookHandler(os.getenv('CHANNEL_SECRET'))
line_bot_api = LineBotApi(LINE_BOT_TOKEN)

@app.route('/')
def home():
    return"X1X1"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        LINE_USER_ID.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@LINE_USER_ID.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(LINE_BOT_TOKEN) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

if __name__ == "__main__":
    app.run()