import requests

from telegram import sendNewAnswer, sendNewMarket
from helpers import formatAnswer


SUBGRAPH_API = "https://api.thegraph.com/subgraphs/name/prodeapp/prodeapp"


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
            lastBond
            templateID
            markets{name, id}
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
            sendNewAnswer(event['title'], answer, _wei2eth(event['lastBond']),
                          event['markets'][0]['name'],
                          event['markets'][0]['id'])
    else:
        print("No new answers")


if __name__ == '__main__':
    from datetime import datetime
    lastTimestamp = datetime(2022, 9, 1, 0, 0, 0, 0).timestamp()
    getNewMarkets(lastTimestamp)
    # getNewAnswers(lastTimestamp)
