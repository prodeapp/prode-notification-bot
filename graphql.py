import requests

from telegram import sendMessage
from twitter import post_tweet
from helpers import formatAnswer
from datetime import datetime


SUBGRAPH_API = "https://api.thegraph.com/subgraphs/name/prodeapp/prodeapp"

MEDAL_1 = '\U0001F947'
MONOCLE = '\U0001f9d0'
MONEY_FACE = '\U0001f911'


def _post_query(query):
    response = requests.post(SUBGRAPH_API, json={'query': query})
    data = response.json()
    try:
        data = data['data']
    except KeyError:
        print("Error: ", data['errors'])
        return None
    data_length = 0
    for key in data.keys():
        if len(data[key]) != 0:
            data_length += 1
            break
    if data_length > 0:
        return data
    else:
        return None


def _wei2eth(gwei):
    return float(gwei) * 10**-18


def getNewMarkets(timestamp):
    """Get the markets created after a timestamp"""
    query = (
        "{markets(where:{creationTime_gt:" + str(int(timestamp)) + "},"
        "orderBy:creationTime, orderDirection:asc){"
        """
            name
            id
            category
            closingTime
            price
            category
            }
        }
        """
    )
    data = _post_query(query)
    if data is not None:
        for market in data['markets']:
            print(f"New Market {market['name']}")
            sendNewMarket(market['name'], market['id'],
                          _wei2eth(market['price']),
                          market['closingTime'])
    else:
        print("No new markets")


def getNewAnswers(timestamp):
    """Get the markets created after a timestamp"""
    query = (
        "{events(where:{lastAnswerTs_gt:" + str(int(timestamp)) + "},"
        "orderBy:lastAnswerTs, orderDirection:asc){"
        """
            title
            outcomes
            finalizeTs
            answer
            minBond
            lastBond
            templateID
            markets{name, id, category}
            }
        }
        """
    )
    data = _post_query(query)
    if data is not None:
        for event in data['events']:
            answer = formatAnswer(event['answer'],
                                  event['templateID'],
                                  event['outcomes'])
            print(f"New Answer for {event['title']}")
            changed_answer = float(event['lastBond']) > float(event['minBond'])
            sendNewAnswer(event['title'], answer, _wei2eth(event['lastBond']),
                          event['markets'][0]['name'],
                          event['markets'][0]['id'],
                          changed_answer
                          )
    else:
        print("No new answers")


def sendNewMarket(market_name, market_address, bet_price, bet_deadline,
                  category=None):
    bet_deadline_date = datetime.fromtimestamp(
        int(bet_deadline)).strftime('%Y-%m-%d %H:%M')
    text = ('New market has been created!.\n\n'
            f'*Name: {market_name}*\n\n'
            f'Bet Price: {bet_price:.2f} xDAI\n\n'
            f'Hurry Up!, you have time until {bet_deadline_date}')
    button = {'text': MEDAL_1 + ' Place Your Bet ' + MEDAL_1,
              'url': 'https://prode.market/#/markets/{}'.format(
                  market_address.lower())}
    sendMessage(text, button)
    post_tweet(text)


def sendNewAnswer(question, answer, bond, market_name, market_id, changed,
                  category=None):
    if changed is True:
        base_text = MONOCLE + ' Someone has changed the answer in this Prode' \
            + ' Event!\n\n'
    else:
        base_text = MONOCLE + ' This is the first answer in this Prode ' \
            + 'Event!\n\n'
    text = base_text + (f'*Market: {market_name}*\n\n'
                        f'Question: {question}\n\n'
                        f'Current Answer: {answer}\n\n'
                        f'Review it to win a bond of {bond} xDAI'
                        )
    button = {'text': 'Review Result and earn the bond ' + MONEY_FACE,
              'url': 'https://prode.market/#/markets/{}'.format(market_id)}
    sendMessage(text, button)
    text = (base_text + f'Q: {question}\n'
            f'A: {answer}\n' + f'Review to earn the {bond} xDAI bond '
            + MONEY_FACE + f'\nhttps://prode.market/#/markets/{market_id}')
    post_tweet(text)


if __name__ == '__main__':
    lastTimestamp = datetime(2022, 9, 9, 0, 0, 0, 0).timestamp()
    # getNewMarkets(lastTimestamp)
    getNewAnswers(1661860740)
