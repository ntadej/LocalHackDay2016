from flask import Flask, request, Response
from gevent import spawn
from gevent.queue import Queue

from sse import ServerSentEvent

from crossdomain import crossdomain

app = Flask(__name__)
subscriptions = []

pixels = "         "
current_player = "x"

@app.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)

@app.route("/status")
def status():
    global current_player

    change = str(request.args["change"])

    if change == "player":
        if current_player == "x":
            current_player = "o"
        else:
            current_player = "x"

    def notify():
        msg = change
        for sub in subscriptions[:]:
            sub.put(msg)

    spawn(notify)

    return str(request.args["change"])

@app.route("/target")
def target():
    change = str(request.args["pixels"])

    for i in range(len(change)):
        if pixels[i] == " " and change[i] == "1":
            pixels[i] = current_player

    def notify():
        msg = pixels
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
