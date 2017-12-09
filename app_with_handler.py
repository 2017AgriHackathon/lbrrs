# -*- coding: utf-8 -*-


import os
import sys
from argparse import ArgumentParser
from lbrrs.database import config
from lbrrs.directory import Directory

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = 'f09331ba7c1060578fc98d2b7111293f'
channel_access_token = 'JQIQDl6ObDATW3X0vwicfNAbgENfQmXdBvLINSVrGVwf91NeXvsyfo7Sgl3qkNqnboSzMdX153AOPCANOczZTNHSx9m/A5/GWZJgp9JMGNrH0HpiSQ3UtMozXPvnfluvGPF/KJCTFgE/k+jHaScqKgdB04t89/1O/w1cDnyilFU='
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # print('running callback', file=sys.stdout)
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


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    if event.message.text=='安安':
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url='https://www.imgur.com/83ZTQ.jpg',
                preview_image_url='https://www.imgur.com/83ZTQ.jpg'
            )
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=d.get_today_price('番茄')), TextSendMessage(text='🍅')]
        )
    print(event.message.text, file=sys.stdout)


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=5050, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    config.setup_session('postgresql+psycopg2://postgres:1qaz@WSX@104.199.238.161/lbrrs')
    configs = Directory.get_configs()
    d = Directory()
    print('flask setting done', file=sys.stdout)

    app.run(debug=options.debug, port=options.port)
