from flask import Flask, render_template
from flask_socketio import SocketIO

import Scroller
from threading import Lock
import time

application = Flask(__name__)
application.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(application)
thread = None
thread_lock = Lock()

def squaresEmitter(squares):
    # print(squares)
    socketio.emit('my response', squares)

def background_thread():
    print("starting thread")
    s = Scroller.Scroller(squaresEmitter)
    s.scrollText("Snorlax!!", socketio, 0, 255, 0)
    while True:
        print("banana")
        s.scrollText("Banana   ", socketio, 0, 0, 255)

@application.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(application, debug=True)
