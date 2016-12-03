from flask import Flask, request, Response
from gevent import spawn
from gevent.queue import Queue

from sse import ServerSentEvent

from crossdomain import crossdomain

app = Flask(__name__)
subscriptions = []

pixels = [" " for i in range(9)]
current_player = "x"

@app.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)

@app.route("/status")
def status():
    global pixels
    global current_player

    change = ""

    if request.args["change"] == "player":
        if current_player == "x":
            current_player = "o"
        else:
            current_player = "x"
        change = current_player
    else:
        pixels = [" " for i in range(9)]
        change = "".join(pixels)

    def notify():
        msg = change
        for sub in subscriptions[:]:
            sub.put(msg)

    spawn(notify)

    return str(request.args["change"])

@app.route("/target")
def target():
    change = str(request.args["pixels"])

    for i in range(len(pixels)):
        if pixels[i] == " " and change[i] == "0":
            pixels[i] = current_player

    def notify():
        msg = "".join(pixels)
        for sub in subscriptions[:]:
            sub.put(msg)

    spawn(notify)

    return str(request.args["pixels"])

@app.route("/subscribe")
@crossdomain(origin='*')
def subscribe():
    def notify():
        msg = str(len(subscriptions))
        for sub in subscriptions[:]:
            sub.put(msg)

    def gen():
        q = Queue()
        subscriptions.append(q)
        spawn(notify)
        try:
            while True:
                result = q.get()
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit: # Or maybe use flask signals
            subscriptions.remove(q)
            spawn(notify)

    return Response(gen(), mimetype="text/event-stream")
