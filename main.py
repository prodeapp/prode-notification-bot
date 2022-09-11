from datetime import datetime
from dotenv import load_dotenv

from graphql import getNewAnswers, getNewMarkets
from database import read_last_timestamp, write_last_timestamp


def main():

    timestamp = read_last_timestamp()
    if timestamp is None:
        print("No timestamp found in the database")
        return
    print("last timestamp that I've checked: {}"
          .format(datetime.fromtimestamp(
              int(timestamp))))
    getNewAnswers(timestamp)
    getNewMarkets(timestamp)
    write_last_timestamp(int(datetime.now().timestamp()))


if __name__ == '__main__':
    load_dotenv()
    main()
