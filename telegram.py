import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = '@prodeEventsNotifications'


def sendMessage(msg, button=None):
    params = {'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'MarkDown'}
    if button is not None:
        params["reply_markup"] = json.dumps(
            {"inline_keyboard":
             [
                 [
                     {"text": button['text'],
                      "url": button['url']
                      }
                 ]
             ]
             })
    try:
        res = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}'
                            '/sendMessage', data=params).json()
    except Exception as e:
        print(e)
        res = None
    return res

