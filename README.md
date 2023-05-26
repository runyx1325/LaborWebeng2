# Mensch ärgere Dich nicht

## Online Multiplayer with Flask and Flask-Socketio

This is a little study project. It's a little Browser realtime multiplayer. You can play this game with 2 - 4 players. For the Websocket Connection between Client and Server, we are using Flask-Socketio. The Frontend is prgrammed with HTML, CSS and JS.


## Starting

You can run this Flask App on localhost with this command:
```
python run.py
```

## Structure

* **templates**:
In this folder you can find all html files. Every page is builded with the base.html + one other html file.
* **static**:
In this folder 3 more folders. One folder for the css files, one for JavaScript files and the last one for all svg images of the gameboard and the animated dice.
* **Game logic**:
All python files except [run.py](app/run.py) are the game logic. In [start.py](app/start.py) the start of a game is programmed. [field.py](app/field.py), [gameboard.py](app/gameboard.py), [player.py](app/player.py) are the diffrent classes for the game.
* **run.py**:
Communication between Client and Server is programmed in [run.py](app/run.py). All events that can happen are here.
