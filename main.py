import json
from datetime import datetime
from dotenv import load_dotenv

from graphql import getNewAnswers, getNewMarkets


def main():
    with open('timestamps.json', 'r+') as f:
        timestamps = json.load(f)
        getNewAnswers(timestamps['last_timestamp'])
        getNewMarkets(timestamps['last_timestamp'])
        timestamps['last_timestamp'] = datetime.now().timestamp()
        # go to the beggining of the file
        f.seek(0)
        json.dump(timestamps, f)


if __name__ == '__main__':
    load_dotenv()
    main()
