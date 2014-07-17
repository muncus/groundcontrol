#!/usr/bin/env python

import gevent
import gevent.monkey
import sseclient
import json
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from flask import Flask, request, Response, render_template

app = Flask(__name__)

#event_data = {'name': "foo", "value": True}
event_data = {'name': "foo", "action": "toggle"}

def event_stream():
    while True:
        gevent.sleep(2)
        #event_data['value'] = not event_data['value']
        yield 'data: %s\n\n' % json.dumps(event_data)

@app.route('/e')
def sse_request():
    return Response(
            event_stream(),
            mimetype='text/event-stream')

@app.route('/')
def page():
    return render_template('sse.html')

if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 8001), app)
    http_server.serve_forever()
