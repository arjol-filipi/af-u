from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from news.sc import scrappTop

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrappTop, 'interval', minutes=30)
    scheduler.start()