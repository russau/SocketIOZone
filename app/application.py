from flask import Flask, render_template
from flask_socketio import SocketIO

application = Flask(__name__)
# application.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(application)

@application.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)



if __name__ == '__main__':
    socketio.run(application, debug=True)
