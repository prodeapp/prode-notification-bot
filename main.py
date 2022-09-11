import json
import os
from datetime import datetime
from dotenv import load_dotenv

from graphql import getNewAnswers, getNewMarkets
from database import read_last_timestamp, write_last_timestamp


def main():

    timestamps = read_last_timestamp()
    print("last timestamp that I've checked: {}"
          .format(datetime.fromtimestamp(
              int(timestamps['last_timestamp']))))
    getNewAnswers(timestamps['last_timestamp'])
    getNewMarkets(timestamps['last_timestamp'])
    write_last_timestamp(int(datetime.now().timestamp()))


if __name__ == '__main__':
    load_dotenv()
    main()
