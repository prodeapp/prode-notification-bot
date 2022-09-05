import os
import requests
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = '@prodeEventsNotifications'


def sendMessage(msg):
    params = {'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'MarkDown'}
    res = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', data=params).json()
    print(res)


def sendNewMarket(marketInfo):
    text = ('New market has been created!.\n\n'
            f'Place your [bets](http://prode.market/#/markets/{marketInfo[3]})'
            f' in the {marketInfo[3]}!')
    sendMessage(text)
