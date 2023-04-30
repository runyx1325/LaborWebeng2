from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, send, join_room, leave_room
import random, json, time
from string import ascii_uppercase
from start import Mensch

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

MAX_CLIENTS_PER_ROOM = 4
room_clients = {}
room_states = {}
room_game = {}

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
    print("\n\nHILDFDasljdfkasjdnn\n\n")
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
        data["members"] -= 1
        del data["clients"][sid]
        room_clients[room] = json.dumps(data)
        if data["members"] <= 0:
            del room_clients[room]
            if room in room_states:
                del room_states[room]
                if room in room_game:
                    del room_game[room]
        else:
            client_list = json.dumps(data["clients"])
            send('{"type":"' + type + '", "client_list":' + (client_list) + '}', to=room)
    print(f"{nickname} {sid} has left the room {room}")

@socketio.on('start-round')
def start_round(data):
    room = data['room']
    data_clients = json.dumps(data['clients'])
    room_states[room] = 0
    game = Mensch(data_clients)
    room_game[room] = game

    type="gameboard"
    gameboard = json.dumps(game.get_gameboard.get_gameboard)
    send('{"type":"' + type + '", "gameboard": '+ gameboard +'}', to=room)
    print(data['user'] + ' started round in room: '+ data['room'])

    while not game.get_gameboard.get_finished:
        print("start move")
        game.set_waiting(True)
        next_player = game.start()
        type = "dice"   
        send('{"type":"' + type + '"}', room=next_player)
        
        while game.get_waiting:
            time.sleep(1)
            if not game.get_waiting:
                break
        print("Next Player: "+next_player)

@socketio.on('dice')
def roll_dice(data):
    room = data['room']
    user_dict = json.loads(room_clients[room])
    nickname =json.dumps(user_dict["clients"].get(data['user']))
    number = json.dumps(random.randrange(1,6))
    game = room_game[room]
    game.set_cur_dice(number)
    
    #if no move is possible and less than 3 bad moves and all figures on best possible field, try again
    print("Liste der bewegbaren Figuren: " + str(game.get_possible_moves(data['user']).keys()))
    if len(game.get_possible_moves(data['user'])) == 0 and game.get_counter_bad_moves < 2 and game.get_player_dict[data['user']].ready:
        #wenn kein zug mögglich und noch nicht 3 Mal gewürfelt und alle figuren im ziel sind aufgerückt oder zu Hause
        #dann würfel nochmal
        type = "send_dice_result"
        send('{"type":"' + type + '", "number": '+ number +', "user": '+ nickname +'}', to=room)
        game.update_counter_bad_moves()
        game.again()
        next_player = game.start()
        type = "dice"   
        send('{"type":"' + type + '"}', room=next_player)
    elif len(game.get_possible_moves(data['user'])) == 0 and game.get_counter_bad_moves == 2:
        type = "send_dice_result"
        send('{"type":"' + type + '", "number": '+ number +', "user": '+ nickname +'}', to=room)
    else:
        type = "send_dice_result"
        send('{"type":"' + type + '", "number": '+ number +', "user": '+ nickname +'}', to=room)

@socketio.on('choose-figure')
def choose_figure(data):
    room = data['room']
    sid = data['user']
    field = data['field']
    game = room_game[room]
    
    if game.get_cur_player == sid:
        if game.game_move(sid, field):
            type="gameboard"
            gameboard = json.dumps(game.get_gameboard.get_gameboard)
            send('{"type":"' + type + '", "gameboard": '+ gameboard +'}', to=room)
            if game.get_cur_dice == 6:
                type = "dice"   
                send('{"type":"' + type + '"}', room=sid)
            else:
                game.set_waiting(False)

@socketio.on('room-log')
def send_log(data):
    print(data)
    type = "room-log"
    room = data['room']
    msg  = data['msg']
    user = data['user']
    color = str(room_game[room].get_player_dict.get(request.sid).get_color)
    send('{"type":"' + type + '","user":"' + user + '","color":"' + color + '", "msg":"'+ msg+'"}', to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)