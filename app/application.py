from flask import Flask, render_template
from flask_socketio import SocketIO

from threading import Lock
import time

application = Flask(__name__)
application.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(application)
thread = None
thread_lock = Lock()

def background_thread():
    print("starting thread")
    while True:
        print("emitting from thread")
        socketio.emit('my response', 'from thread')
        socketio.sleep(4)

@application.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')
    socketio.emit('my response', 'from connect')
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)



if __name__ == '__main__':
    socketio.run(application, debug=False)
