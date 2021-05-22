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
    print(subThread.getName(), subThread.isAlive()) #change isAlive to is_alive if using python 3.9


# ----------------------------------- GET DATA FROM COUCHDB --------------------------------------

from couchdb.client import Server, ViewResults
import os

#----------------------------------- ENVIRONMENT DEFINITION --------------------------------------

COUCHDB_IP = os.environ['COUCHDB_IP']
password = os.environ['password'] #password format not sure, string or file
username = os.environ['username']

#--------------------------------------- END DEFINITION ------------------------------------------


#remote server format not sure, test with
server = Server('http://' + username + ':' + password + '@' + COUCHDB_IP + ':5984/')
print('http://' + username + ':' + password + '@' + COUCHDB_IP + ':5984/')
#or test with
#server = Server('http://' + COUCHDB_IP + ':5984/')

#test connection purpose, print all the databases in the server
# for each in server:
#     print(each)

#database names not sure
db1 = server['tweets']  #which stores all the tweets
db2 = server['states']  #which stores all the states information

#map/reduce process
#codes below may not be used, depending on whether we import design documents into databases beforehand
#if imported beforehand, comment out the codes 

#design document for database 'tweets'
#based on the assumption that each tweet is a document
#!! need to confirm the "doc." names => doc.state, doc.semantics
doc1 = {'_id': '_design/stateInfo',
       'views': {
      'perState': {
        'reduce': 'function (keys, values) {\n  \n  return sum(values)/values.length;\n  \n}',
        'map': 'function (doc) {\n  emit(doc.state, doc.semantics);\n}'
      }
    },
    'language': 'javascript'}
db1.save(doc1)

#design document for database 'states'
#based on the assumption that each state is a document
#!! need to confirm the "doc." names => doc.state,doc.median_housing_price,doc.median_age,doc.total_cases
doc2 = {
    "_id": "_design/stateInfo",
    "views": {
      "perState": {
        "map": "function (doc) {\n  emit(doc.state, {\"median housing price\": doc.median_housing_price, \"median age\": doc.median_age, \"total cases\": doc.total_cases});\n}"
      }
    },
    "language": "javascript"
  }
db2.save(doc2)

#mapreduce result for the tweets
result1 = db1.view('stateInfo/perState', group=True).rows
#mapreduce result for the states
result2 = db2.view('stateInfo/perState').rows

#collect the results
data = {}

for row in result1:
    data.update({row.key:{'score': row.value}})
    
for row in result2:
    
    if row.key.upper() in data:
        data[row.key.upper()]['price'] = row.value['median housing price']
        data[row.key.upper()]['age'] = row.value['median age']
        data[row.key.upper()]['cases'] = row.value['total cases']
    else:
        data.update({row.key.upper():{'price':row.value['median housing price']}})
        data[row.key.upper()]['age'] = row.value['median age']
        data[row.key.upper()]['cases'] = row.value['total cases']



#test data
# data = {
#     'A1':{
#         'score':0.1,
#         'price':1000,
#         'cases':100,
#         'age': 23,
#     },
#     'A2':{
#         'score':-0.3,
#         'price':2000,
#         'cases':90,
#         'age':39,
#     },
#     'A3':{
#         'score':-0.2,
#         'price':3000,
#         'cases':108,
#         'age':33,
#     }
# }


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
