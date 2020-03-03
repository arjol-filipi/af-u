from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from news.sc import scrappTop,scrappKlan



sched = BlockingScheduler()
# @sched.scheduled_job( 'interval', minutes=3)
# def sct():  
#     scrappTop()
# @sched.scheduled_job( 'interval', minutes=1)
# def sck():
#     scrappKlan()
# @sched.scheduled_job('interval', days=1)
# def delO():
    # deleteOld()

sched.start()