from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/start")
def start():
    return render_template('index.html')

@app.route("/game")
def game():
    return render_template('game/game.html')
  
@socketio.on('connect')
def handle_connect():
    print('Websocket connected!')

@socketio.on('disconnect')
def handle_disconnect():
    print("Websocket disconnected!")

@socketio.on('play')
def handlePlay(json):
    print("Received JSON:" + str(json))
    #emit('updateView', {'player' : id, 'position': }, broadcast = True)
    
    
#socketio.on('dice')
#def handleDice():



    #emit()    

#socketio.on('start')
#def handleStart():
    #emit()


if __name__ == '__main__':
    socketio.run(app)