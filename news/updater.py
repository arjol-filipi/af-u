from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from news.sc import scrappTop,scrappKlan

def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(scrappTop, 'interval', minutes=30)
    # scheduler.add_job(scrappKlan, 'interval', minutes=10)
    
    scheduler.start()