# coding: utf-8
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, send, join_room, leave_room
import random, json, time
from string import ascii_uppercase
from start import Mensch

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Create global dictionaries
MAX_CLIENTS_PER_ROOM = 4
# List of Clients in every existing room
room_clients = {}
# Closed Room: 0 or Open Room: 1
room_states = {}
# Game object of every existing Room
room_game = {}
# Test purposes
settings_endgame = True



# generate unique room code
def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in room_clients:
            break
    return code



# starting page at /
@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    # React only to POST Request
    if request.method == "POST":
        nickname = request.form.get("nickname")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        # No nickname entered
        if not nickname:
            return render_template("index.html", error="Please enter a nickname!", nickname=nickname, code=code)
        
        # Clicked on Join, but no room code was entered
        if join != False and not code:
            return render_template("index.html", error="Please enter a room code!", nickname=nickname, code=code)
        
        room = code
        # Clicked on Create Private Game
        if create != False:
            room = generate_unique_code(4)
            room_data = {"members": 0, "clients": {}}
            room_clients[room] = json.dumps(room_data)
            room_states[room] = {"status": 1}  
        # Entered not existing room code
        elif code not in room_clients:
            return render_template("index.html", error="Room does not exist!", nickname=nickname, code=code)
        
        # Clicked on Join 
        if join != False:
            #wenn raum bereits voll ist
            data = json.loads(room_clients[room])
            # Room is already full
            if data["members"] >= 4:
                return render_template("index.html", error="Room is closed! Limit of 4 players is reached.", nickname=nickname, code=code)
            # Room already started
            elif room_states[room] == 0:
                return render_template("index.html", error="Room is closed! Game is already started.", nickname=nickname, code=code)
        
        # save room and nickname in session cookie
        session["room"] = room
        session["nickname"] = nickname
        # redirect to /game
        return redirect(url_for("game"))
    
    # Redirect to / at GET Requests
    return render_template("index.html")



# game page at /game
@app.route("/game")
def game():
    room = session.get("room")
    # check session cookie is correct
    if room is None or session.get("nickname") is None or room not in room_clients:
        return redirect(url_for("home"))
    return render_template("game.html", room=room)



# impressum page at /impressum
@app.route("/impressum")
def impressum():
    return render_template("impressum.html")



# privacy policy at /privacy
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")



# initialize websocket connection
@socketio.on('connect')
def connect():
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
        
    # user joined the room
    # send event "user_joined" to room 
    send('{"type":"' + type + '", "client_list":' + (client_list) + '}', to=room)



# client disconnect websocket connection
@socketio.on("disconnect")
def disconnect():
    # user left the room
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
        # delete room if 0 members
        if data["members"] <= 0:
            del room_clients[room]
            if room in room_states:
                del room_states[room]
                if room in room_game:
                    del room_game[room]
        else:
            client_list = json.dumps(data["clients"])
            # send event "user_left" to room
            send('{"type":"' + type + '", "client_list":' + (client_list) + '}', to=room)
    


# event start-round
@socketio.on('start-round')
def start_round(data):
    room = data['room']
    data_clients = json.dumps(data['clients'])
    room_states[room] = 0

    # create game object
    game = Mensch(data_clients, settings_endgame)
    room_game[room] = game

    type="gameboard"
    gameboard = json.dumps(game.get_gameboard.get_gameboard)
    # send new gameboard view to room
    send('{"type":"' + type + '", "gameboard": '+ gameboard +'}', to=room)
    # User started game in room
    print(data['user'] + ' started round in room: '+ data['room'])

    # loop while game is not finished
    while game.get_gameboard.get_finished == False:
        # while move not finished game.set_waiting is Ture
        game.set_waiting(True)
        # get socket id of next player
        next_player = game.start()
        type = "dice"   
        # send event dice only to the next player
        send('{"type":"' + type + '"}', room=next_player)
        
        # waiting till move is finished
        while game.get_waiting:
            time.sleep(1)
            if not game.get_waiting:
                break
    #game is finished
    print("Game is finished.")



