import os
import requests
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = '@prodeEventsNotifications'


def sendMessage(msg):
    params = {'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'MarkDown'}
    return requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                         data=params).json()


def sendNewMarket(marketInfo, market_address):
    text = ('New market has been created!.\n\n'
            'Place your [bets](http://prode.market/#/markets/'
            f'{market_address.toLower()}) in the {marketInfo[3]}!')
    sendMessage(text)
    sendMessage(text)
