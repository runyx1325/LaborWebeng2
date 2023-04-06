from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/start")
def start():
    return render_template('index.html')

@app.route("/game")
def game():
    return render_template('game/game.html')

if __name__ == '__main__':
    socketio.run(app)