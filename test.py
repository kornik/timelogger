
import threading
import datetime
import time
from urllib.request import urlopen
from models import TimeLog


class checkThread(threading.Thread):
    def __init__(self, threadID, url, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.url = url
        self.delay = delay

    def run(self):
        print('Check response: ', self.url)
        check_response(self.url, self.delay)

def check_response(url,delay):
    while True:
        start = datetime.datetime.now()
        resp = urlopen(url)
        end = datetime.datetime.now()
        resp_time = end -start

        response_data = TimeLog()
        response_data.request_time=datetime.datetime.now()
        response_data.url = url
        response_data.response_time = round(resp_time.total_seconds(), 2)
        response_data.response_code = resp.getcode()
        response_data.save()
        time.sleep(delay)