# event dice
@socketio.on('dice')
def roll_dice(data):
    room = data['room']
    sid_cur_player = data['user']
    user_dict = json.loads(room_clients[room])
    nickname = json.dumps(user_dict["clients"].get(data['user']))
    # dice number generated with random
    number = json.dumps(random.randrange(1,7))
    game = room_game[room]
    game.set_cur_dice(0)
    game.set_cur_dice(number)
    
    # send dice number to game log
    type = "send_dice_result"
    send('{"type":"' + type + '", "number": '+ number +', "user": '+ nickname +'}', to=sid_cur_player)

    # if no move is possible and less than 3 bad moves and all figures on best possible field, try again
    if len(game.get_possible_moves(data['user'])) == 0 and game.get_counter_bad_moves < 2 and game.get_player_dict[data['user']].ready():
        # player can not move with rolled dice number and did not rolled 3 times
        game.update_counter_bad_moves()
        game.again()
        next_player = game.start()
        type = "dice"   
        send('{"type":"' + type + '"}', room=next_player)

    # if player rolled 3 times and rolled no 6, next players turn
    elif game.get_counter_bad_moves == 2 and len(game.get_possible_moves(data['user'])) == 0 and not int(number) == 6:
        game.set_counter_bad_moves()
        game.set_waiting(False)

    # if player can not move but rolled a 6, roll the dice again
    elif len(game.get_possible_moves(data['user'])) == 0 and int(number) == 6:
        game.set_cur_dice(0)
        game.again()
        next_player = game.start()
        type = "dice"   
        send('{"type":"' + type + '"}', room=next_player)

    # if player rolled 3 times and no move is possible
    elif len(game.get_possible_moves(data['user'])) == 0:
        game.set_cur_dice(0)
        game.set_counter_bad_moves()
        game.set_waiting(False)

    # else choose a figure you want to move
    else:
        type = "room-log"
        message = " Choose a figure!"
        color = str(room_game[room].get_player_dict.get(request.sid).get_color)
        game.set_counter_bad_moves()
        # send event "room-log" with message to room
        send('{"type":"' + type + '","user":' + nickname + ',"color":"' + color + '", "msg":"'+ message+'"}', to=room)



# event choose-figrue
@socketio.on('choose-figure')
def choose_figure(data):
    room = data['room']
    sid = data['user']
    field = data['field']
    game = room_game[room]

    # check if correct player clicked the field with correct dice number
    if game.get_cur_player == sid and game.get_cur_dice > 0 and game.get_cur_dice < 7:
        # when move is possible make move
        if game.game_move(sid, field):
            type="gameboard"
            gameboard = json.dumps(game.get_gameboard.get_gameboard)
            # send new gameboard view to room
            send('{"type":"' + type + '", "gameboard": '+ gameboard +'}', to=room)
            game.set_counter_bad_moves()

            # if dice number is 6 player is again
            if game.get_cur_dice == 6 and not game.get_gameboard.get_finished:
                game.set_cur_dice(0)
                type = "dice"   
                send('{"type":"' + type + '"}', room=sid)

            # if game is not finished, next player
            elif not game.get_gameboard.get_finished:
                game.set_cur_dice(0)
                game.set_waiting(False)

            # else game is finsihed
            else:
                game.set_waiting(False)
                game.set_cur_dice(0)
                winner = game.get_winner
                winner_name = json.dumps(winner.get_nickname)
                type = "game_finished"
                # send event "game_finished" to room
                send('{"type":"' + type + '", "winner": '+ winner_name +'}', to=sid)



# event room-log
@socketio.on('room-log')
def send_log(data):
    type = "room-log"
    room = data['room']
    msg  = data['msg']
    user = data['user']
    
    if room in room_game:
        sid = ""
        # get the player color with the socket id
        for key, val in room_game[room].get_player_dict.items():
            if str(val) == str(user):
                sid = str(key)
        color = str(room_game[room].get_player_dict.get(str(sid)).get_color)
        # send event "room-log" with message to room
        send('{"type":"' + type + '","user":"' + user + '","color":"' + color + '", "msg":"'+ msg+'"}', to=room)
    


# starting app
if __name__ == '__main__':
    socketio.run(app, debug=True)