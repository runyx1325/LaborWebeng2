from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import random, json
from string import ascii_uppercase
from start import Mensch

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

MAX_CLIENTS_PER_ROOM = 4
room_clients = {}
room_states = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in room_clients:
            break
    return code

@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        nickname = request.form.get("nickname")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not nickname:
            #Wenn kein Name eingegeben wurde
            return render_template("index.html", error="Please enter a nickname!", nickname=nickname, code=code)
        if join != False and not code:
            #Wenn auf Join geklickt wurde aber kein Raum Code eingegeben wurde
            return render_template("index.html", error="Please enter a room code!", nickname=nickname, code=code)
        
        room = code
        if create != False:
            #wenn create eingegeben wurde
            room = generate_unique_code(4)
            room_data = {"members": 0, "clients": {}}
            room_clients[room] = json.dumps(room_data) #Maximal 4 Clients
            room_states[room] = {"status": 1} #Geschlossen: 0 | Offen: 1 
        elif code not in room_clients:
            #wenn ein falscher raum code eingegeben wurde
            return render_template("index.html", error="Room does not exist!", nickname=nickname, code=code)
        
        if join != False:
            #wenn raum bereits voll ist
            data = json.loads(room_clients[room])
            if data["members"] >= 4:
                return render_template("index.html", error="Room is closed! Limit of 4 players is reached.", nickname=nickname, code=code)
            elif room_states[room] == 0:
                return render_template("index.html", error="Room is closed! Game is already started.", nickname=nickname, code=code)
        
        session["room"] = room
        session["nickname"] = nickname
        return redirect(url_for("game"))
    
    return render_template("index.html")

@app.route("/game")
def game():
    room = session.get("room")
    if room is None or session.get("nickname") is None or room not in room_clients:
        return redirect(url_for("home"))
    return render_template("game.html", room=room)

@socketio.on('connect')
def connect(auth):
    room = session.get("room")
    nickname = session.get("nickname")
    sid = request.sid
    session["sid"] = sid
    if not room or not nickname:
        return
    if room not in room_clients:
        leave_room(room)
        return
    
    join_room(room)
    type = "user_joined"
    data = json.loads(room_clients[room])
    data["members"] += 1
    data["clients"][sid] = nickname
    client_list = json.dumps(data["clients"])
    room_clients[room] = json.dumps(data)
        
    print(f"Nickname: {nickname} (sid: {sid}) joined room: {room}")
    send('{"type":"' + type + '", "client_list":' + (client_list) + '}', to=room)


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    nickname = session.get("nickname")
    sid = session.get("sid")
    leave_room(room)

    type = "user_left"
    
    if room in room_clients:
        data = json.loads(room_clients[room])
        print(data["members"])
        data["members"] -= 1
        print(data["members"])
        print(data["clients"][sid])
        del data["clients"][sid]
        room_clients[room] = json.dumps(data)
        if data["members"] <= 0:
            del room_clients[room]
            if room in room_states:
                del room_states[room]
        else:
            client_list = json.dumps(data["clients"])
            send('{"type":"' + type + '", "client_list":' + (client_list) + '}', to=room)
    
    print(room_clients)
    print(f"{nickname} {sid} has left the room {room}")

@socketio.on('start-round')
def start_round(data):
    room = data['room']
    data_clients = json.dumps(data['clients'])
    room_states[room] = 0
    game = Mensch(data_clients)
    type="gameboard"
    gameboard = json.dumps(game.get_gameboard.get_gameboard)
    send('{"type":"' + type + '", "gameboard": '+ gameboard +'}', to=room)
    #game1.start() return sid wer dran ist
    #client event dice(sid) drückt button
    #zahl = random
    #show zahl beim client
    #wähle Spieler aus
    #dann schicken wir infos an lea (sid, team, figure id, zahl, startfeld)
    #Zugzahl modulo 4 = Spieler        
    print(data['user'] + ' started round in room: '+ data['room'])

@socketio.on('table-cell-clicked')
def table_cell_clicked(data):
    print('received: ', data)
      
if __name__ == '__main__':
    socketio.run(app, debug=True)