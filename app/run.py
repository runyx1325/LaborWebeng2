from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import game

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

MAX_CLIENTS_PER_ROOM = 4
room_clients = {}
room_states = {}

@app.route("/start")
def start():
    return render_template('index.html')
  
@socketio.on('connect')
def handle_connect():
    print('Client connected!')

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected!")

@socketio.on('join')
def handle_join(data):
    print("---")
    print(MAX_CLIENTS_PER_ROOM)
    print("---")
    nickname = data['nickname']
    room = data['room']
    if room not in room_clients:
        room_clients[room] = 0
    if room_clients[room] >= MAX_CLIENTS_PER_ROOM:
        emit('room_full', {'room': room})
    else:
        if room in room_states and room_states[room] == 'running':
            emit('room_running', {'room': room})
        else:
            join_room(room)
            room_clients[room] += 1
            emit('joined', {'nickname': nickname, 'room': room, 'template': 'game.html'}, room=room)

    
@socketio.on('leave')
def handle_leave(data):
    nickname = data['nickname']
    room = data['room']
    leave_room(room)
    room_clients[room] -= 1
    if room_clients[room] == 0:
        del room_clients[room]
        del room_states[room]
    emit('left', {'nickname': nickname, 'room': room}, room=room)
    



    #data = request.get_json()
    #print(data['data'])
    #game = Mensch(data)

    #emit('updateView', {'player' : id, 'position': }, broadcast = True)
    
    
#socketio.on('dice')
#def handleDice():



    #emit()    

#socketio.on('start')
#def handleStart():
    #emit()


if __name__ == '__main__':
    socketio.run(app)