import os
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

from main import main


load_dotenv()

DB_URL = os.environ.get('DATABASE_URL')
scheduler = BlockingScheduler()
scheduler.add_job(main, "interval", minutes=2)
scheduler.start()
