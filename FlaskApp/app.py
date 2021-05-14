from flask import Flask, request, url_for, redirect, render_template, jsonify
app = Flask(__name__, template_folder="Templates", static_folder="static")

# ----------------------------SOCKET IO--------------------------------------
from flask_socketio import SocketIO
app.config['SECRET_KEY'] = 'mySecret'
socketio = SocketIO(app)

namespace = '/backendMonitor'
@socketio.on('connect', namespace=namespace)
def on_connect():
    print("On backendMonitor: Backend Connected!")

@socketio.on('message', namespace=namespace)
def msgHandling(msg):
    print('On backendMonitor received Message: ' + msg)

@socketio.on('disconnect', namespace=namespace)
def on_disconnect():
    print('On backendMonitor: Disconnected!')

# ----------------------------------- END --------------------------------------

import time, threading

def sendData():
    time.sleep(10)
    socketio.emit('getMapData',
                    data,
                    namespace = namespace)
    print("Data sent!!!")

def startSThread(method):
    subThread = threading.Thread(target = method, name = 'sub_thread')
    subThread.setDaemon(True)
    subThread.start()
    print(subThread.getName(), subThread.isAlive())

data = {
    'A1':{
        'score':0.1,
        'price':1000,
        'cases':100,
        'age': 23,
    },
    'A2':{
        'score':-0.3,
        'price':2000,
        'cases':90,
        'age':39,
    },
    'A3':{
        'score':-0.2,
        'price':3000,
        'cases':108,
        'age':33,
    }
}


@app.route('/getMapData')
def add_numbers():
    return jsonify(data)



@app.route('/', methods = ['GET', 'POST'])
def home():
    startSThread(sendData)
    return render_template('chart.html')


if __name__ == '__main__':

    # app.run(port=1003, )
    socketio.run(app, port=1003, debug=True) #, host = ''
