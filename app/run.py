from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import random
from string import ascii_uppercase

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
            room_clients[room] = {"members": 0, "clients": {}} #Maximal 4 Clients
            room_states[room] = {"status": 1} #Geschlossen: 0 | Offen: 1 
        elif code not in room_clients:
            #wenn ein falscher raum code eingegeben wurde
            return render_template("index.html", error="Room does not exist!", nickname=nickname, code=code)
        
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
def connect():
    room = session.get("room")
    nickname = session.get("nickname")
    if not room or not nickname:
        return
    if room not in room_clients:
        leave_room(room)
        return
    
    join_room(room)
    send({"nickname": nickname}, to=room)
    room_clients[room]["members"] += 1
    print(f"{nickname} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    nickname = session.get("nickname")
    leave_room(room)

    if room in room_clients:
        room_clients[room]["memebers"] -= 1
        if room_clients[room]["mmebers"] <= 0:
            del room_clients[room]
            if room in room_states:
                del room_states[room]

    send({"nickname": nickname}, to=room)
    print(f"{nickname} has left the room {room}")
      
if __name__ == '__main__':
    socketio.run(app, debug=True)