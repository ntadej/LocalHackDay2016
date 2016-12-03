from flask import Flask, request, Response
from gevent import spawn
from gevent.queue import Queue

from sse import ServerSentEvent

import time

from crossdomain import crossdomain

app = Flask(__name__)
subscriptions = []

@app.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)

@app.route("/target")
def target():
    def notify():
        msg = str(request.args["pixels"])
        for sub in subscriptions[:]:
            sub.put(msg)

    spawn(notify)

    return str(request.args["pixels"])

@app.route("/subscribe")
@crossdomain(origin='*')
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit: # Or maybe use flask signals
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")
