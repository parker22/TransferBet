import schedule
import time
import urllib2

def job():
	response = urllib2.urlopen('http://localhost:8088/updateOdds/')
	html = response.read()

schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
