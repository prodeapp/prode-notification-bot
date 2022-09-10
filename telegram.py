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


def sendNewMarket(market_name, market_address, bet_price, bet_deadline):
    bet_deadline_date = datetime.fromtimestamp(
        int(bet_deadline)).strftime('%Y-%m-%d %H:%M')
    text = ('New market has been created!.\n\n'
            f'*Name: {market_name}*\n\n'
            f'Bet Price: {bet_price:.2f} xDAI\n\n'
            f'Hurry Up!, you have time until {bet_deadline_date}')
    button = {'text': 'Place Your Bet',
              'url': 'https://prode.market/#/markets/{}'.format(
                  market_address.lower())}
    sendMessage(text, button)


def sendNewAnswer(question, answer, bond, market_name, market_id, changed):
    if changed is True:
        text = 'Someone has changed the answer in this Prode Event!\n\n'
    else:
        text = 'This is the first answer in this Prode Event!\n\n'
    text += (f'*Market: {market_name}*\n\n'
             f'Question: {question}\n\n'
             f'Current Answer: {answer}\n\n'
             f'Review it to win the deposit of {bond} xDAI'
             )
    button = {'text': '*Review Result*',
              'url': 'https://prode.market/#/markets/{}'.format(market_id)}
    sendMessage(text, button)
