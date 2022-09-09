from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

from main import main


load_dotenv()

scheduler = BlockingScheduler()
scheduler.add_job(main, "interval", minutes=5)
scheduler.start()
