from flask import Flask
from flask_restful import Resource, Api
import yaml
import threading
import datetime
import time
from urllib.request import urlopen
from models import *
from mongoengine import connect

connect('timelogger')


class CheckThread(threading.Thread):
    def __init__(self, threadID, url, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.url = url
        self.delay = delay

    def run(self):
        print('Check response: ', self.url)
        check_response(self.url, self.delay)


def check_response(url,delay):
    connect('timelogger')
    while True:
        start = datetime.datetime.now()
        resp = urlopen(url)
        end = datetime.datetime.now()
        resp_time = end -start
        timelog = TimeLog(request_time=datetime.datetime.now(),
                          url=url, response_time=round(resp_time.total_seconds(), 2),
                          response_code=resp.getcode())
        timelog.save()

        time.sleep(delay)

app = Flask(__name__)
api = Api(app)
app.debug = True


config = yaml.load(open('config.yml','r'))

for i in config['urls']:
    thread = CheckThread(config['urls'].index(i), i['url'], i['delay'])
    thread.start()


class TimeLogger(Resource):
    def get(self):
        output = []
        for log in TimeLog.objects:
            output.append({"Timestamp": log.request_time.isoformat(),
                           "url": log.url, "response_time": log.response_time,
                           "response_code": log.response_code})
        return output


api.add_resource(TimeLogger, '/')


if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
