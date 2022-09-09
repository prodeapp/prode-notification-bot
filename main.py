import json
from datetime import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

from graphql import getNewAnswers, getNewMarkets

load_dotenv()


def main():
    with open('timestamps.json', 'r+') as f:
        timestamps = json.load(f)
        getNewAnswers(timestamps['last_timestamp'])
        getNewMarkets(timestamps['last_timestamp'])
        timestamps['last_timestamp'] = datetime.now().timestamp()
        f.write(json.dumps(timestamps, indent=4))


scheduler = BlockingScheduler()
scheduler.add_job(main, "interval", minutes=5)
scheduler.start()
