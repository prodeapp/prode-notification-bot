import os
import requests
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = '@prodeEventsNotifications'


def sendMessage(msg):
    params = {'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'MarkDown'}
    try:
        res = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}'
                            '/sendMessage', data=params).json()
    except Exception as e:
        print(e)
        res = None
    return res


def sendNewMarket(market_name, market_address):
    text = ('New market has been created!.\n\n'
            'Place your [bets](http://prode.market/#/markets/'
            f'{market_address.lower()}) in the {market_name}!')
    sendMessage(text)


def sendNewAnswer(question, answer, bond):
    text = (f'New Answer in a Prode Event!\n\n'
            f'Question: {question}\n'
            f'Current Answer: {answer}\n\n'
            f'Review it to win the deposit of {bond} xDAI'
            )
    sendMessage(text)
