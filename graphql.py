import requests

from telegram import sendNewMarket


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
            sendNewMarket(market['name'], market['id'])


if __name__ == '__main__':
    from datetime import datetime
    print(datetime(2022, 9, 1, 0, 0, 0, 0).timestamp())
    getNewMarkets(datetime(2022, 9, 1, 0, 0, 0, 0).timestamp())
