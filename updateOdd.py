import time
import urllib2

import schedule


def job():
    while True:
        try:
            response = urllib2.urlopen('http://localhost:8088/updateOdds/')
            html = response.read()
            break
        except Exception as e:
            print 'retry'


schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
