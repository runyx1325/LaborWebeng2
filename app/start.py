from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import random, json
from Gameboard import Gameboard
from Figure import Figure
from Player import Player
from Felder import Felder



class Mensch():
    def __init__(self, data):
        #What is happening in __init__?
        #...

        data_room = json.loads(data)
        #data_room is a dict with all sids and usernames in the room

        #save keys (sid) of data_room dict
        self.player_sid = data_room.keys()
        
        # color of Figure
        i = 1
        #list of player objects
        playerlist = [] 
        for key in self.player_sid:
            #save nickname from data_room dict
            self.player_nickname = data_room[key]
            playerlist.append(Player(key, self.player_nickname, i))
            i += 1
        
        
        #1.Spieler auslesen
        #player = list(data_room['clients'].keys())[0]

        #Create Gameboard
        #playerlist := list with 
        self.gameboard = Gameboard(playerlist)
        #return True

        #Start game
        #Gameboard.start()
    
    def start_play(self, data):
        data_room = json.loads(data)
        print(data_room)
        pass