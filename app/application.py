from flask import Flask, render_template
from flask_socketio import SocketIO

import Scroller
from threading import Thread

#########
# import eventlet
# eventlet.monkey_patch(socket=True)
############

application = Flask(__name__)
# application.config['SECRET_KEY'] = 'secret!'
# , async_mode='eventlet'
socketio = SocketIO(application)
thread = None

def squaresEmitter(squares):
    # print(squares)
    socketio.emit('my response', squares)

def background_thread():
    print("starting thread")
    s = Scroller.Scroller(squaresEmitter)
    s.scrollText("Snorlax!!", 0, 255, 0)
    while True:
        print("banana")
        s.scrollText("Banana   ", 0, 0, 255)

@application.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(application, debug=False, host='0.0.0.0')
