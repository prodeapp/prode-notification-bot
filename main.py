import json
import os
from datetime import datetime
from dotenv import load_dotenv

from graphql import getNewAnswers, getNewMarkets
from database import create_table, read_last_timestamp, write_last_timestamp


def main():
    with open('timestamps.json', 'r+') as f:
        timestamps = json.load(f)
        print("last timestamp that I've checked: {}"
              .format(datetime.fromtimestamp(
                  int(timestamps['last_timestamp']))))
        getNewAnswers(timestamps['last_timestamp'])
        getNewMarkets(timestamps['last_timestamp'])
        timestamps['last_timestamp'] = datetime.now().timestamp()
        # go to the beggining of the file
        f.seek(0)
        json.dump(timestamps, f)


if __name__ == '__main__':
    load_dotenv()
    # main()

    # create_table()
    print(read_last_timestamp())
    write_last_timestamp(int(datetime.timestamp(datetime.now())))