from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import random, json
from Gameboard import Gameboard
from Figure import Figure
from Player import Player
from Field import Field



class Mensch():
    def __init__(self, data):
        #What is happening in __init__?
        #...

        self.data_room = json.loads(data)
        #data_room is a dict with all sids and usernames in the room
        self.waiting = False
        #save keys (sid) of data_room dict
        self.player_sid = self.data_room.keys()
        
        #color of Figure
        i = 1
        #list of player objects
        self.playerlist = []
        
        if len(self.player_sid) == 4:
            orderFour = [1, 4, 2, 3]
            i = 0
            for key in self.player_sid:               
                self.player_nickname = self.data_room[key]
                self.playerlist.append(Player(key, self.player_nickname, orderFour[i]))
                i += 1
            
        else: 
            for key in self.player_sid:
                #save nickname from data_room dict
                self.player_nickname = self.data_room[key]
                self.playerlist.append(Player(key, self.player_nickname, i))
                i += 1
        
            
        #Create Gameboard
        self.gameboard = Gameboard(self.playerlist)
        self.playerturn = 0
        #Start game
        #Gameboard.start()
    def start(self):
        #choose current player
        player = self.playerturn % len(self.player_sid)
        #for next move
        self.playerturn +=1

        self.cur_player = list(self.player_sid)[player]
        return self.cur_player
        
    def start_play(self, data):
        data_room = json.loads(data)
        print(data_room)
        pass

    def set_waiting(self, bool):
        self.waiting = bool

    @property
    def get_gameboard(self):
        return self.gameboard
    @property
    def get_waiting(self):
        return self.waiting
    @property
    def get_cur_player(self):
        return self.cur_player